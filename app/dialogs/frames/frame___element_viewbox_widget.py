# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'element_viewbox_widget.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(200, 212)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(200, 200))
        Form.setMaximumSize(QtCore.QSize(200, 214))
        Form.setStyleSheet(_fromUtf8("background-color: rgb(48, 48, 48);\n"
"gridline-color: rgb(195, 195, 195);\n"
"color: rgb(255, 255, 255);"))
        self.gridLayout_3 = QtGui.QGridLayout(Form)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.frame = QtGui.QFrame(Form)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        spacerItem1 = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.atomic_number_lbl = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.atomic_number_lbl.setFont(font)
        self.atomic_number_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.atomic_number_lbl.setObjectName(_fromUtf8("atomic_number_lbl"))
        self.horizontalLayout.addWidget(self.atomic_number_lbl)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.boiling_lbl = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.boiling_lbl.setFont(font)
        self.boiling_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.boiling_lbl.setObjectName(_fromUtf8("boiling_lbl"))
        self.horizontalLayout.addWidget(self.boiling_lbl)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.symbol_lbl = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.symbol_lbl.setFont(font)
        self.symbol_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.symbol_lbl.setObjectName(_fromUtf8("symbol_lbl"))
        self.verticalLayout_2.addWidget(self.symbol_lbl)
        self.name_lbl = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.name_lbl.setFont(font)
        self.name_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.name_lbl.setObjectName(_fromUtf8("name_lbl"))
        self.verticalLayout_2.addWidget(self.name_lbl)
        self.atomic_mass_lbl = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.atomic_mass_lbl.setFont(font)
        self.atomic_mass_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.atomic_mass_lbl.setObjectName(_fromUtf8("atomic_mass_lbl"))
        self.verticalLayout_2.addWidget(self.atomic_mass_lbl)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.atomic_number_lbl.setText(_translate("Form", "26", None))
        self.boiling_lbl.setText(_translate("Form", "2861", None))
        self.symbol_lbl.setText(_translate("Form", "Fe", None))
        self.name_lbl.setText(_translate("Form", "Iron", None))
        self.atomic_mass_lbl.setText(_translate("Form", "55.933", None))

