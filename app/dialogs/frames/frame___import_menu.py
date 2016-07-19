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
        importmenu_frame.resize(1029, 684)
        importmenu_frame.setStyleSheet(_fromUtf8("background-color: rgb(53, 53, 53);"))
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
        self.title_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Small Fonts"))
        font.setPointSize(13)
        self.title_lbl.setFont(font)
        self.title_lbl.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.title_lbl.setFrameShape(QtGui.QFrame.NoFrame)
        self.title_lbl.setFrameShadow(QtGui.QFrame.Plain)
        self.title_lbl.setLineWidth(0)
        self.title_lbl.setObjectName(_fromUtf8("title_lbl"))
        self.verticalLayout.addWidget(self.title_lbl)
        self.single_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("8514oem"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.single_lbl.setFont(font)
        self.single_lbl.setAutoFillBackground(False)
        self.single_lbl.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.single_lbl.setFrameShape(QtGui.QFrame.Panel)
        self.single_lbl.setFrameShadow(QtGui.QFrame.Raised)
        self.single_lbl.setLineWidth(6)
        self.single_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.single_lbl.setOpenExternalLinks(False)
        self.single_lbl.setObjectName(_fromUtf8("single_lbl"))
        self.verticalLayout.addWidget(self.single_lbl)
        self.directory_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("8514oem"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.directory_lbl.setFont(font)
        self.directory_lbl.setAutoFillBackground(False)
        self.directory_lbl.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.directory_lbl.setFrameShape(QtGui.QFrame.Panel)
        self.directory_lbl.setFrameShadow(QtGui.QFrame.Raised)
        self.directory_lbl.setLineWidth(6)
        self.directory_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.directory_lbl.setObjectName(_fromUtf8("directory_lbl"))
        self.verticalLayout.addWidget(self.directory_lbl)
        self.goback_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("8514oem"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.goback_lbl.setFont(font)
        self.goback_lbl.setAutoFillBackground(False)
        self.goback_lbl.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.goback_lbl.setFrameShape(QtGui.QFrame.Panel)
        self.goback_lbl.setFrameShadow(QtGui.QFrame.Raised)
        self.goback_lbl.setLineWidth(6)
        self.goback_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.goback_lbl.setObjectName(_fromUtf8("goback_lbl"))
        self.verticalLayout.addWidget(self.goback_lbl)

        self.retranslateUi(importmenu_frame)
        QtCore.QMetaObject.connectSlotsByName(importmenu_frame)

    def retranslateUi(self, importmenu_frame):
        importmenu_frame.setWindowTitle(_translate("importmenu_frame", "Dialog", None))
        self.title_lbl.setText(_translate("importmenu_frame", "Import Menu", None))
        self.single_lbl.setText(_translate("importmenu_frame", "Import a single file", None))
        self.directory_lbl.setText(_translate("importmenu_frame", "Import an entire directory", None))
        self.goback_lbl.setText(_translate("importmenu_frame", "Go back", None))

