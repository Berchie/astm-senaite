# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ASTM_Middleware.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QHeaderView,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QTextEdit, QVBoxLayout, QWidget)
import Icons_rc

class Ui_astm_middleware(object):
    def setupUi(self, astm_middleware):
        if not astm_middleware.objectName():
            astm_middleware.setObjectName(u"astm_middleware")
        astm_middleware.resize(744, 835)
        icon = QIcon()
        icon.addFile(u":/Main/port.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        astm_middleware.setWindowIcon(icon)
        self.verticalLayout_3 = QVBoxLayout(astm_middleware)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_start_listener = QPushButton(astm_middleware)
        self.btn_start_listener.setObjectName(u"btn_start_listener")
        font = QFont()
        font.setPointSize(10)
        self.btn_start_listener.setFont(font)
        self.btn_start_listener.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/Buttons/icons8-connected-94.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_start_listener.setIcon(icon1)
        self.btn_start_listener.setIconSize(QSize(50, 50))
        self.btn_start_listener.setFlat(False)

        self.horizontalLayout.addWidget(self.btn_start_listener)

        self.btn_stop_listener = QPushButton(astm_middleware)
        self.btn_stop_listener.setObjectName(u"btn_stop_listener")
        self.btn_stop_listener.setFont(font)
        self.btn_stop_listener.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/Buttons/icons8-disconnected-94.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_stop_listener.setIcon(icon2)
        self.btn_stop_listener.setIconSize(QSize(50, 50))

        self.horizontalLayout.addWidget(self.btn_stop_listener)

        self.btn_settings = QPushButton(astm_middleware)
        self.btn_settings.setObjectName(u"btn_settings")
        self.btn_settings.setFont(font)
        self.btn_settings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/Buttons/icons8-settings-375.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_settings.setIcon(icon3)
        self.btn_settings.setIconSize(QSize(50, 50))

        self.horizontalLayout.addWidget(self.btn_settings)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.table_layout = QVBoxLayout()
        self.table_layout.setSpacing(20)
        self.table_layout.setObjectName(u"table_layout")
        self.table_layout.setContentsMargins(-1, 20, -1, -1)
        self.gb_sqlite_view_data_table = QGroupBox(astm_middleware)
        self.gb_sqlite_view_data_table.setObjectName(u"gb_sqlite_view_data_table")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setKerning(True)
        self.gb_sqlite_view_data_table.setFont(font1)
        self.sqlite_db_table_layout = QVBoxLayout(self.gb_sqlite_view_data_table)
        self.sqlite_db_table_layout.setObjectName(u"sqlite_db_table_layout")
        self.sqlite_data_table = QTableWidget(self.gb_sqlite_view_data_table)
        if (self.sqlite_data_table.columnCount() < 4):
            self.sqlite_data_table.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.sqlite_data_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.sqlite_data_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.sqlite_data_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.sqlite_data_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.sqlite_data_table.setObjectName(u"sqlite_data_table")
        self.sqlite_data_table.setWordWrap(True)
        self.sqlite_data_table.setColumnCount(4)

        self.sqlite_db_table_layout.addWidget(self.sqlite_data_table)


        self.table_layout.addWidget(self.gb_sqlite_view_data_table)

        self.gb_astm_message = QGroupBox(astm_middleware)
        self.gb_astm_message.setObjectName(u"gb_astm_message")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.gb_astm_message.setFont(font2)
        self.astm_msg_layout = QVBoxLayout(self.gb_astm_message)
        self.astm_msg_layout.setObjectName(u"astm_msg_layout")
        self.astm_msg_textEdit = QTextEdit(self.gb_astm_message)
        self.astm_msg_textEdit.setObjectName(u"astm_msg_textEdit")
        self.astm_msg_textEdit.setReadOnly(True)

        self.astm_msg_layout.addWidget(self.astm_msg_textEdit)


        self.table_layout.addWidget(self.gb_astm_message)


        self.verticalLayout_3.addLayout(self.table_layout)


        self.retranslateUi(astm_middleware)

        self.btn_start_listener.setDefault(False)


        QMetaObject.connectSlotsByName(astm_middleware)
    # setupUi

    def retranslateUi(self, astm_middleware):
        astm_middleware.setWindowTitle(QCoreApplication.translate("astm_middleware", u"Analyzer - ASTM Middleware", None))
        self.btn_start_listener.setText(QCoreApplication.translate("astm_middleware", u"Start Listener", None))
        self.btn_stop_listener.setText(QCoreApplication.translate("astm_middleware", u"Stop Listener", None))
        self.btn_settings.setText(QCoreApplication.translate("astm_middleware", u"Settings", None))
        self.gb_sqlite_view_data_table.setTitle("")
        ___qtablewidgetitem = self.sqlite_data_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("astm_middleware", u"DateTime", None));
        ___qtablewidgetitem1 = self.sqlite_data_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("astm_middleware", u"Analyzer", None));
        ___qtablewidgetitem2 = self.sqlite_data_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("astm_middleware", u"Sample ID", None));
        ___qtablewidgetitem3 = self.sqlite_data_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("astm_middleware", u"Message", None));
        self.gb_astm_message.setTitle(QCoreApplication.translate("astm_middleware", u"ASTM Message from the Analyzer", None))
    # retranslateUi

