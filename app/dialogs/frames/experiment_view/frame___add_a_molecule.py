# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_a_molecule.ui'
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
        Dialog.resize(887, 575)
        Dialog.setStyleSheet(_fromUtf8("background-color: rgb(48, 48, 48);\n"
"gridline-color: rgb(195, 195, 195);\n"
"color: rgb(255, 255, 255);\n"
""))
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
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
        self.label_4.setGeometry(QtCore.QRect(10, 30, 561, 21))
        self.label_4.setStyleSheet(_fromUtf8("color: rgb(163, 163, 163);"))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.frame_6, 0, 0, 1, 1)
        self.frame_2 = QtGui.QFrame(Dialog)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_2 = QtGui.QLabel(self.frame_2)
        self.label_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(self.frame_2)
        self.scrollArea.setStyleSheet(_fromUtf8(""))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 855, 351))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.scrollArea, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.select_all_btn = QtGui.QPushButton(self.frame)
        self.select_all_btn.setObjectName(_fromUtf8("select_all_btn"))
        self.horizontalLayout_3.addWidget(self.select_all_btn)
        self.deselect_all_btn = QtGui.QPushButton(self.frame)
        self.deselect_all_btn.setObjectName(_fromUtf8("deselect_all_btn"))
        self.horizontalLayout_3.addWidget(self.deselect_all_btn)
        self.invert_btn = QtGui.QPushButton(self.frame)
        self.invert_btn.setObjectName(_fromUtf8("invert_btn"))
        self.horizontalLayout_3.addWidget(self.invert_btn)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.ok_btn = QtGui.QPushButton(self.frame)
        self.ok_btn.setStyleSheet(_fromUtf8("background-color: rgba(0, 128, 128, 154);"))
        self.ok_btn.setObjectName(_fromUtf8("ok_btn"))
        self.horizontalLayout_2.addWidget(self.ok_btn)
        self.cancel_btn = QtGui.QPushButton(self.frame)
        self.cancel_btn.setStyleSheet(_fromUtf8(""))
        self.cancel_btn.setObjectName(_fromUtf8("cancel_btn"))
        self.horizontalLayout_2.addWidget(self.cancel_btn)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.gridLayout.addWidget(self.frame, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_3.setText(_translate("Dialog", "Add a Molecule", None))
        self.label_4.setText(_translate("Dialog", "Choose from molecules below to be added to the analysis. Click \'OK\' to accept.", None))
        self.label_2.setText(_translate("Dialog", "Please select molecules to be analysed:", None))
        self.select_all_btn.setText(_translate("Dialog", "Select All", None))
        self.deselect_all_btn.setText(_translate("Dialog", "Deselect All", None))
        self.invert_btn.setText(_translate("Dialog", "Invert", None))
        self.ok_btn.setText(_translate("Dialog", "OK", None))
        self.cancel_btn.setText(_translate("Dialog", "Cancel", None))

