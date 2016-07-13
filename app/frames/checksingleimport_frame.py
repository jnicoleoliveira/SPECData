# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'checksingleimport.ui'
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

class Ui_importsingle_form(object):
    def setupUi(self, importsingle_form):
        importsingle_form.setObjectName(_fromUtf8("importsingle_form"))
        importsingle_form.resize(1034, 669)
        importsingle_form.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        importsingle_form.setAutoFillBackground(False)
        importsingle_form.setStyleSheet(_fromUtf8("background-color: rgb(0, 117, 135);"))
        self.title_lbl = QtGui.QLabel(importsingle_form)
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
        self.finish_lbl = QtGui.QLabel(importsingle_form)
        self.finish_lbl.setGeometry(QtCore.QRect(749, 541, 251, 75))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("8514oem"))
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.finish_lbl.setFont(font)
        self.finish_lbl.setAutoFillBackground(False)
        self.finish_lbl.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.finish_lbl.setFrameShape(QtGui.QFrame.Panel)
        self.finish_lbl.setFrameShadow(QtGui.QFrame.Raised)
        self.finish_lbl.setLineWidth(6)
        self.finish_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.finish_lbl.setOpenExternalLinks(False)
        self.finish_lbl.setObjectName(_fromUtf8("finish_lbl"))
        self.back_lbl = QtGui.QLabel(importsingle_form)
        self.back_lbl.setGeometry(QtCore.QRect(59, 541, 251, 75))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("8514oem"))
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.back_lbl.setFont(font)
        self.back_lbl.setAutoFillBackground(False)
        self.back_lbl.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.back_lbl.setFrameShape(QtGui.QFrame.Panel)
        self.back_lbl.setFrameShadow(QtGui.QFrame.Raised)
        self.back_lbl.setLineWidth(6)
        self.back_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.back_lbl.setOpenExternalLinks(False)
        self.back_lbl.setObjectName(_fromUtf8("back_lbl"))
        self.frame = QtGui.QFrame(importsingle_form)
        self.frame.setGeometry(QtCore.QRect(59, 121, 941, 401))
        self.frame.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.frame.setFrameShape(QtGui.QFrame.Panel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setLineWidth(5)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(60, 70, 451, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.info_tbl = QtGui.QTableView(self.frame)
        self.info_tbl.setGeometry(QtCore.QRect(60, 110, 721, 231))
        self.info_tbl.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.info_tbl.setGridStyle(QtCore.Qt.SolidLine)
        self.info_tbl.setObjectName(_fromUtf8("info_tbl"))
        self.title_lbl.raise_()
        self.frame.raise_()
        self.finish_lbl.raise_()
        self.back_lbl.raise_()

        self.retranslateUi(importsingle_form)
        QtCore.QMetaObject.connectSlotsByName(importsingle_form)

    def retranslateUi(self, importsingle_form):
        importsingle_form.setWindowTitle(_translate("importsingle_form", "Dialog", None))
        self.title_lbl.setText(_translate("importsingle_form", "Import Single File", None))
        self.finish_lbl.setText(_translate("importsingle_form", "Finish", None))
        self.back_lbl.setText(_translate("importsingle_form", "Back", None))
        self.label_2.setText(_translate("importsingle_form", "Is this the data you want imported?", None))

