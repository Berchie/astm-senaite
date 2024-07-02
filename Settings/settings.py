import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtSerialPort as qts

from Settings.UI.settings import Ui_dg_settings


def com_ports():
    port = qts.QSerialPortInfo()
    return port.portName()


class SettingsForm(qtw.QTabWidget, Ui_dg_settings):
    def __init__(self):
        super().__init__()
        # super(SettingsForm, self).__init__()  # this also work
        self.setupUi(self)

        self.port = com_ports()
        self.cb_comport.addItems(["", "COM1", "COM2"])

        # close the form
        self.btnbx_save_cancel.button(qtw.QDialogButtonBox.StandardButton.Cancel).clicked.connect(self.close)

        # save settings
        self.btnbx_save_cancel.button(qtw.QDialogButtonBox.StandardButton.Save).clicked.connect(self.save)

    def save(self):
        pass


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)

    window = SettingsForm()
    window.show()

    sys.exit(app.exec())
