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
        mainmenu.resize(1106, 750)
        mainmenu.setStyleSheet(_fromUtf8("background-color: rgb(53, 53, 53);"))
        self.gridLayout = QtGui.QGridLayout(mainmenu)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.make_queries_btn = QtGui.QPushButton(mainmenu)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.make_queries_btn.setFont(font)
        self.make_queries_btn.setAutoFillBackground(False)
        self.make_queries_btn.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.make_queries_btn.setObjectName(_fromUtf8("make_queries_btn"))
        self.gridLayout.addWidget(self.make_queries_btn, 6, 0, 1, 1)
        self.mainmenu_lbl = QtGui.QLabel(mainmenu)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Small Fonts"))
        font.setPointSize(13)
        self.mainmenu_lbl.setFont(font)
        self.mainmenu_lbl.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.mainmenu_lbl.setFrameShape(QtGui.QFrame.NoFrame)
        self.mainmenu_lbl.setFrameShadow(QtGui.QFrame.Plain)
        self.mainmenu_lbl.setLineWidth(0)
        self.mainmenu_lbl.setObjectName(_fromUtf8("mainmenu_lbl"))
        self.gridLayout.addWidget(self.mainmenu_lbl, 2, 0, 1, 1)
        self.logo_lbl = QtGui.QLabel(mainmenu)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo_lbl.sizePolicy().hasHeightForWidth())
        self.logo_lbl.setSizePolicy(sizePolicy)
        self.logo_lbl.setMinimumSize(QtCore.QSize(1, 0))
        self.logo_lbl.setMaximumSize(QtCore.QSize(300, 117))
        self.logo_lbl.setSizeIncrement(QtCore.QSize(0, 0))
        self.logo_lbl.setAutoFillBackground(False)
        self.logo_lbl.setFrameShape(QtGui.QFrame.NoFrame)
        self.logo_lbl.setText(_fromUtf8(""))
        self.logo_lbl.setPixmap(QtGui.QPixmap(_fromUtf8("../../../resources/specdata_logo.png")))
        self.logo_lbl.setScaledContents(True)
        self.logo_lbl.setObjectName(_fromUtf8("logo_lbl"))
        self.gridLayout.addWidget(self.logo_lbl, 1, 0, 1, 1)
        self.load_experiment_btn = QtGui.QPushButton(mainmenu)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.load_experiment_btn.setFont(font)
        self.load_experiment_btn.setAutoFillBackground(False)
        self.load_experiment_btn.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.load_experiment_btn.setObjectName(_fromUtf8("load_experiment_btn"))
        self.gridLayout.addWidget(self.load_experiment_btn, 4, 0, 1, 1)
        self.new_experiment_btn = QtGui.QPushButton(mainmenu)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.new_experiment_btn.setFont(font)
        self.new_experiment_btn.setAutoFillBackground(False)
        self.new_experiment_btn.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.new_experiment_btn.setObjectName(_fromUtf8("new_experiment_btn"))
        self.gridLayout.addWidget(self.new_experiment_btn, 3, 0, 1, 1)
        self.import_btn = QtGui.QPushButton(mainmenu)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.import_btn.setFont(font)
        self.import_btn.setAutoFillBackground(False)
        self.import_btn.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.import_btn.setObjectName(_fromUtf8("import_btn"))
        self.gridLayout.addWidget(self.import_btn, 5, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 7, 0, 1, 1)
        self.new_experiment_btn.raise_()
        self.load_experiment_btn.raise_()
        self.logo_lbl.raise_()
        self.logo_lbl.raise_()

        self.retranslateUi(mainmenu)
        QtCore.QMetaObject.connectSlotsByName(mainmenu)

    def retranslateUi(self, mainmenu):
        mainmenu.setWindowTitle(_translate("mainmenu", "Dialog", None))
        self.make_queries_btn.setText(_translate("mainmenu", "Make Queries", None))
        self.mainmenu_lbl.setText(_translate("mainmenu", "Main Menu", None))
        self.load_experiment_btn.setText(_translate("mainmenu", "Load Experiment", None))
        self.new_experiment_btn.setText(_translate("mainmenu", "New Experiment", None))
        self.import_btn.setText(_translate("mainmenu", "Import Files to database", None))

