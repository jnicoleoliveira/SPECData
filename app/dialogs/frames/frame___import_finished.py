# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importfinished.ui'
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

class Ui_importfinished_frame(object):
    def setupUi(self, importfinished_frame):
        importfinished_frame.setObjectName(_fromUtf8("importfinished_frame"))
        importfinished_frame.resize(1051, 671)
        importfinished_frame.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        importfinished_frame.setAutoFillBackground(False)
        importfinished_frame.setStyleSheet(_fromUtf8("background-color: rgb(53, 53, 53);"))
        self.title_lbl = QtGui.QLabel(importfinished_frame)
        self.title_lbl.setGeometry(QtCore.QRect(70, 50, 419, 75))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Small Fonts"))
        font.setPointSize(13)
        self.title_lbl.setFont(font)
        self.title_lbl.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.title_lbl.setFrameShape(QtGui.QFrame.NoFrame)
        self.title_lbl.setFrameShadow(QtGui.QFrame.Plain)
        self.title_lbl.setLineWidth(0)
        self.title_lbl.setObjectName(_fromUtf8("title_lbl"))
        self.return_lbl = QtGui.QLabel(importfinished_frame)
        self.return_lbl.setGeometry(QtCore.QRect(340, 540, 321, 75))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("8514oem"))
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.return_lbl.setFont(font)
        self.return_lbl.setAutoFillBackground(False)
        self.return_lbl.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.return_lbl.setFrameShape(QtGui.QFrame.Panel)
        self.return_lbl.setFrameShadow(QtGui.QFrame.Raised)
        self.return_lbl.setLineWidth(6)
        self.return_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.return_lbl.setOpenExternalLinks(False)
        self.return_lbl.setObjectName(_fromUtf8("return_lbl"))
        self.frame = QtGui.QFrame(importfinished_frame)
        self.frame.setGeometry(QtCore.QRect(59, 121, 941, 401))
        self.frame.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.frame.setFrameShape(QtGui.QFrame.Panel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setLineWidth(5)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.log_list = QtGui.QListWidget(self.frame)
        self.log_list.setGeometry(QtCore.QRect(30, 40, 881, 191))
        self.log_list.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.log_list.setObjectName(_fromUtf8("log_list"))
        self.issuccessful_lbl = QtGui.QLabel(self.frame)
        self.issuccessful_lbl.setGeometry(QtCore.QRect(30, 250, 881, 101))
        self.issuccessful_lbl.setStyleSheet(_fromUtf8("background-color: rgb(4, 78, 110);"))
        self.issuccessful_lbl.setText(_fromUtf8(""))
        self.issuccessful_lbl.setObjectName(_fromUtf8("issuccessful_lbl"))
        self.title_lbl.raise_()
        self.frame.raise_()
        self.return_lbl.raise_()

        self.retranslateUi(importfinished_frame)
        QtCore.QMetaObject.connectSlotsByName(importfinished_frame)

    def retranslateUi(self, importfinished_frame):
        importfinished_frame.setWindowTitle(_translate("importfinished_frame", "Dialog", None))
        self.title_lbl.setText(_translate("importfinished_frame", "Import to database", None))
        self.return_lbl.setText(_translate("importfinished_frame", "Return to menu", None))

