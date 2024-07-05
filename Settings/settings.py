import sys
import os
import json
import requests
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtSerialPort as qts

from Settings.UI.settings import Ui_dg_settings

filepath = os.path.join(os.path.join(os.path.dirname(__file__), "..", "settings.json"))


def com_ports():
    ports = [""]
    for port in qts.QSerialPortInfo().portName():
        ports.append(port)
    return ports


def read_json_settings(analyzer_name):
    settings_values = None

    if os.path.getsize(filepath) > 0:
        with open(filepath, 'r') as jsonFile:
            data = json.load(jsonFile)

        for analyzer in data:
            if analyzer == analyzer_name:
                settings_values = data[analyzer]
                # settings_values = tuple(settings_values)

        return settings_values


class SettingsForm(qtw.QTabWidget, Ui_dg_settings):
    #
    saved = qtc.Signal(str)

    def __init__(self, analyzer):
        super().__init__()
        # super(SettingsForm, self).__init__()  # this also work
        self.setupUi(self)

        self.buadrate = None
        self.analyzer = None
        self.comport = None
        self.password = None
        self.username = None
        self.site = None
        self.port = None
        self.server = None
        self.bytesize = None
        self.parity = None
        self.stopbits = None
        self.flow_control = None
        self.upl_analyzer_settings = analyzer
        self.txt_sever_name_ip_address.setFocus()

        self.port_names = com_ports()
        # self.cb_comport.addItems(["", "COM1", "COM2"])
        self.cb_comport.addItems(self.port_names)

        self.upload_settings()

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

        settings_values = {}
        analyzer_settings = {}

        filepath = os.path.join(os.path.join(os.path.dirname(__file__), "..", "settings.json"))

        try:

            # senaite lims settings
            self.server = self.txt_sever_name_ip_address.text().strip()
            self.port = self.txt_senaite_port.text().strip()
            self.site = self.txt_site_id.text().strip()
            self.username = self.txt_senaite_username.text().strip()
            self.password = self.txt_senaite_password.text().strip()

            # analyzer settings
            self.analyzer = self.cb_analyzer_name.currentText()
            self.comport = self.cb_comport.currentText().strip()
            self.buadrate = int(self.cb_buadrate.currentText())
            self.bytesize = self.cb_bytesize.currentText()
            self.parity = self.cb_parity.currentText()
            self.stopbits = self.cb_stopbits.currentText()
            self.flow_control = self.cb_flow_control.currentText()

            settings_values.update({"server": self.server})
            settings_values.update({"port": self.port})
            settings_values.update({"site": self.site})
            settings_values.update({"username": self.username})
            settings_values.update({"password": self.password})
            settings_values.update({"analyzer": self.analyzer})
            settings_values.update({"port_name": self.comport})
            settings_values.update({"buadrate": self.buadrate})
            settings_values.update({"bytesize": self.bytesize})
            settings_values.update({"parity": self.parity})
            settings_values.update({"stopbits": self.stopbits})
            settings_values.update({"flowcontrol": self.flow_control})

            analyzer_settings.update({self.analyzer: settings_values})

            if os.path.getsize(filepath) == 0:
                with open(filepath, 'w') as jsonfile:
                    json.dump(analyzer_settings, jsonfile, indent=4)
            else:
                with open(filepath, 'r') as jsonFile:
                    data = json.load(jsonFile)

                data.update(analyzer_settings)

                with open(filepath, 'w') as jsonfile:
                    json.dump(data, jsonfile, indent=4)

            # emit signal
            self.saved.emit(self.analyzer)

            qtw.QMessageBox.information(self, "Saving Settings", f"{self.analyzer} settings saved!")

            self.close()

        except Exception as e:
            qtw.QMessageBox.critical(self, "Error", f"{e}")

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

    def upload_settings(self):
        if self.upl_analyzer_settings:
            uploaded_settings = read_json_settings(self.upl_analyzer_settings)

            for key in uploaded_settings.keys():

                match key:

                    case "server":
                        self.txt_sever_name_ip_address.setText(uploaded_settings[key])
                    case "port":
                        self.txt_senaite_port.setText(uploaded_settings[key])
                    case "site":
                        self.txt_site_id.setText(uploaded_settings[key])
                    case "username":
                        self.txt_senaite_username.setText(uploaded_settings[key])
                    case "password":
                        self.txt_senaite_password.setText(uploaded_settings[key])
                    case "analyzer":
                        self.cb_analyzer_name.setCurrentText(uploaded_settings[key])
                    case "port_name":
                        self.cb_comport.setCurrentText(uploaded_settings[key])
                    case "buadrate":
                        self.cb_buadrate.setCurrentText(str(uploaded_settings[key]))
                    case "bytesize":
                        self.cb_bytesize.setCurrentText(uploaded_settings[key])
                    case "parity":
                        self.cb_parity.setCurrentText(uploaded_settings[key])
                    case "stopbits":
                        self.cb_stopbits.setCurrentText(uploaded_settings[key])
                    case "flowcontrol":
                        self.cb_flow_control.setCurrentText(uploaded_settings[key])
                    case _:
                        pass


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)

    window = SettingsForm()
    window.show()

    sys.exit(app.exec())
