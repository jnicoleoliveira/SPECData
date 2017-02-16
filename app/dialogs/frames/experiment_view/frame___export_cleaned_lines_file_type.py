# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export_cleaned_lines_file_type.ui'
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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(257, 355)
        Dialog.setStyleSheet(_fromUtf8("background-color: rgb(48, 48, 48);\n"
                                       "gridline-color: rgb(195, 195, 195);\n"
                                       "color: rgb(255, 255, 255);\n"
                                       ""))
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.ok_btn = QtGui.QPushButton(self.frame)
        self.ok_btn.setStyleSheet(_fromUtf8("background-color: rgba(0, 128, 128, 154);"))
        self.ok_btn.setObjectName(_fromUtf8("ok_btn"))
        self.horizontalLayout_2.addWidget(self.ok_btn)
        self.cancel_btn = QtGui.QPushButton(self.frame)
        self.cancel_btn.setStyleSheet(_fromUtf8(""))
        self.cancel_btn.setObjectName(_fromUtf8("cancel_btn"))
        self.horizontalLayout_2.addWidget(self.cancel_btn)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.gridLayout.addWidget(self.frame, 4, 0, 1, 1)
        self.frame_6 = QtGui.QFrame(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setMinimumSize(QtCore.QSize(0, 58))
        self.frame_6.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_6.setObjectName(_fromUtf8("frame_6"))
        self.label_3 = QtGui.QLabel(self.frame_6)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 821, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(_fromUtf8("color: rgb(163, 163, 163);"))
        self.label_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_3.setFrameShadow(QtGui.QFrame.Raised)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.frame_6)
        self.label_4.setGeometry(QtCore.QRect(10, 30, 441, 21))
        self.label_4.setStyleSheet(_fromUtf8("color: rgb(163, 163, 163);"))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.frame_6, 0, 0, 1, 1)
        self.additional_options_frame = QtGui.QFrame(Dialog)
        self.additional_options_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.additional_options_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.additional_options_frame.setObjectName(_fromUtf8("additional_options_frame"))
        self.gridLayout_3 = QtGui.QGridLayout(self.additional_options_frame)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_6 = QtGui.QLabel(self.additional_options_frame)
        self.label_6.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.additional_options_frame, 3, 0, 1, 1)
        self.frame_3 = QtGui.QFrame(Dialog)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame_3)
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.format_cmbobx = QtGui.QComboBox(self.frame_3)
        self.format_cmbobx.setObjectName(_fromUtf8("format_cmbobx"))
        self.gridLayout_2.addWidget(self.format_cmbobx, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.frame_3)
        self.label_5.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_3, 2, 0, 1, 1)
        self.frame_2 = QtGui.QFrame(Dialog)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(self.frame_2)
        self.label_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.type_cmbobx = QtGui.QComboBox(self.frame_2)
        self.type_cmbobx.setObjectName(_fromUtf8("type_cmbobx"))
        self.verticalLayout.addWidget(self.type_cmbobx)
        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)
        self.frame_6.raise_()
        self.frame.raise_()
        self.frame_2.raise_()
        self.frame_3.raise_()
        self.additional_options_frame.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.ok_btn.setText(_translate("Dialog", "OK", None))
        self.cancel_btn.setText(_translate("Dialog", "Cancel", None))
        self.label_3.setText(_translate("Dialog", "Choose Export Type", None))
        self.label_4.setText(_translate("Dialog", "Choose your file type, and format. Click \'OK\' to accept.", None))
        self.label_6.setText(_translate("Dialog", "Additional Options:", None))
        self.label_5.setText(_translate("Dialog", "Choose a format:", None))
        self.label_2.setText(_translate("Dialog", "Choose a file type:", None))
