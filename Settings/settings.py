import sys

import requests
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtSerialPort as qts

from Settings.UI.settings import Ui_dg_settings


def com_ports():
    ports = [""]
    for port in qts.QSerialPortInfo().portName():
        ports.append(port)
    return ports


class SettingsForm(qtw.QTabWidget, Ui_dg_settings):
    #
    saved = qtc.Signal(str, str, str, str, str, str, int, str, str, str, str)

    def __init__(self, ):
        super().__init__()
        # super(SettingsForm, self).__init__()  # this also work
        self.buadrate = None
        self.analyzer = None
        self.comport = None
        self.password = None
        self.username = None
        self.site = None
        self.port = None
        self.server = None
        self.bytesite = None
        self.parity = None
        self.stopbits = None
        self.flow_control = None
        self.setupUi(self)

        self.txt_sever_name_ip_address.setFocus()

        self.port_names = com_ports()
        # self.cb_comport.addItems(["", "COM1", "COM2"])
        self.cb_comport.addItems(self.port_names)

        # message dialog box
        self.msgBox = qtw.QMessageBox()
        self.msgBox.setWindowTitle("Testing SENAITE LIMS")
        self.msgBox.setIcon(qtw.QMessageBox.Information)

        # close the form
        self.btnbx_save_cancel.button(qtw.QDialogButtonBox.StandardButton.Cancel).clicked.connect(self.close)

        # save settings
        self.btnbx_save_cancel.button(qtw.QDialogButtonBox.StandardButton.Save).clicked.connect(self.save)

        # reset senaite settings
        self.btnbx_reset_senaite_settings.clicked.connect(self.rest)

        # restore analyzer settings
        self.btnbx_restore_analyzer_default_settings.button(qtw.QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(self.restore)

        # test senaite connection
        self.pb_test_lims.clicked.connect(self.test_senaite)

    @qtc.Slot()
    def save(self):
        # self.saved.emit()
        # senaite lims settings
        self.server = self.txt_sever_name_ip_address.text().strip()
        self.port = self.txt_senaite_port.text().strip()
        self.site = self.txt_site_id.text().strip()
        self.username = self.txt_senaite_username.text().strip()
        self.password = self.txt_senaite_password.text().strip()

        # analyzer settings
        self.analyzer = self.cb_analyzer_name.currentText()
        self.comport = int(self.cb_comport.currentText().strip())
        self.buadrate = self.cb_buadrate.currentText()
        self.bytesite = self.cb_bytesize.currentText()
        self.parity = self.cb_parity.currentText()
        self.stopbits = self.cb_stopbits.currentText()
        self.flow_control = self.cb_flow_control.currentText()

        self.saved.emit(self.server, self.port, self.site, self.username, self.password, self.analyzer,
                        self.comport, self.buadrate, self.bytesite, self.parity, self.stopbits, self.flow_control)

        # print(self.server)
        # print(self.port)
        # print(self.site)
        # print(self.analyzer)
        # print(self.comport)
        # print(self.buadrate)


    def rest(self):
        self.txt_sever_name_ip_address.clear()
        self.txt_senaite_port.clear()
        self.txt_site_id.clear()
        self.txt_senaite_username.clear()
        self.txt_senaite_password.clear()
        self.txt_sever_name_ip_address.setFocus()


    def restore(self):
        # self.cb_analyzer_name.setCurrentText("Select Analyzer")
        self.cb_comport.setCurrentText("")
        self.cb_buadrate.setCurrentText("9600")
        self.cb_bytesize.setCurrentText("8")
        self.cb_parity.setCurrentText("None")
        self.cb_stopbits.setCurrentText("1")
        self.cb_flow_control.setCurrentText("None")


    def test_senaite(self):
        try:
            senaite_url = f"{self.txt_sever_name_ip_address.text().strip()}:{self.txt_senaite_port.text().strip()}/{self.txt_site_id.text().strip()}"
            resp = requests.post(f"http://{senaite_url}/@@API/senaite/v1/login", params={"__ac_name": self.txt_senaite_username.text().strip(),
                                                                                         "__ac_password": self.txt_senaite_password.text().strip()})

            if resp.status_code == 200 and resp.json()["items"]:
                self.msgBox.setText("Connection to SENAITE LIMS is successful!")
                self.msgBox.exec()
            elif resp.status_code == 401:
                self.msgBox.setText(f"{resp.json()["message"]}")
                self.msgBox.exec()
            elif resp.status_code == 200 and resp.json()["message"]:
                self.msgBox.setText(f"{resp.json()["message"]}")
                self.msgBox.exec()
            else:
                self.msgBox.setText("Connection to SENAITE LIMS fails!")
                self.msgBox.exec()
        except ConnectionError as cerr:
            qtw.QMessageBox.critical(self, "Error", str(cerr))
        except Exception as e:
            qtw.QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)

    window = SettingsForm()
    window.show()

    sys.exit(app.exec())
