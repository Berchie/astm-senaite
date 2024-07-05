import os
import sys
import json
import threading

import requests
import serial
from PySide6.QtCore import Slot, Signal, QIODevice, QObject, QThread
from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication, QWidget
from PySide6 import QtGui as qtg
from Middleware.UI.ASTM_Middleware import Ui_astm_middleware
from Settings.settings import SettingsForm


# setting.json filepath
filepath = os.path.join(os.path.join(os.path.dirname(__file__), "..", "settings.json"))


def read_json_serial_setting(analyzer_name):
    serial_config_values = None
    comport_parameters = []
    # comport_parameters_value =

    bytesize = {"5": serial.FIVEBITS, "6": serial.SIXBITS, "7": serial.SEVENBITS, "8": serial.EIGHTBITS}
    parity = {"None": serial.PARITY_NONE, "Even": serial.PARITY_EVEN, "Odd": serial.PARITY_ODD, "Mark": serial.PARITY_MARK, "Space": serial.PARITY_SPACE}
    stopbits = {"1": serial.STOPBITS_ONE, "1.5": serial.STOPBITS_ONE_POINT_FIVE, "2": serial.STOPBITS_TWO}

    if os.path.getsize(filepath) > 0:
        with open(filepath, 'r') as jsonfile:
            data = json.load(jsonfile)

        for analyzer in data:
            if analyzer == analyzer_name:
                serial_config_values = data[analyzer]

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
            self.serialPort = serial.Serial(self.port_name, self.buadrate, timeout=1, bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits,
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
        if self.thread.is_alive():
            self.thread.join()


class MiddlewareWindow(QWidget, Ui_astm_middleware):
    edit_settings = Signal()

    def __init__(self):
        super().__init__()
        self.uiWorker = None
        self.uiWorkerThread = None
        self.setupUi(self)

        # setup
        self.analyzerName = None

        self.btn_stop_listener.setEnabled(False)

        # port_parameter = read_json_serial_setting(self.analyzerName)

        # buffer
        self.buffer = b''

        # self.uiWorkerThread = QThread()
        # self.uiWorker = SerialReadWorker(self.port, self.buadrate, self.bytesize, self.parity, self.stopbits, self.xonxoff, self.rtscts)
        # self.uiWorker.moveToThread(self.uiWorkerThread)
        # self.uiWorkerThread.started.connect(self.uiWorker.start)
        # self.uiWorker.data_received.connect(self.onDataReceived)
        # self.uiWorker.error_occurred.connect(self.showError)

        self.btn_settings.clicked.connect(self.middleware_settings)
        self.btn_start_listener.clicked.connect(self.startListener)
        self.btn_stop_listener.clicked.connect(self.stopListener)

    @Slot()
    def middleware_settings(self):

        self.form_Settings = SettingsForm(self.analyzerName)
        self.form_Settings.saved.connect(self.update_windowTitle)
        self.form_Settings.show()

    @Slot()
    def startListener(self):

        port_parameter = read_json_serial_setting(self.analyzerName)

        if port_parameter:
            port, buadrate, bytesize, parity, stopbits, xonxoff, rtscts = port_parameter

            self.uiWorkerThread = QThread()
            self.uiWorker = SerialReadWorker(port, buadrate, bytesize, parity, stopbits, xonxoff, rtscts)
            self.uiWorker.moveToThread(self.uiWorkerThread)
            self.uiWorkerThread.started.connect(self.uiWorker.start)
            self.uiWorker.data_received.connect(self.onDataReceived)
            self.uiWorker.error_occurred.connect(self.showError)

            self.btn_start_listener.setEnabled(False)
            self.btn_settings.setEnabled(False)

    @Slot(str)
    def update_windowTitle(self, title):
        self.setWindowTitle(title)
        self.analyzerName = title

    @Slot(bytes)
    def onDataReceived(self, data):
        self.buffer += data
        self.astm_msg_textEdit.append(f"Data received: {data}")
        self.processASTMMessages()

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

    def stopListener(self, event):
        if self.uiWorker:
            self.uiWorker.stop()
            self.uiWorkerThread.quit()
            self.uiWorkerThread.wait()
            event.accept()

        self.btn_start_listener.setEnabled(True)
        self.btn_settings.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MiddlewareWindow()
    window.show()

    sys.exit(app.exec())
