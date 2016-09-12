# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assignment_info_widget.ui'
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
        Form.resize(501, 233)
        Form.setStyleSheet(_fromUtf8("background-color: rgb(48, 48, 48);\n"
"gridline-color: rgb(195, 195, 195);\n"
"color: rgb(255, 255, 255);\n"
""))
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.Title = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Title.setFont(font)
        self.Title.setFrameShadow(QtGui.QFrame.Raised)
        self.Title.setObjectName(_fromUtf8("Title"))
        self.verticalLayout.addWidget(self.Title)
        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.experiment_name_lbl = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.experiment_name_lbl.setFont(font)
        self.experiment_name_lbl.setObjectName(_fromUtf8("experiment_name_lbl"))
        self.verticalLayout.addWidget(self.experiment_name_lbl)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.total_peaks_lbl = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.total_peaks_lbl.setFont(font)
        self.total_peaks_lbl.setObjectName(_fromUtf8("total_peaks_lbl"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.total_peaks_lbl)
        self.total_peaks_val = QtGui.QLabel(Form)
        self.total_peaks_val.setObjectName(_fromUtf8("total_peaks_val"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.total_peaks_val)
        self.peaks_assigned_lbl = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.peaks_assigned_lbl.setFont(font)
        self.peaks_assigned_lbl.setObjectName(_fromUtf8("peaks_assigned_lbl"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.peaks_assigned_lbl)
        self.peaks_assigned_val = QtGui.QLabel(Form)
        self.peaks_assigned_val.setObjectName(_fromUtf8("peaks_assigned_val"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.peaks_assigned_val)
        self.presence_lbl = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.presence_lbl.setFont(font)
        self.presence_lbl.setObjectName(_fromUtf8("presence_lbl"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.presence_lbl)
        self.presence_val_lbl = QtGui.QLabel(Form)
        self.presence_val_lbl.setObjectName(_fromUtf8("presence_val_lbl"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.presence_val_lbl)
        self.info_val_lbl = QtGui.QLabel(Form)
        self.info_val_lbl.setObjectName(_fromUtf8("info_val_lbl"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.info_val_lbl)
        self.info_lbl = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.info_lbl.setFont(font)
        self.info_lbl.setObjectName(_fromUtf8("info_lbl"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.info_lbl)
        self.verticalLayout_2.addLayout(self.formLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.Title.setText(_translate("Form", "Individual Match View", None))
        self.experiment_name_lbl.setText(_translate("Form", "molecule name here", None))
        self.total_peaks_lbl.setText(_translate("Form", "Total Peaks:", None))
        self.total_peaks_val.setText(_translate("Form", "TextLabel", None))
        self.peaks_assigned_lbl.setText(_translate("Form", "Peaks Assigned:", None))
        self.peaks_assigned_val.setText(_translate("Form", "TextLabel", None))
        self.presence_lbl.setText(_translate("Form", "Chance of Presence (P):", None))
        self.presence_val_lbl.setText(_translate("Form", "TextLabel", None))
        self.info_val_lbl.setText(_translate("Form", "TextLabel", None))
        self.info_lbl.setText(_translate("Form", "Additional Info:", None))

