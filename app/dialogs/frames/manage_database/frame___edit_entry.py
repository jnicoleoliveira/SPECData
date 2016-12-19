# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_entry.ui'
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
        Dialog.resize(576, 626)
        Dialog.setStyleSheet(_fromUtf8("background-color: rgb(48, 48, 48);\n"
"color: rgb(255, 255, 255);"))
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 4, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.gridLayout_2.addItem(spacerItem1, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 2, 0, 1, 1)
        self.table_widget = QtGui.QTableWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_widget.sizePolicy().hasHeightForWidth())
        self.table_widget.setSizePolicy(sizePolicy)
        self.table_widget.setStyleSheet(_fromUtf8(""))
        self.table_widget.setObjectName(_fromUtf8("table_widget"))
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)
        self.gridLayout_2.addWidget(self.table_widget, 2, 1, 1, 3)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem3 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.composition_txt = QtGui.QLineEdit(Dialog)
        self.composition_txt.setText(_fromUtf8(""))
        self.composition_txt.setObjectName(_fromUtf8("composition_txt"))
        self.horizontalLayout_3.addWidget(self.composition_txt)
        self.composition_btn = QtGui.QToolButton(Dialog)
        self.composition_btn.setObjectName(_fromUtf8("composition_btn"))
        self.horizontalLayout_3.addWidget(self.composition_btn)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.file_txt = QtGui.QLineEdit(Dialog)
        self.file_txt.setObjectName(_fromUtf8("file_txt"))
        self.horizontalLayout_4.addWidget(self.file_txt)
        self.file_btn = QtGui.QToolButton(Dialog)
        self.file_btn.setObjectName(_fromUtf8("file_btn"))
        self.horizontalLayout_4.addWidget(self.file_btn)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 0, 1, 1)
        self.full_rdio = QtGui.QRadioButton(Dialog)
        self.full_rdio.setObjectName(_fromUtf8("full_rdio"))
        self.gridLayout.addWidget(self.full_rdio, 0, 1, 1, 1)
        self.peak_rdio = QtGui.QRadioButton(Dialog)
        self.peak_rdio.setObjectName(_fromUtf8("peak_rdio"))
        self.gridLayout.addWidget(self.peak_rdio, 1, 1, 1, 1)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.gridLayout)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem5 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.exit_btn = QtGui.QPushButton(Dialog)
        self.exit_btn.setObjectName(_fromUtf8("exit_btn"))
        self.horizontalLayout.addWidget(self.exit_btn)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.save_btn = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_btn.sizePolicy().hasHeightForWidth())
        self.save_btn.setSizePolicy(sizePolicy)
        self.save_btn.setStyleSheet(_fromUtf8("background-color: rgb(1, 133, 116);"))
        self.save_btn.setObjectName(_fromUtf8("save_btn"))
        self.horizontalLayout.addWidget(self.save_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_2.addLayout(self.verticalLayout, 3, 1, 1, 3)
        spacerItem7 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem7, 4, 1, 1, 1)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem8, 1, 2, 1, 1)
        self.delete_btn = QtGui.QToolButton(Dialog)
        self.delete_btn.setText(_fromUtf8(""))
        self.delete_btn.setIconSize(QtCore.QSize(20, 20))
        self.delete_btn.setAutoRaise(True)
        self.delete_btn.setObjectName(_fromUtf8("delete_btn"))
        self.gridLayout_2.addWidget(self.delete_btn, 1, 3, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        Dialog.setAccessibleDescription(_translate("Dialog", "Remove this entry", None))
        self.label.setText(_translate("Dialog", "Update composition", None))
        self.composition_btn.setText(_translate("Dialog", "...", None))
        self.label_2.setText(_translate("Dialog", "Upload new data", None))
        self.file_txt.setText(_translate("Dialog", " ", None))
        self.file_btn.setText(_translate("Dialog", "...", None))
        self.full_rdio.setText(_translate("Dialog", "Full spectrum", None))
        self.peak_rdio.setText(_translate("Dialog", "Peaks", None))
        self.exit_btn.setText(_translate("Dialog", "Exit", None))
        self.save_btn.setText(_translate("Dialog", "Save Changes", None))
        self.delete_btn.setWhatsThis(_translate("Dialog", "<html><head/><body><p>Delete this entry</p></body></html>", None))

