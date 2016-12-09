# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selected_element_box.ui'
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
        Form.resize(86, 110)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(50, 60))
        Form.setMaximumSize(QtCore.QSize(100, 110))
        Form.setAutoFillBackground(False)
        Form.setStyleSheet(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.blank_lbl = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blank_lbl.sizePolicy().hasHeightForWidth())
        self.blank_lbl.setSizePolicy(sizePolicy)
        self.blank_lbl.setMaximumSize(QtCore.QSize(16777215, 11))
        self.blank_lbl.setStyleSheet(_fromUtf8("background-color: rgb(255, 82, 168);"))
        self.blank_lbl.setText(_fromUtf8(""))
        self.blank_lbl.setObjectName(_fromUtf8("blank_lbl"))
        self.horizontalLayout_2.addWidget(self.blank_lbl)
        self.close_btn = QtGui.QToolButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_btn.sizePolicy().hasHeightForWidth())
        self.close_btn.setSizePolicy(sizePolicy)
        self.close_btn.setMaximumSize(QtCore.QSize(20, 11))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.close_btn.setFont(font)
        self.close_btn.setStyleSheet(_fromUtf8("background-color: rgb(255, 82, 168);\n"
"color: rgb(0, 0, 0);"))
        self.close_btn.setAutoRaise(True)
        self.close_btn.setObjectName(_fromUtf8("close_btn"))
        self.horizontalLayout_2.addWidget(self.close_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.symbol_lbl = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.symbol_lbl.sizePolicy().hasHeightForWidth())
        self.symbol_lbl.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.symbol_lbl.setFont(font)
        self.symbol_lbl.setStyleSheet(_fromUtf8("background-color: rgb(255, 82, 168);"))
        self.symbol_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.symbol_lbl.setObjectName(_fromUtf8("symbol_lbl"))
        self.verticalLayout.addWidget(self.symbol_lbl)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.spinBox = QtGui.QSpinBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy)
        self.spinBox.setStyleSheet(_fromUtf8(""))
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.horizontalLayout.addWidget(self.spinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.close_btn.setText(_translate("Form", "x", None))
        self.symbol_lbl.setText(_translate("Form", "N", None))

