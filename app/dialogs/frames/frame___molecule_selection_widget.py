# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'molecule_selection_widget.ui'
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

class Ui_ScrollArea(object):
    def setupUi(self, ScrollArea):
        ScrollArea.setObjectName(_fromUtf8("ScrollArea"))
        ScrollArea.resize(379, 737)
        ScrollArea.setStyleSheet(_fromUtf8("background-color: rgb(48, 48, 48);\n"
"gridline-color: rgb(195, 195, 195);\n"
"color: rgb(255, 255, 255);\n"
""))
        #ScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 375, 733))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayoutWidget = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 341, 711))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        #ScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(ScrollArea)
        QtCore.QMetaObject.connectSlotsByName(ScrollArea)

    def retranslateUi(self, ScrollArea):
        ScrollArea.setWindowTitle(_translate("ScrollArea", "ScrollArea", None))

