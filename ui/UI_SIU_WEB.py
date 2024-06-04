# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLayout, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_siu_web(object):
    def setupUi(self, siu_web):
        if not siu_web.objectName():
            siu_web.setObjectName(u"siu_web")
        siu_web.resize(620, 320)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(siu_web.sizePolicy().hasHeightForWidth())
        siu_web.setSizePolicy(sizePolicy)
        siu_web.setMinimumSize(QSize(620, 320))
        siu_web.setMaximumSize(QSize(620, 320))
        self.layoutWidget = QWidget(siu_web)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 20, 576, 281))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.ln_prn = QLineEdit(self.layoutWidget)
        self.ln_prn.setObjectName(u"ln_prn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ln_prn.sizePolicy().hasHeightForWidth())
        self.ln_prn.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(16)
        self.ln_prn.setFont(font)
        self.ln_prn.setMaxLength(15)
        self.ln_prn.setAlignment(Qt.AlignCenter)
        self.ln_prn.setClearButtonEnabled(False)

        self.verticalLayout.addWidget(self.ln_prn)

        self.ln_seat_no = QLineEdit(self.layoutWidget)
        self.ln_seat_no.setObjectName(u"ln_seat_no")
        sizePolicy1.setHeightForWidth(self.ln_seat_no.sizePolicy().hasHeightForWidth())
        self.ln_seat_no.setSizePolicy(sizePolicy1)
        self.ln_seat_no.setFont(font)
        self.ln_seat_no.setMaxLength(6)
        self.ln_seat_no.setFrame(False)
        self.ln_seat_no.setAlignment(Qt.AlignCenter)
        self.ln_seat_no.setPlaceholderText(u"Seat Number")

        self.verticalLayout.addWidget(self.ln_seat_no)

        self.ln_uid = QLineEdit(self.layoutWidget)
        self.ln_uid.setObjectName(u"ln_uid")
        sizePolicy1.setHeightForWidth(self.ln_uid.sizePolicy().hasHeightForWidth())
        self.ln_uid.setSizePolicy(sizePolicy1)
        self.ln_uid.setFont(font)
        self.ln_uid.setMouseTracking(False)
        self.ln_uid.setAlignment(Qt.AlignCenter)
        self.ln_uid.setReadOnly(True)

        self.verticalLayout.addWidget(self.ln_uid)

        self.btn_run = QPushButton(self.layoutWidget)
        self.btn_run.setObjectName(u"btn_run")
        sizePolicy1.setHeightForWidth(self.btn_run.sizePolicy().hasHeightForWidth())
        self.btn_run.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamilies([u"Segoe Script"])
        font1.setPointSize(14)
        self.btn_run.setFont(font1)

        self.verticalLayout.addWidget(self.btn_run)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.lst_credentials = QListWidget(self.layoutWidget)
        __qlistwidgetitem = QListWidgetItem(self.lst_credentials)
        __qlistwidgetitem.setTextAlignment(Qt.AlignCenter);
        self.lst_credentials.setObjectName(u"lst_credentials")
        sizePolicy1.setHeightForWidth(self.lst_credentials.sizePolicy().hasHeightForWidth())
        self.lst_credentials.setSizePolicy(sizePolicy1)
        self.lst_credentials.setMinimumSize(QSize(330, 0))
        font2 = QFont()
        font2.setFamilies([u"Roboto Medium"])
        font2.setPointSize(10)
        self.lst_credentials.setFont(font2)
        self.lst_credentials.setItemAlignment(Qt.AlignHCenter)
        self.lst_credentials.setSortingEnabled(False)

        self.horizontalLayout_2.addWidget(self.lst_credentials)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.te_display_terminal = QTextEdit(self.layoutWidget)
        self.te_display_terminal.setObjectName(u"te_display_terminal")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.te_display_terminal.sizePolicy().hasHeightForWidth())
        self.te_display_terminal.setSizePolicy(sizePolicy2)
        self.te_display_terminal.setMaximumSize(QSize(580, 50))
        font3 = QFont()
        font3.setFamilies([u"Roboto Medium"])
        font3.setPointSize(12)
        self.te_display_terminal.setFont(font3)
        self.te_display_terminal.setReadOnly(True)
        self.te_display_terminal.setAcceptRichText(False)
        self.te_display_terminal.setPlaceholderText(u"")

        self.verticalLayout_2.addWidget(self.te_display_terminal)


        self.retranslateUi(siu_web)

        QMetaObject.connectSlotsByName(siu_web)
    # setupUi

    def retranslateUi(self, siu_web):
        siu_web.setWindowTitle(QCoreApplication.translate("siu_web", u"RESULT GETTER", None))
        self.ln_prn.setPlaceholderText(QCoreApplication.translate("siu_web", u"PRN", None))
        self.ln_uid.setPlaceholderText(QCoreApplication.translate("siu_web", u"Database ID", None))
        self.btn_run.setText(QCoreApplication.translate("siu_web", u"Fetch Result", None))

        __sortingEnabled = self.lst_credentials.isSortingEnabled()
        self.lst_credentials.setSortingEnabled(False)
        ___qlistwidgetitem = self.lst_credentials.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("siu_web", u"-----------------------------------------------------", None));
        self.lst_credentials.setSortingEnabled(__sortingEnabled)

    # retranslateUi

