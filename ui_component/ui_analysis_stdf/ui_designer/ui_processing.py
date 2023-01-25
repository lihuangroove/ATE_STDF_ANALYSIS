# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'processing.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1110, 657)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.groupBox_2 = QGroupBox(self.splitter)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.listView_3 = QListView(self.groupBox_2)
        self.listView_3.setObjectName(u"listView_3")

        self.verticalLayout_2.addWidget(self.listView_3)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.radioButton = QRadioButton(self.groupBox_2)
        self.radioButton.setObjectName(u"radioButton")

        self.verticalLayout_2.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.groupBox_2)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setChecked(True)

        self.verticalLayout_2.addWidget(self.radioButton_2)

        self.listView_2 = QListView(self.groupBox_2)
        self.listView_2.setObjectName(u"listView_2")
        self.listView_2.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_2.addWidget(self.listView_2)

        self.listView = QListView(self.groupBox_2)
        self.listView.setObjectName(u"listView")
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout_2.addWidget(self.listView)

        self.pushButton = QPushButton(self.groupBox_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(False)

        self.verticalLayout_2.addWidget(self.pushButton)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(3, 1)
        self.verticalLayout_2.setStretch(4, 1)
        self.verticalLayout_2.setStretch(5, 3)
        self.splitter.addWidget(self.groupBox_2)
        self.groupBox = QGroupBox(self.splitter)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.splitter.addWidget(self.groupBox)

        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Processing Report", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u5236\u7a0b\u80fd\u529b\u62a5\u544a", None))
        self.label.setText(QCoreApplication.translate("Form", u"DATA\u7c7b\u578b", None))
        self.radioButton.setText(QCoreApplication.translate("Form", u"Diff\u5dee\u5f02\u62a5\u544a(\u9009\u53d65%-95%\u6570\u636e\u533a\u95f4)", None))
        self.radioButton_2.setText(QCoreApplication.translate("Form", u"Value\u503c\u62a5\u544a(\u4ec5\u8ba1\u7b97PASSDIE)", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u5bfc\u51fa\u4e3aExcel", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u5236\u7a0b\u80fd\u529bTable", None))
    # retranslateUi

