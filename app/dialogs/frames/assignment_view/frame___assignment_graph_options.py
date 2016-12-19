# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assignment_graph_options.ui'
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
        Form.resize(445, 163)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setStyleSheet(_fromUtf8("background-color: rgb(48, 48, 48);\n"
"gridline-color: rgb(195, 195, 195);\n"
"color: rgb(255, 255, 255);\n"
""))
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.matches_selections_grpbox = QtGui.QGroupBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.matches_selections_grpbox.sizePolicy().hasHeightForWidth())
        self.matches_selections_grpbox.setSizePolicy(sizePolicy)
        self.matches_selections_grpbox.setObjectName(_fromUtf8("matches_selections_grpbox"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.matches_selections_grpbox)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 30, 421, 121))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.matches_layout = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.matches_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.matches_layout.setHorizontalSpacing(2)
        self.matches_layout.setObjectName(_fromUtf8("matches_layout"))
        self.options_layout = QtGui.QHBoxLayout()
        self.options_layout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.options_layout.setObjectName(_fromUtf8("options_layout"))
        self.redisplay_btn = QtGui.QPushButton(self.gridLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.redisplay_btn.sizePolicy().hasHeightForWidth())
        self.redisplay_btn.setSizePolicy(sizePolicy)
        self.redisplay_btn.setIconSize(QtCore.QSize(121, 120))
        self.redisplay_btn.setObjectName(_fromUtf8("redisplay_btn"))
        self.options_layout.addWidget(self.redisplay_btn)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label = QtGui.QLabel(self.gridLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.full_spectrum_chk = QtGui.QCheckBox(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.full_spectrum_chk.setFont(font)
        self.full_spectrum_chk.setObjectName(_fromUtf8("full_spectrum_chk"))
        self.verticalLayout_3.addWidget(self.full_spectrum_chk)
        self.color_experiment_chk = QtGui.QCheckBox(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.color_experiment_chk.setFont(font)
        self.color_experiment_chk.setObjectName(_fromUtf8("color_experiment_chk"))
        self.verticalLayout_3.addWidget(self.color_experiment_chk)
        self.options_layout.addLayout(self.verticalLayout_3)
        self.line_2 = QtGui.QFrame(self.gridLayoutWidget_2)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.options_layout.addWidget(self.line_2)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.sharey_chk = QtGui.QCheckBox(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.sharey_chk.setFont(font)
        self.sharey_chk.setObjectName(_fromUtf8("sharey_chk"))
        self.verticalLayout_2.addWidget(self.sharey_chk)
        self.y_exp_intensities_chk = QtGui.QCheckBox(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.y_exp_intensities_chk.setFont(font)
        self.y_exp_intensities_chk.setObjectName(_fromUtf8("y_exp_intensities_chk"))
        self.verticalLayout_2.addWidget(self.y_exp_intensities_chk)
        self.options_layout.addLayout(self.verticalLayout_2)
        self.matches_layout.addLayout(self.options_layout, 0, 1, 1, 1)
        self.gridLayoutWidget_2.raise_()
        self.gridLayout_2.addWidget(self.matches_selections_grpbox, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.matches_selections_grpbox.setTitle(_translate("Form", "Graph Options", None))
        self.redisplay_btn.setText(_translate("Form", "Redisplay", None))
        self.label.setText(_translate("Form", "Experiment", None))
        self.full_spectrum_chk.setText(_translate("Form", "Plot full spectrum", None))
        self.color_experiment_chk.setText(_translate("Form", "Color peak assignments", None))
        self.label_2.setText(_translate("Form", "Matches ", None))
        self.sharey_chk.setText(_translate("Form", "Share Experiment y-axis", None))
        self.y_exp_intensities_chk.setText(_translate("Form", "Set y to experiment intensities", None))

