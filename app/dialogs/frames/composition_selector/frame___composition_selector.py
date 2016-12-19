# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'composition_selector.ui'
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
        Dialog.resize(896, 507)
        Dialog.setStyleSheet(_fromUtf8("background-color: rgb(48, 48, 48);\n"
"gridline-color: rgb(195, 195, 195);\n"
"color: rgb(255, 255, 255);"))
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.left_frame = QtGui.QFrame(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_frame.sizePolicy().hasHeightForWidth())
        self.left_frame.setSizePolicy(sizePolicy)
        self.left_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.left_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.left_frame.setObjectName(_fromUtf8("left_frame"))
        self.gridLayout.addWidget(self.left_frame, 1, 0, 4, 1)
        self.view_box_frame = QtGui.QFrame(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view_box_frame.sizePolicy().hasHeightForWidth())
        self.view_box_frame.setSizePolicy(sizePolicy)
        self.view_box_frame.setMinimumSize(QtCore.QSize(275, 200))
        self.view_box_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.view_box_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.view_box_frame.setObjectName(_fromUtf8("view_box_frame"))
        self.gridLayout.addWidget(self.view_box_frame, 1, 1, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.accept_btn = QtGui.QPushButton(Dialog)
        self.accept_btn.setStyleSheet(_fromUtf8("background-color: rgba(0, 128, 128, 154);"))
        self.accept_btn.setObjectName(_fromUtf8("accept_btn"))
        self.horizontalLayout_2.addWidget(self.accept_btn)
        self.cancel_btn = QtGui.QPushButton(Dialog)
        self.cancel_btn.setStyleSheet(_fromUtf8(""))
        self.cancel_btn.setObjectName(_fromUtf8("cancel_btn"))
        self.horizontalLayout_2.addWidget(self.cancel_btn)
        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 1, 1, 1)
        self.right_frame = QtGui.QFrame(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.right_frame.sizePolicy().hasHeightForWidth())
        self.right_frame.setSizePolicy(sizePolicy)
        self.right_frame.setMinimumSize(QtCore.QSize(50, 100))
        self.right_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.right_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.right_frame.setObjectName(_fromUtf8("right_frame"))
        self.gridLayout.addWidget(self.right_frame, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Click to add element to your composition:", None))
        self.accept_btn.setText(_translate("Dialog", "Accept", None))
        self.cancel_btn.setText(_translate("Dialog", "Cancel", None))

