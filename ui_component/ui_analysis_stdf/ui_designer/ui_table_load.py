# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'table_load.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import pyqtsource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1221, 503)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(True)

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setEnabled(True)

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_5 = QPushButton(Form)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_2.addWidget(self.pushButton_5)

        self.pushButton_4 = QPushButton(Form)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setEnabled(True)

        self.horizontalLayout_2.addWidget(self.pushButton_4)

        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.setObjectName(u"pushButton_3")
        icon = QIcon()
        icon.addFile(u":/pyqt/source/images/lc_recsearch.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_3.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.checkBox = QCheckBox(Form)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_2.addWidget(self.checkBox)

        self.progressBar = QProgressBar(Form)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximumSize(QSize(100, 16777215))
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.horizontalLayout_2.addWidget(self.progressBar)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u6539\u53d8Limit\u540e\u91cd\u7b97Rate", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"\u53ea\u770b\u9009\u4e2d\u9879\u76eePASS\u6570\u636e", None))
        self.pushButton_5.setText(QCoreApplication.translate("Form", u"\u53ea\u770b\u9009\u4e2d\u9879\u76eeFAIL\u6570\u636e", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"\u5bf9\u9009\u4e2d\u9879\u76ee\u5206\u6790", None))
        self.pushButton_3.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"\u56de\u8f66\u7b5b\u9009", None))
        self.checkBox.setText(QCoreApplication.translate("Form", u"Top Fail \u663e\u793a", None))
    # retranslateUi

