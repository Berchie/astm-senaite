import os
import sys
import json
import threading
import sqlite3
import serial
from PySide6.QtCore import Slot, Signal, QObject, QThread
from PySide6.QtWidgets import QMessageBox, QApplication, QWidget, QTableWidgetItem
from Middleware.UI.ASTM_Middleware import Ui_astm_middleware
from Settings.settings import SettingsForm
from Middleware.fujifilm_chemistry_nx500 import nx500_parser_data
from Middleware.process_astm_message import parse_astm_data
from Middleware.senaite import transfer_to_senaite, process_settings_name
from Settings.senaite_connect import login_senaite_api


# setting.json filepath
# filepath = os.path.join(os.path.join(os.path.dirname(__file__), "data", "settings.json"))
# text_filepath = os.path.join(os.path.join(os.path.dirname(__file__), "data", "setting_names.txt"))

# sqlit database path
# db_path = os.path.join(os.path.dirname(__file__), "data", "result_astm.db")


# def read_json_serial_setting(analyzer_name):
#     serial_config_values = None
#     comport_parameters = []
#     # comport_parameters_value = putting everything together to mdi window
#
#     bytesize = {"5": serial.FIVEBITS, "6": serial.SIXBITS, "7": serial.SEVENBITS, "8": serial.EIGHTBITS}
#     parity = {"None": serial.PARITY_NONE, "Even": serial.PARITY_EVEN, "Odd": serial.PARITY_ODD,
#               "Mark": serial.PARITY_MARK, "Space": serial.PARITY_SPACE}
#     stopbits = {"1": serial.STOPBITS_ONE, "1.5": serial.STOPBITS_ONE_POINT_FIVE, "2": serial.STOPBITS_TWO}
#
#     if os.path.getsize(filepath) > 0:
#         with open(filepath, 'r') as jsonfile:
#             data = json.load(jsonfile)
#
#         for analyzer in data:
#             if analyzer == analyzer_name:
#                 serial_config_values = data[analyzer]
#
#         if serial_config_values:
#             for index in serial_config_values.keys():
#                 if index == "port_name":
#                     comport_parameters.append(serial_config_values[index])
#
#                 if index == "buadrate":
#                     comport_parameters.append(serial_config_values[index])
#
#                 if index == "bytesize":
#                     comport_parameters.append(bytesize[serial_config_values[index]])
#
#                 if index == "parity":
#                     comport_parameters.append(parity[serial_config_values[index]])
#
#                 if index == "stopbits":
#                     comport_parameters.append(stopbits[serial_config_values[index]])
#
#                 if index == "flowcontrol":
#                     if serial_config_values[index] == "None":
#                         xonxoff = False
#                         rtscts = False
#                         comport_parameters.append(xonxoff)
#                         comport_parameters.append(rtscts)
#                     elif serial_config_values[index] == "Software":
#                         xonxoff = True
#                         rtscts = False
#                         comport_parameters.append(xonxoff)
#                         comport_parameters.append(rtscts)
#                     else:
#                         xonxoff = False
#                         rtscts = True
#                         comport_parameters.append(xonxoff)
#                         comport_parameters.append(rtscts)
#
#         # comport_parameters_value = tuple(comport_parameters)
#
#         return comport_parameters


class SerialReadWorker(QObject):
    data_received = Signal(bytes)
    error_occurred = Signal(str)

    def __init__(self, port_name, buadrate, bytesize, parity, stopbits, xonxoff=False, rtscts=False):
        super().__init__()
        self.port_name = port_name
        self.buadrate = buadrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self.serialPort = None
        self.running = True
        self.thread = None

    @Slot()
    def start(self):
        try:
            self.serialPort = serial.Serial(self.port_name, self.buadrate, timeout=1, bytesize=self.bytesize,
                                            parity=self.parity, stopbits=self.stopbits,
                                            xonxoff=self.xonxoff, rtscts=self.rtscts)

        except serial.SerialException as e:
            self.error_occurred.emit(f"Failed to open port {self.port_name}: {e}")
            return

        self.thread = threading.Thread(target=self.onReadyReadMessageFromPort)
        self.thread.start()

    @Slot()
    def onReadyReadMessageFromPort(self):
        while self.running:
            # while True:
            try:
                if self.serialPort.in_waiting:
                    data = self.serialPort.read(self.serialPort.in_waiting)
                    self.data_received.emit(data)
            except serial.SerialException as e:
                self.error_occurred.emit(f"Serial port error: {e}")
                break

    def write_to_port(self, data):
        try:
            self.serialPort.write(data)
        except serial.SerialException as e:
            self.error_occurred.emit(f"Failed to write data: {e}")

    def stop(self):
        self.running = False
        if self.serialPort:
            self.serialPort.close()
        if self.thread and self.thread.is_alive():
            self.thread.join()


class MiddlewareWindow(QWidget, Ui_astm_middleware):
    send_setting_name = Signal(str)
    share_variable = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.uiWorker = None
        self.uiWorkerThread = None
        self.form_Settings = None

        # setup
        self.analyzerName = None
        self.analyzerSettingsName = None

        self.btn_stop_listener.setEnabled(False)

        # port_parameter = read_json_serial_setting(self.analyzerName)
        # MiddlewareWindow.share_variable = self.windowTitle()

        # find data file
        self.filepath = self.find_data_file("settings.json")
        self.text_filepath = self.find_data_file("setting_names.txt")
        self.db_path = self.find_data_file("result_astm.db")

        # buffer
        self.buffer = b''

        # string astm message
        self.astm_message = ""

        # tableWidget
        self.sqlite_data_table.setColumnWidth(0, 200)
        self.sqlite_data_table.setColumnWidth(1, 80)
        self.sqlite_data_table.setColumnWidth(2, 110)
        self.sqlite_data_table.setColumnWidth(3, 300)

        # load data into QTableWidget
        self.load_sqlite_db_data()

        # self.uiWorkerThread = QThread()
        # self.uiWorker = SerialReadWorker(self.port, self.buadrate, self.bytesize, self.parity, self.stopbits, self.xonxoff, self.rtscts)
        # self.uiWorker.moveToThread(self.uiWorkerThread)
        # self.uiWorkerThread.started.connect(self.uiWorker.start)
        # self.uiWorker.data_received.connect(self.onDataReceived)
        # self.uiWorker.error_occurred.connect(self.showError)

        self.btn_settings.clicked.connect(self.middleware_settings)
        self.btn_start_listener.clicked.connect(self.startListener)
        self.btn_stop_listener.clicked.connect(self.stopListener)

    def load_sqlite_db_data(self):

        try:
            if os.path.exists(self.db_path):
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM transactions")

                sqlit_data = cursor.fetchall()
                self.sqlite_data_table.setRowCount(len(sqlit_data))

                for row, row_data in enumerate(sqlit_data):
                    for col, cell_data in enumerate(row_data):
                        self.sqlite_data_table.setItem(row, col, QTableWidgetItem(cell_data))

                cursor.close()
                conn.close()
        except Exception as e:
            QMessageBox.critical(self, "SQLite Error", f"Error occurred: {str(e)}")

    @Slot()
    def middleware_settings(self):

        self.form_Settings = SettingsForm(self.analyzerSettingsName)
        self.form_Settings.saved.connect(self.update_windowTitle)
        self.form_Settings.analyzer_settings_name.connect(self.middlewareSettingsName)
        self.form_Settings.show()

    @Slot()
    def startListener(self):

        # port_parameter = read_json_serial_setting(self.analyzerSettingsName)
        port_parameter = self.read_json_serial_setting()

        if port_parameter:
            port, buadrate, bytesize, parity, stopbits, xonxoff, rtscts = port_parameter

            self.uiWorkerThread = QThread()
            self.uiWorker = SerialReadWorker(port, buadrate, bytesize, parity, stopbits, xonxoff, rtscts)
            self.uiWorker.moveToThread(self.uiWorkerThread)
            self.uiWorkerThread.started.connect(self.uiWorker.start)
            self.uiWorker.data_received.connect(self.onDataReceived)
            self.uiWorker.error_occurred.connect(self.showError)

            self.uiWorker.start()
            self.astm_msg_textEdit.append(f"Started listening to the {port} port")

            self.btn_start_listener.setEnabled(False)
            self.btn_settings.setEnabled(False)
            self.btn_stop_listener.setEnabled(True)

            process_settings_name(self.analyzerSettingsName)

            self.store_settings_name()

            # login to senaite api
            login_senaite_api()

    @Slot(str, str)
    def update_windowTitle(self, title, com):
        self.setWindowTitle(f"{title}_{com}[ASTM Middleware]")
        self.analyzerName = title
        MiddlewareWindow.share_variable = f"{title}_{com}[ASTM Middleware]"

    @Slot(str)
    def middlewareSettingsName(self, analyzerSettingsName):
        self.analyzerSettingsName = analyzerSettingsName

    @Slot(bytes)
    def onDataReceived(self, data):
        self.buffer += data if isinstance(data, bytes) else data.encode()
        # self.astm_msg_textEdit.append(f"Data received: {data}")
        self.processASTMMessages()

    def processASTMTransfer(self):
        # this method is place in the Context of EOT (End of Transmission) character of processingASTMMessage,
        # ensuring the message ends before transferring ASTM Message.
        # passing the message through a parser to process the message to transfer to senaite lims
        if self.analyzerName == "DRI-CHEM NX500":
            if self.astm_message:
                self.astm_msg_textEdit.append("Preparing the ASTM Message for transfer to SENAITE LIMS")
                data = nx500_parser_data(self.astm_message)
                if data:
                    self.astm_msg_textEdit.append("Transferring the ASTM Message to SENAITE LIMS")
                    transfer_to_senaite(data)
                    # self.astm_msg_textEdit.append(resp)
                self.astm_message = ''
        else:
            if self.astm_message:
                self.astm_msg_textEdit.append("Preparing the ASTM Message for transfer to SENAITE LIMS")
                data = parse_astm_data(self.astm_message)
                if data:
                    self.astm_msg_textEdit.append("Transferring the ASTM Message to SENAITE LIMS\n")
                    resp = transfer_to_senaite(data)
                    self.astm_msg_textEdit.append(resp)
                self.astm_message = ''

        # load data into the table for newly added
        self.load_sqlite_db_data()

    def processASTMMessages(self):
        ENQ = b'\x05'
        STX = b'\x02'
        ETX = b'\x03'
        ETB = b'\x17'
        EOT = b'\x04'
        ACK = b'\x06'
        NAK = b'\x15'
        CR = b'\x0D'
        LF = b'\x0A'

        while True:
            if ENQ in self.buffer:
                enq_pos = self.buffer.find(ENQ)
                self.buffer = self.buffer[enq_pos + 1:]
                self.uiWorker.write_to_port(ACK)
                self.astm_msg_textEdit.append("ENQ received, ACK sent.")
                continue

            if STX in self.buffer:
                stx_pos = self.buffer.find(STX)
                end_block_pos = self.buffer.find(ETX, stx_pos)
                if end_block_pos == -1:
                    end_block_pos = self.buffer.find(ETB, stx_pos)

                if end_block_pos != -1:
                    message_block = self.buffer[stx_pos + 1:end_block_pos]
                    self.buffer = self.buffer[end_block_pos + 1:]
                    self.astm_message += message_block.decode()
                    self.astm_msg_textEdit.append(f"Received block: {message_block.decode()}")
                    self.uiWorker.write_to_port(ACK)
                    self.astm_msg_textEdit.append("Block ACK sent.")
                    continue
                else:
                    break

            if EOT in self.buffer:
                eot_pos = self.buffer.find(EOT)
                self.buffer = self.buffer[eot_pos + 1:]
                self.astm_msg_textEdit.append("EOT received. Transmission complete.")
                self.uiWorker.write_to_port(ACK)
                self.astm_msg_textEdit.append("EOT ACK sent.")
                self.processASTMTransfer()
                break

            if NAK in self.buffer:
                nak_pos = self.buffer.find(NAK)
                self.buffer = self.buffer[nak_pos + 1:]
                self.astm_msg_textEdit.append("NAK received. Transmission error.")
                break

            break

    def sendData(self):
        data = "Hello Serial Port"
        self.uiWorker.write_to_port(data.encode())
        self.astm_msg_textEdit.append(f"Sent: {data}")

    @Slot(str)
    def showError(self, message):
        QMessageBox.critical(self, "Error", message)
        self.astm_msg_textEdit.append(f"Error: {message}")

    # using data files
    # finding them using the code below
    @staticmethod
    def find_data_file(filename):
        if getattr(sys, "frozen", False):
            # The application is frozen
            datadir = os.path.dirname(sys.executable)
            return os.path.join(datadir, "data", filename)
        else:
            # The application is not frozen
            # Change this bit to match where you store your data files:
            datadir = os.path.dirname(__file__)
        return os.path.join(datadir, "..", "data", filename)

    def read_json_serial_setting(self):
        serial_config_values = None
        comport_parameters = []
        # comport_parameters_value = putting everything together to mdi window

        bytesize = {"5": serial.FIVEBITS, "6": serial.SIXBITS, "7": serial.SEVENBITS, "8": serial.EIGHTBITS}
        parity = {"None": serial.PARITY_NONE, "Even": serial.PARITY_EVEN, "Odd": serial.PARITY_ODD,
                  "Mark": serial.PARITY_MARK, "Space": serial.PARITY_SPACE}
        stopbits = {"1": serial.STOPBITS_ONE, "1.5": serial.STOPBITS_ONE_POINT_FIVE, "2": serial.STOPBITS_TWO}

        if os.path.getsize(self.filepath) > 0:
            with open(self.filepath, 'r') as jsonfile:
                data = json.load(jsonfile)

            for analyzer_setting in data:
                if analyzer_setting == self.analyzerSettingsName:
                    serial_config_values = data[analyzer_setting]

            if serial_config_values:
                for index in serial_config_values.keys():
                    if index == "port_name":
                        comport_parameters.append(serial_config_values[index])

                    if index == "buadrate":
                        comport_parameters.append(serial_config_values[index])

                    if index == "bytesize":
                        comport_parameters.append(bytesize[serial_config_values[index]])

                    if index == "parity":
                        comport_parameters.append(parity[serial_config_values[index]])

                    if index == "stopbits":
                        comport_parameters.append(stopbits[serial_config_values[index]])

                    if index == "flowcontrol":
                        if serial_config_values[index] == "None":
                            xonxoff = False
                            rtscts = False
                            comport_parameters.append(xonxoff)
                            comport_parameters.append(rtscts)
                        elif serial_config_values[index] == "Software":
                            xonxoff = True
                            rtscts = False
                            comport_parameters.append(xonxoff)
                            comport_parameters.append(rtscts)
                        else:
                            xonxoff = False
                            rtscts = True
                            comport_parameters.append(xonxoff)
                            comport_parameters.append(rtscts)

            # comport_parameters_value = tuple(comport_parameters)

            return comport_parameters

    def delete_settings(self):
        new_settings = {}

        if os.path.getsize(self.filepath) > 0:
            with open(self.filepath, 'r') as jsonFile:
                data = json.load(jsonFile)

            if data:
                for analyzer_setting in data:
                    if analyzer_setting == self.analyzerSettingsName:
                        pass
                    else:
                        new_settings.update({analyzer_setting: data[analyzer_setting]})

                with open(self.filepath, "w") as jsonfile:
                    if new_settings:
                        json.dump(new_settings, jsonfile, indent=4)
                    else:
                        jsonfile.write("")

    # @staticmethod
    def store_settings_name(self):
        with open(self.text_filepath, "w") as textfile:
            textfile.write(f"{self.analyzerSettingsName}")

    def stopListener(self):
        if self.uiWorker:
            self.uiWorker.stop()
            self.uiWorkerThread.quit()
            self.uiWorkerThread.wait()

        self.btn_start_listener.setEnabled(True)
        self.btn_settings.setEnabled(True)
        self.btn_stop_listener.setEnabled(False)

    def closeEvent(self, event):
        if self.uiWorker:
            self.uiWorker.stop()
            self.uiWorkerThread.quit()
            self.uiWorkerThread.wait()
            event.accept()

        self.delete_settings()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MiddlewareWindow()
    window.show()

    sys.exit(app.exec())
