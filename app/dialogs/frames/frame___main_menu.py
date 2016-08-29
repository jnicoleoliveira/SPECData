# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainmenu.ui'
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

class Ui_mainmenu(object):
    def setupUi(self, mainmenu):
        mainmenu.setObjectName(_fromUtf8("mainmenu"))
        mainmenu.resize(1035, 679)
        mainmenu.setStyleSheet(_fromUtf8("background-color: rgb(53, 53, 53);"))
        self.layoutWidget = QtGui.QWidget(mainmenu)
        self.layoutWidget.setGeometry(QtCore.QRect(310, 270, 421, 301))
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
        self.query_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("8514oem"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.query_lbl.setFont(font)
        self.query_lbl.setAutoFillBackground(False)
        self.query_lbl.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.query_lbl.setFrameShape(QtGui.QFrame.Panel)
        self.query_lbl.setFrameShadow(QtGui.QFrame.Raised)
        self.query_lbl.setLineWidth(6)
        self.query_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.query_lbl.setObjectName(_fromUtf8("query_lbl"))
        self.verticalLayout.addWidget(self.query_lbl)
        self.logo_lbl = QtGui.QLabel(mainmenu)
        self.logo_lbl.setGeometry(QtCore.QRect(340, 100, 361, 131))
        self.logo_lbl.setAutoFillBackground(False)
        self.logo_lbl.setFrameShape(QtGui.QFrame.NoFrame)
        self.logo_lbl.setText(_fromUtf8(""))
        self.logo_lbl.setPixmap(QtGui.QPixmap(_fromUtf8("../../../resources/specdata_logo.png")))
        self.logo_lbl.setScaledContents(True)
        self.logo_lbl.setObjectName(_fromUtf8("logo_lbl"))

        self.retranslateUi(mainmenu)
        QtCore.QMetaObject.connectSlotsByName(mainmenu)

    def retranslateUi(self, mainmenu):
        mainmenu.setWindowTitle(_translate("mainmenu", "Dialog", None))
        self.mainmenu_lbl.setText(_translate("mainmenu", "Main Menu", None))
        self.new_lbl.setText(_translate("mainmenu", "New experiment", None))
        self.load_lbl.setText(_translate("mainmenu", "Load existing experiment", None))
        self.import_lbl.setText(_translate("mainmenu", "Import files to database", None))
        self.query_lbl.setText(_translate("mainmenu", "Make queries", None))

