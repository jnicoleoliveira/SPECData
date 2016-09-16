# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_graph_options.ui'
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
        Form.resize(127, 149)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setStyleSheet(_fromUtf8("background-color: rgb(48, 48, 48);\n"
"gridline-color: rgb(195, 195, 195);\n"
"color: rgb(255, 255, 255);\n"
""))
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(_fromUtf8(""))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.full_spectrum_chk = QtGui.QCheckBox(Form)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.full_spectrum_chk.setFont(font)
        self.full_spectrum_chk.setObjectName(_fromUtf8("full_spectrum_chk"))
        self.verticalLayout.addWidget(self.full_spectrum_chk)
        self.color_experiment_chk = QtGui.QCheckBox(Form)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.color_experiment_chk.setFont(font)
        self.color_experiment_chk.setObjectName(_fromUtf8("color_experiment_chk"))
        self.verticalLayout.addWidget(self.color_experiment_chk)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.line_2 = QtGui.QFrame(Form)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.sharey_chk = QtGui.QCheckBox(Form)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.sharey_chk.setFont(font)
        self.sharey_chk.setObjectName(_fromUtf8("sharey_chk"))
        self.verticalLayout_2.addWidget(self.sharey_chk)
        self.y_exp_intensities_chk = QtGui.QCheckBox(Form)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.y_exp_intensities_chk.setFont(font)
        self.y_exp_intensities_chk.setObjectName(_fromUtf8("y_exp_intensities_chk"))
        self.verticalLayout_2.addWidget(self.y_exp_intensities_chk)
        self.gridLayout.addLayout(self.verticalLayout_2, 4, 0, 1, 1)
        self.label_3.raise_()
        self.line.raise_()
        self.label_2.raise_()
        self.line_2.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_3.setText(_translate("Form", "Graph Options", None))
        self.label.setText(_translate("Form", "Experiment", None))
        self.full_spectrum_chk.setText(_translate("Form", "Plot full spectrum", None))
        self.color_experiment_chk.setText(_translate("Form", "Color peak assignments", None))
        self.label_2.setText(_translate("Form", "Matches ", None))
        self.sharey_chk.setText(_translate("Form", "Share Experiment y-axis", None))
        self.y_exp_intensities_chk.setText(_translate("Form", "Set y to experiment intensities", None))

