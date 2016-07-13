# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importmenu.ui'
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

class Ui_importmenu_frame(object):
    def setupUi(self, importmenu_frame):
        importmenu_frame.setObjectName(_fromUtf8("importmenu_frame"))
        importmenu_frame.resize(1029, 637)
        importmenu_frame.setStyleSheet(_fromUtf8("background-color: rgb(0, 117, 135);"))
        self.layoutWidget = QtGui.QWidget(importmenu_frame)
        self.layoutWidget.setGeometry(QtCore.QRect(330, 170, 421, 301))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Small Fonts"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.layoutWidget.setFont(font)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.mainmenu_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Small Fonts"))
        font.setPointSize(13)
        self.mainmenu_lbl.setFont(font)
        self.mainmenu_lbl.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.mainmenu_lbl.setFrameShape(QtGui.QFrame.NoFrame)
        self.mainmenu_lbl.setFrameShadow(QtGui.QFrame.Plain)
        self.mainmenu_lbl.setLineWidth(0)
        self.mainmenu_lbl.setObjectName(_fromUtf8("mainmenu_lbl"))
        self.verticalLayout.addWidget(self.mainmenu_lbl)
        self.new_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("8514oem"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.new_lbl.setFont(font)
        self.new_lbl.setAutoFillBackground(False)
        self.new_lbl.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.new_lbl.setFrameShape(QtGui.QFrame.Panel)
        self.new_lbl.setFrameShadow(QtGui.QFrame.Raised)
        self.new_lbl.setLineWidth(6)
        self.new_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.new_lbl.setObjectName(_fromUtf8("new_lbl"))
        self.verticalLayout.addWidget(self.new_lbl)
        self.load_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("8514oem"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.load_lbl.setFont(font)
        self.load_lbl.setAutoFillBackground(False)
        self.load_lbl.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.load_lbl.setFrameShape(QtGui.QFrame.Panel)
        self.load_lbl.setFrameShadow(QtGui.QFrame.Raised)
        self.load_lbl.setLineWidth(6)
        self.load_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.load_lbl.setObjectName(_fromUtf8("load_lbl"))
        self.verticalLayout.addWidget(self.load_lbl)
        self.import_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("8514oem"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.import_lbl.setFont(font)
        self.import_lbl.setAutoFillBackground(False)
        self.import_lbl.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.import_lbl.setFrameShape(QtGui.QFrame.Panel)
        self.import_lbl.setFrameShadow(QtGui.QFrame.Raised)
        self.import_lbl.setLineWidth(6)
        self.import_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.import_lbl.setObjectName(_fromUtf8("import_lbl"))
        self.verticalLayout.addWidget(self.import_lbl)
        self.mainmenu_lbl.raise_()
        self.layoutWidget.raise_()

        self.retranslateUi(importmenu_frame)
        QtCore.QMetaObject.connectSlotsByName(importmenu_frame)

    def retranslateUi(self, importmenu_frame):
        importmenu_frame.setWindowTitle(_translate("importmenu_frame", "Dialog", None))
        self.mainmenu_lbl.setText(_translate("importmenu_frame", "Import Menu", None))
        self.new_lbl.setText(_translate("importmenu_frame", "Import a single file", None))
        self.load_lbl.setText(_translate("importmenu_frame", "Import an entire directory", None))
        self.import_lbl.setText(_translate("importmenu_frame", "Go back", None))

