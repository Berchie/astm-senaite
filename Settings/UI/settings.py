# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTabWidget, QVBoxLayout, QWidget)
import Icons_rc

class Ui_dg_settings(object):
    def setupUi(self, dg_settings):
        if not dg_settings.objectName():
            dg_settings.setObjectName(u"dg_settings")
        dg_settings.setWindowModality(Qt.WindowModality.ApplicationModal)
        dg_settings.resize(376, 423)
        font = QFont()
        font.setPointSize(10)
        dg_settings.setFont(font)
        icon = QIcon()
        icon.addFile(u":/Main/port.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        dg_settings.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(dg_settings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(dg_settings)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_senaite_lims = QWidget()
        self.tab_senaite_lims.setObjectName(u"tab_senaite_lims")
        self.gridLayout_2 = QGridLayout(self.tab_senaite_lims)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(27)
        self.lb_server_name = QLabel(self.tab_senaite_lims)
        self.lb_server_name.setObjectName(u"lb_server_name")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lb_server_name)

        self.txt_sever_name_ip_address = QLineEdit(self.tab_senaite_lims)
        self.txt_sever_name_ip_address.setObjectName(u"txt_sever_name_ip_address")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.txt_sever_name_ip_address)

        self.lb_port = QLabel(self.tab_senaite_lims)
        self.lb_port.setObjectName(u"lb_port")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lb_port)

        self.txt_senaite_port = QLineEdit(self.tab_senaite_lims)
        self.txt_senaite_port.setObjectName(u"txt_senaite_port")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.txt_senaite_port)

        self.lb_seiteid = QLabel(self.tab_senaite_lims)
        self.lb_seiteid.setObjectName(u"lb_seiteid")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lb_seiteid)

        self.txt_site_id = QLineEdit(self.tab_senaite_lims)
        self.txt_site_id.setObjectName(u"txt_site_id")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.txt_site_id)

        self.lb_username = QLabel(self.tab_senaite_lims)
        self.lb_username.setObjectName(u"lb_username")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lb_username)

        self.txt_senaite_username = QLineEdit(self.tab_senaite_lims)
        self.txt_senaite_username.setObjectName(u"txt_senaite_username")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.txt_senaite_username)

        self.lb_password = QLabel(self.tab_senaite_lims)
        self.lb_password.setObjectName(u"lb_password")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lb_password)

        self.txt_senaite_password = QLineEdit(self.tab_senaite_lims)
        self.txt_senaite_password.setObjectName(u"txt_senaite_password")
        self.txt_senaite_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.txt_senaite_password)


        self.gridLayout_2.addLayout(self.formLayout, 0, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(148)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 30)
        self.pb_test_lims = QPushButton(self.tab_senaite_lims)
        self.pb_test_lims.setObjectName(u"pb_test_lims")

        self.horizontalLayout.addWidget(self.pb_test_lims)

        self.btnbx_reset_senaite_settings = QDialogButtonBox(self.tab_senaite_lims)
        self.btnbx_reset_senaite_settings.setObjectName(u"btnbx_reset_senaite_settings")
        self.btnbx_reset_senaite_settings.setStandardButtons(QDialogButtonBox.StandardButton.Reset)

        self.horizontalLayout.addWidget(self.btnbx_reset_senaite_settings)


        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 2)

        self.tabWidget.addTab(self.tab_senaite_lims, "")
        self.tab_analyzer = QWidget()
        self.tab_analyzer.setObjectName(u"tab_analyzer")
        self.gridLayout = QGridLayout(self.tab_analyzer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setHorizontalSpacing(21)
        self.formLayout_2.setVerticalSpacing(21)
        self.lb_analyzer_name = QLabel(self.tab_analyzer)
        self.lb_analyzer_name.setObjectName(u"lb_analyzer_name")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.lb_analyzer_name)

        self.cb_analyzer_name = QComboBox(self.tab_analyzer)
        self.cb_analyzer_name.addItem("")
        self.cb_analyzer_name.addItem("")
        self.cb_analyzer_name.addItem("")
        self.cb_analyzer_name.addItem("")
        self.cb_analyzer_name.addItem("")
        self.cb_analyzer_name.setObjectName(u"cb_analyzer_name")
        self.cb_analyzer_name.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.cb_analyzer_name.setFrame(True)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.cb_analyzer_name)

        self.lb_com_port = QLabel(self.tab_analyzer)
        self.lb_com_port.setObjectName(u"lb_com_port")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.lb_com_port)

        self.cb_comport = QComboBox(self.tab_analyzer)
        self.cb_comport.setObjectName(u"cb_comport")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.cb_comport)

        self.lb_buadrate = QLabel(self.tab_analyzer)
        self.lb_buadrate.setObjectName(u"lb_buadrate")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.lb_buadrate)

        self.cb_buadrate = QComboBox(self.tab_analyzer)
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.addItem("")
        self.cb_buadrate.setObjectName(u"cb_buadrate")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.cb_buadrate)

        self.lb_bytesize = QLabel(self.tab_analyzer)
        self.lb_bytesize.setObjectName(u"lb_bytesize")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.lb_bytesize)

        self.cb_bytesize = QComboBox(self.tab_analyzer)
        self.cb_bytesize.addItem("")
        self.cb_bytesize.addItem("")
        self.cb_bytesize.addItem("")
        self.cb_bytesize.addItem("")
        self.cb_bytesize.setObjectName(u"cb_bytesize")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.cb_bytesize)

        self.lb_parity = QLabel(self.tab_analyzer)
        self.lb_parity.setObjectName(u"lb_parity")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.lb_parity)

        self.cb_parity = QComboBox(self.tab_analyzer)
        self.cb_parity.addItem("")
        self.cb_parity.addItem("")
        self.cb_parity.addItem("")
        self.cb_parity.addItem("")
        self.cb_parity.addItem("")
        self.cb_parity.setObjectName(u"cb_parity")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.cb_parity)

        self.lb_stopbits = QLabel(self.tab_analyzer)
        self.lb_stopbits.setObjectName(u"lb_stopbits")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.lb_stopbits)

        self.cb_stopbits = QComboBox(self.tab_analyzer)
        self.cb_stopbits.addItem("")
        self.cb_stopbits.addItem("")
        self.cb_stopbits.addItem("")
        self.cb_stopbits.setObjectName(u"cb_stopbits")

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.cb_stopbits)

        self.lb_flow_control = QLabel(self.tab_analyzer)
        self.lb_flow_control.setObjectName(u"lb_flow_control")
        self.lb_flow_control.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lb_flow_control.setAutoFillBackground(False)
        self.lb_flow_control.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.lb_flow_control)

        self.cb_flow_control = QComboBox(self.tab_analyzer)
        self.cb_flow_control.addItem("")
        self.cb_flow_control.addItem("")
        self.cb_flow_control.addItem("")
        self.cb_flow_control.setObjectName(u"cb_flow_control")

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.cb_flow_control)


        self.gridLayout.addLayout(self.formLayout_2, 0, 0, 1, 1)

        self.btnbx_restore_analyzer_default_settings = QDialogButtonBox(self.tab_analyzer)
        self.btnbx_restore_analyzer_default_settings.setObjectName(u"btnbx_restore_analyzer_default_settings")
        self.btnbx_restore_analyzer_default_settings.setStandardButtons(QDialogButtonBox.StandardButton.RestoreDefaults)

        self.gridLayout.addWidget(self.btnbx_restore_analyzer_default_settings, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_analyzer, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.btnbx_save_cancel = QDialogButtonBox(dg_settings)
        self.btnbx_save_cancel.setObjectName(u"btnbx_save_cancel")
        self.btnbx_save_cancel.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)
        self.btnbx_save_cancel.setCenterButtons(False)

        self.verticalLayout.addWidget(self.btnbx_save_cancel)


        self.retranslateUi(dg_settings)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dg_settings)
    # setupUi

    def retranslateUi(self, dg_settings):
        dg_settings.setWindowTitle(QCoreApplication.translate("dg_settings", u"Settings", None))
        self.lb_server_name.setText(QCoreApplication.translate("dg_settings", u"Server Name/IP Address:", None))
        self.lb_port.setText(QCoreApplication.translate("dg_settings", u"Senaite Port:", None))
        self.lb_seiteid.setText(QCoreApplication.translate("dg_settings", u"Site ID:", None))
        self.lb_username.setText(QCoreApplication.translate("dg_settings", u"Senaite Username:", None))
        self.lb_password.setText(QCoreApplication.translate("dg_settings", u"Senaite Password:", None))
        self.pb_test_lims.setText(QCoreApplication.translate("dg_settings", u"Test LIMS", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_senaite_lims), QCoreApplication.translate("dg_settings", u"SENAITE LIMS", None))
        self.lb_analyzer_name.setText(QCoreApplication.translate("dg_settings", u"Analyzer Name:", None))
        self.cb_analyzer_name.setItemText(0, QCoreApplication.translate("dg_settings", u"Select Analyzer", None))
        self.cb_analyzer_name.setItemText(1, QCoreApplication.translate("dg_settings", u"BD BACTEC FX40", None))
        self.cb_analyzer_name.setItemText(2, QCoreApplication.translate("dg_settings", u"COBAS C11", None))
        self.cb_analyzer_name.setItemText(3, QCoreApplication.translate("dg_settings", u"DRI-CHEM NX500", None))
        self.cb_analyzer_name.setItemText(4, QCoreApplication.translate("dg_settings", u"SYSMEX XN-350", None))

        self.cb_analyzer_name.setCurrentText(QCoreApplication.translate("dg_settings", u"Select Analyzer", None))
        self.lb_com_port.setText(QCoreApplication.translate("dg_settings", u"COM Port:", None))
        self.lb_buadrate.setText(QCoreApplication.translate("dg_settings", u"Baudrate:", None))
        self.cb_buadrate.setItemText(0, QCoreApplication.translate("dg_settings", u"50", None))
        self.cb_buadrate.setItemText(1, QCoreApplication.translate("dg_settings", u"75", None))
        self.cb_buadrate.setItemText(2, QCoreApplication.translate("dg_settings", u"110", None))
        self.cb_buadrate.setItemText(3, QCoreApplication.translate("dg_settings", u"134", None))
        self.cb_buadrate.setItemText(4, QCoreApplication.translate("dg_settings", u"150", None))
        self.cb_buadrate.setItemText(5, QCoreApplication.translate("dg_settings", u"200", None))
        self.cb_buadrate.setItemText(6, QCoreApplication.translate("dg_settings", u"300", None))
        self.cb_buadrate.setItemText(7, QCoreApplication.translate("dg_settings", u"600", None))
        self.cb_buadrate.setItemText(8, QCoreApplication.translate("dg_settings", u"1200", None))
        self.cb_buadrate.setItemText(9, QCoreApplication.translate("dg_settings", u"1800", None))
        self.cb_buadrate.setItemText(10, QCoreApplication.translate("dg_settings", u"2400", None))
        self.cb_buadrate.setItemText(11, QCoreApplication.translate("dg_settings", u"4800", None))
        self.cb_buadrate.setItemText(12, QCoreApplication.translate("dg_settings", u"9600", None))
        self.cb_buadrate.setItemText(13, QCoreApplication.translate("dg_settings", u"19200", None))
        self.cb_buadrate.setItemText(14, QCoreApplication.translate("dg_settings", u"38400", None))
        self.cb_buadrate.setItemText(15, QCoreApplication.translate("dg_settings", u"57600", None))
        self.cb_buadrate.setItemText(16, QCoreApplication.translate("dg_settings", u"115200", None))
        self.cb_buadrate.setItemText(17, QCoreApplication.translate("dg_settings", u"230400", None))
        self.cb_buadrate.setItemText(18, QCoreApplication.translate("dg_settings", u"460800", None))
        self.cb_buadrate.setItemText(19, QCoreApplication.translate("dg_settings", u"921600", None))

        self.lb_bytesize.setText(QCoreApplication.translate("dg_settings", u"Bytesize:", None))
        self.cb_bytesize.setItemText(0, QCoreApplication.translate("dg_settings", u"5", None))
        self.cb_bytesize.setItemText(1, QCoreApplication.translate("dg_settings", u"6", None))
        self.cb_bytesize.setItemText(2, QCoreApplication.translate("dg_settings", u"7", None))
        self.cb_bytesize.setItemText(3, QCoreApplication.translate("dg_settings", u"8", None))

        self.lb_parity.setText(QCoreApplication.translate("dg_settings", u"Parity:", None))
        self.cb_parity.setItemText(0, QCoreApplication.translate("dg_settings", u"None", None))
        self.cb_parity.setItemText(1, QCoreApplication.translate("dg_settings", u"Even", None))
        self.cb_parity.setItemText(2, QCoreApplication.translate("dg_settings", u"Odd", None))
        self.cb_parity.setItemText(3, QCoreApplication.translate("dg_settings", u"Mark", None))
        self.cb_parity.setItemText(4, QCoreApplication.translate("dg_settings", u"Space", None))

        self.lb_stopbits.setText(QCoreApplication.translate("dg_settings", u"Stopbits:", None))
        self.cb_stopbits.setItemText(0, QCoreApplication.translate("dg_settings", u"1", None))
        self.cb_stopbits.setItemText(1, QCoreApplication.translate("dg_settings", u"1.5", None))
        self.cb_stopbits.setItemText(2, QCoreApplication.translate("dg_settings", u"2", None))

        self.lb_flow_control.setText(QCoreApplication.translate("dg_settings", u"Flow Control:", None))
        self.cb_flow_control.setItemText(0, QCoreApplication.translate("dg_settings", u"Xon/Xoff", None))
        self.cb_flow_control.setItemText(1, QCoreApplication.translate("dg_settings", u"Hardware", None))
        self.cb_flow_control.setItemText(2, QCoreApplication.translate("dg_settings", u"None", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_analyzer), QCoreApplication.translate("dg_settings", u"ANALYZER", None))
    # retranslateUi

