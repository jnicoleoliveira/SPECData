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
        Form.resize(874, 579)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
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
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 1, 1, 1)
        self.options_grpbox = QtGui.QGroupBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.options_grpbox.sizePolicy().hasHeightForWidth())
        self.options_grpbox.setSizePolicy(sizePolicy)
        self.options_grpbox.setObjectName(_fromUtf8("options_grpbox"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.options_grpbox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 341, 79))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.options_layout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.options_layout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.options_layout.setObjectName(_fromUtf8("options_layout"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.full_spectrum_chk = QtGui.QCheckBox(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.full_spectrum_chk.setFont(font)
        self.full_spectrum_chk.setObjectName(_fromUtf8("full_spectrum_chk"))
        self.verticalLayout_3.addWidget(self.full_spectrum_chk)
        self.color_experiment_chk = QtGui.QCheckBox(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.color_experiment_chk.setFont(font)
        self.color_experiment_chk.setObjectName(_fromUtf8("color_experiment_chk"))
        self.verticalLayout_3.addWidget(self.color_experiment_chk)
        self.options_layout.addLayout(self.verticalLayout_3)
        self.line_2 = QtGui.QFrame(self.horizontalLayoutWidget)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.options_layout.addWidget(self.line_2)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.sharey_chk = QtGui.QCheckBox(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.sharey_chk.setFont(font)
        self.sharey_chk.setObjectName(_fromUtf8("sharey_chk"))
        self.verticalLayout_2.addWidget(self.sharey_chk)
        self.y_exp_intensities_chk = QtGui.QCheckBox(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.y_exp_intensities_chk.setFont(font)
        self.y_exp_intensities_chk.setObjectName(_fromUtf8("y_exp_intensities_chk"))
        self.verticalLayout_2.addWidget(self.y_exp_intensities_chk)
        self.options_layout.addLayout(self.verticalLayout_2)
        self.gridLayout.addWidget(self.options_grpbox, 3, 1, 1, 2)
        self.view_grpbox = QtGui.QGroupBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view_grpbox.sizePolicy().hasHeightForWidth())
        self.view_grpbox.setSizePolicy(sizePolicy)
        self.view_grpbox.setObjectName(_fromUtf8("view_grpbox"))
        self.gridLayoutWidget = QtGui.QWidget(self.view_grpbox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 341, 142))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.view_layout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.view_layout.setVerticalSpacing(0)
        self.view_layout.setObjectName(_fromUtf8("view_layout"))
        self.show_invalid_btn = QtGui.QPushButton(self.gridLayoutWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../../resources/show-validations.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_invalid_btn.setIcon(icon)
        self.show_invalid_btn.setObjectName(_fromUtf8("show_invalid_btn"))
        self.view_layout.addWidget(self.show_invalid_btn, 4, 1, 1, 1)
        self.show_pending_btn = QtGui.QPushButton(self.gridLayoutWidget)
        self.show_pending_btn.setIcon(icon)
        self.show_pending_btn.setObjectName(_fromUtf8("show_pending_btn"))
        self.view_layout.addWidget(self.show_pending_btn, 2, 1, 1, 1)
        self.show_validations_btn = QtGui.QPushButton(self.gridLayoutWidget)
        self.show_validations_btn.setIcon(icon)
        self.show_validations_btn.setObjectName(_fromUtf8("show_validations_btn"))
        self.view_layout.addWidget(self.show_validations_btn, 3, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.view_layout.addItem(spacerItem1, 2, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.view_layout.addItem(spacerItem2, 2, 2, 1, 1)
        self.gridLayout.addWidget(self.view_grpbox, 2, 1, 1, 2)
        self.matches_selections_grpbox = QtGui.QGroupBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.matches_selections_grpbox.sizePolicy().hasHeightForWidth())
        self.matches_selections_grpbox.setSizePolicy(sizePolicy)
        self.matches_selections_grpbox.setObjectName(_fromUtf8("matches_selections_grpbox"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.matches_selections_grpbox)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(130, 60, 330, 144))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.matches_layout = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.matches_layout.setSpacing(0)
        self.matches_layout.setObjectName(_fromUtf8("matches_layout"))
        self.redisplay_btn = QtGui.QPushButton(self.gridLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.redisplay_btn.sizePolicy().hasHeightForWidth())
        self.redisplay_btn.setSizePolicy(sizePolicy)
        self.redisplay_btn.setMaximumSize(QtCore.QSize(100, 100))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../../resources/redisplay-__setup_graph.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.redisplay_btn.setIcon(icon1)
        self.redisplay_btn.setFlat(False)
        self.redisplay_btn.setObjectName(_fromUtf8("redisplay_btn"))
        self.matches_layout.addWidget(self.redisplay_btn, 0, 0, 1, 1)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.select_all_btn = QtGui.QPushButton(self.gridLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_all_btn.sizePolicy().hasHeightForWidth())
        self.select_all_btn.setSizePolicy(sizePolicy)
        self.select_all_btn.setMinimumSize(QtCore.QSize(100, 0))
        self.select_all_btn.setMaximumSize(QtCore.QSize(100, 16777215))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("../../../resources/select-all.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.select_all_btn.setIcon(icon2)
        self.select_all_btn.setObjectName(_fromUtf8("select_all_btn"))
        self.verticalLayout.addWidget(self.select_all_btn)
        self.deselect_all_btn = QtGui.QPushButton(self.gridLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deselect_all_btn.sizePolicy().hasHeightForWidth())
        self.deselect_all_btn.setSizePolicy(sizePolicy)
        self.deselect_all_btn.setMinimumSize(QtCore.QSize(100, 0))
        self.deselect_all_btn.setMaximumSize(QtCore.QSize(100, 16777215))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("../../../resources/deselect-all.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deselect_all_btn.setIcon(icon3)
        self.deselect_all_btn.setObjectName(_fromUtf8("deselect_all_btn"))
        self.verticalLayout.addWidget(self.deselect_all_btn)
        self.verticalLayout_5.addLayout(self.verticalLayout)
        self.matches_layout.addLayout(self.verticalLayout_5, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.matches_selections_grpbox, 1, 1, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(50, 50, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 3, 1, 1)
        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 0, 2, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 4, 1, 1, 1)
        self.options_grpbox.raise_()
        self.matches_selections_grpbox.raise_()
        self.line.raise_()
        self.view_grpbox.raise_()
        self.gridLayoutWidget_2.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.options_grpbox.setTitle(_translate("Form", "Options", None))
        self.label.setText(_translate("Form", "Experiment", None))
        self.full_spectrum_chk.setText(_translate("Form", "Plot full spectrum", None))
        self.color_experiment_chk.setText(_translate("Form", "Color peak assignments", None))
        self.label_2.setText(_translate("Form", "Matches ", None))
        self.sharey_chk.setText(_translate("Form", "Share Experiment y-axis", None))
        self.y_exp_intensities_chk.setText(_translate("Form", "Set y to experiment intensities", None))
        self.view_grpbox.setTitle(_translate("Form", "View", None))
        self.show_invalid_btn.setText(_translate("Form", "Show Invalid Lines", None))
        self.show_pending_btn.setText(_translate("Form", "Show Pending", None))
        self.show_validations_btn.setText(_translate("Form", "Show Validations", None))
        self.matches_selections_grpbox.setTitle(_translate("Form", "Matches Selection", None))
        self.redisplay_btn.setText(_translate("Form", "Redisplay", None))
        self.select_all_btn.setText(_translate("Form", "Select All", None))
        self.deselect_all_btn.setText(_translate("Form", "Deselect All", None))

