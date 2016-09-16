# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'load_experiment.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1064, 732)
        Dialog.setStyleSheet(_fromUtf8("background-color: rgb(48, 48, 48);\n"
"gridline-color: rgb(195, 195, 195);\n"
"color: rgb(255, 255, 255);\n"
""))
        self.gridLayout_4 = QtGui.QGridLayout(Dialog)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        spacerItem = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 1, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.listWidget = QtGui.QListWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);\n"
"color: rgb(25, 25, 25);"))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout.addWidget(self.listWidget, 3, 0, 1, 1)
        self.title_lbl = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Droid Sans"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.title_lbl.setFont(font)
        self.title_lbl.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"font: 75 12pt \"Droid Sans\";"))
        self.title_lbl.setFrameShape(QtGui.QFrame.StyledPanel)
        self.title_lbl.setObjectName(_fromUtf8("title_lbl"))
        self.gridLayout.addWidget(self.title_lbl, 1, 0, 1, 1)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 1, 1, 1, 1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.back_btn = QtGui.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DEC Terminal"))
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.back_btn.setFont(font)
        self.back_btn.setAutoFillBackground(False)
        self.back_btn.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"background-color: rgb(48, 48, 48);"))
        self.back_btn.setCheckable(False)
        self.back_btn.setAutoDefault(True)
        self.back_btn.setDefault(False)
        self.back_btn.setFlat(False)
        self.back_btn.setObjectName(_fromUtf8("back_btn"))
        self.gridLayout_3.addWidget(self.back_btn, 0, 0, 1, 1)
        self.load_btn = QtGui.QPushButton(Dialog)
        self.load_btn.setAutoFillBackground(False)
        self.load_btn.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"background-color: rgb(48, 48, 48);"))
        self.load_btn.setCheckable(False)
        self.load_btn.setAutoDefault(True)
        self.load_btn.setDefault(False)
        self.load_btn.setFlat(False)
        self.load_btn.setObjectName(_fromUtf8("load_btn"))
        self.gridLayout_3.addWidget(self.load_btn, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 2, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.gridLayout_4.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem3, 3, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.title_lbl.setText(_translate("Dialog", "Choose an experiment:", None))
        self.back_btn.setText(_translate("Dialog", "Back to Main", None))
        self.load_btn.setText(_translate("Dialog", "Load", None))

