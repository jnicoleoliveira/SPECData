# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'import_files.ui'
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
        Dialog.resize(1006, 644)
        Dialog.setStyleSheet(_fromUtf8("background-color: rgb(48, 48, 48);\n"
"gridline-color: rgb(195, 195, 195);\n"
"color: rgb(255, 255, 255);\n"
""))
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cancel_btn = QtGui.QPushButton(Dialog)
        self.cancel_btn.setObjectName(_fromUtf8("cancel_btn"))
        self.gridLayout.addWidget(self.cancel_btn, 5, 1, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 1, 1, 4)
        self.remove_btn = QtGui.QPushButton(Dialog)
        self.remove_btn.setObjectName(_fromUtf8("remove_btn"))
        self.gridLayout.addWidget(self.remove_btn, 3, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(11, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 155, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 3, 1, 1)
        self.listWidget = QtGui.QListWidget(Dialog)
        self.listWidget.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);\n"
"color: rgb(25, 25, 25);"))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout.addWidget(self.listWidget, 2, 1, 3, 2)
        spacerItem2 = QtGui.QSpacerItem(263, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 5, 2, 1, 1)
        self.add_btn = QtGui.QPushButton(Dialog)
        self.add_btn.setObjectName(_fromUtf8("add_btn"))
        self.gridLayout.addWidget(self.add_btn, 2, 3, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(11, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 5, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(10, 2, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 0, 1, 1, 1)
        self.accept_btn = QtGui.QPushButton(Dialog)
        self.accept_btn.setStyleSheet(_fromUtf8("background-color: rgba(0, 128, 128, 154);"))
        self.accept_btn.setObjectName(_fromUtf8("accept_btn"))
        self.gridLayout.addWidget(self.accept_btn, 5, 3, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(10, 2, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 6, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.cancel_btn.setText(_translate("Dialog", "Cancel", None))
        self.label.setText(_translate("Dialog", "Choose Files to Import", None))
        self.remove_btn.setText(_translate("Dialog", "-", None))
        self.add_btn.setText(_translate("Dialog", "+", None))
        self.accept_btn.setText(_translate("Dialog", "Accept", None))

