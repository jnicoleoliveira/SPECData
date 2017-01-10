# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'experiment_view.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet(_fromUtf8("background-color: rgb(48, 48, 48);\n"
"gridline-color: rgb(195, 195, 195);\n"
"color: rgb(255, 255, 255);\n"
""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menu_bar = QtGui.QMenuBar(MainWindow)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menu_bar.setStyleSheet(_fromUtf8("background-color: rgb(43, 43, 43);"))
        self.menu_bar.setObjectName(_fromUtf8("menu_bar"))
        self.menuView = QtGui.QMenu(self.menu_bar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuFile = QtGui.QMenu(self.menu_bar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menu_bar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuEdit_2 = QtGui.QMenu(self.menu_bar)
        self.menuEdit_2.setObjectName(_fromUtf8("menuEdit_2"))
        MainWindow.setMenuBar(self.menu_bar)
        self.action_bar = QtGui.QToolBar(MainWindow)
        self.action_bar.setObjectName(_fromUtf8("action_bar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.action_bar)
        MainWindow.insertToolBarBreak(self.action_bar)
        self.graph_action_bar = QtGui.QToolBar(MainWindow)
        self.graph_action_bar.setObjectName(_fromUtf8("graph_action_bar"))
        MainWindow.addToolBar(QtCore.Qt.RightToolBarArea, self.graph_action_bar)
        MainWindow.insertToolBarBreak(self.graph_action_bar)
        self.action_Graph_Tools = QtGui.QAction(MainWindow)
        self.action_Graph_Tools.setObjectName(_fromUtf8("action_Graph_Tools"))
        self.actionFull_Screen = QtGui.QAction(MainWindow)
        self.actionFull_Screen.setObjectName(_fromUtf8("actionFull_Screen"))
        self.action_Graph_Settings = QtGui.QAction(MainWindow)
        self.action_Graph_Settings.setObjectName(_fromUtf8("action_Graph_Settings"))
        self.actionAnalysis_Bar = QtGui.QAction(MainWindow)
        self.actionAnalysis_Bar.setObjectName(_fromUtf8("actionAnalysis_Bar"))
        self.actionSave_Analysis = QtGui.QAction(MainWindow)
        self.actionSave_Analysis.setObjectName(_fromUtf8("actionSave_Analysis"))
        self.actionSave_analysis_as = QtGui.QAction(MainWindow)
        self.actionSave_analysis_as.setObjectName(_fromUtf8("actionSave_analysis_as"))
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionSave_analysis_write_up = QtGui.QAction(MainWindow)
        self.actionSave_analysis_write_up.setObjectName(_fromUtf8("actionSave_analysis_write_up"))
        self.actionSave_analysis_write_up_as = QtGui.QAction(MainWindow)
        self.actionSave_analysis_write_up_as.setObjectName(_fromUtf8("actionSave_analysis_write_up_as"))
        self.actionRe_analyze = QtGui.QAction(MainWindow)
        self.actionRe_analyze.setObjectName(_fromUtf8("actionRe_analyze"))
        self.actionEdit_Analyze_Configurations = QtGui.QAction(MainWindow)
        self.actionEdit_Analyze_Configurations.setObjectName(_fromUtf8("actionEdit_Analyze_Configurations"))
        self.actionRe_analyze_2 = QtGui.QAction(MainWindow)
        self.actionRe_analyze_2.setObjectName(_fromUtf8("actionRe_analyze_2"))
        self.actionAdd_a_molecule = QtGui.QAction(MainWindow)
        self.actionAdd_a_molecule.setObjectName(_fromUtf8("actionAdd_a_molecule"))
        self.action_Exit = QtGui.QAction(MainWindow)
        self.action_Exit.setObjectName(_fromUtf8("action_Exit"))
        self.actionSelect_All_Ctrl_A = QtGui.QAction(MainWindow)
        self.actionSelect_All_Ctrl_A.setObjectName(_fromUtf8("actionSelect_All_Ctrl_A"))
        self.actionUndo = QtGui.QAction(MainWindow)
        self.actionUndo.setObjectName(_fromUtf8("actionUndo"))
        self.actionRedo = QtGui.QAction(MainWindow)
        self.actionRedo.setObjectName(_fromUtf8("actionRedo"))
        self.actionExport_cleaned_lines = QtGui.QAction(MainWindow)
        self.actionExport_cleaned_lines.setObjectName(_fromUtf8("actionExport_cleaned_lines"))
        self.menuView.addAction(self.actionFull_Screen)
        self.menuView.addSeparator()
        self.menuView.addAction(self.action_Graph_Settings)
        self.menuView.addAction(self.actionAnalysis_Bar)
        self.menuFile.addAction(self.actionSave_Analysis)
        self.menuFile.addAction(self.actionSave_analysis_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_analysis_write_up)
        self.menuFile.addAction(self.actionSave_analysis_write_up_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_cleaned_lines)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_Exit)
        self.menuEdit.addAction(self.actionRe_analyze_2)
        self.menuEdit.addAction(self.actionRe_analyze)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionAdd_a_molecule)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionEdit_Analyze_Configurations)
        self.menuEdit_2.addAction(self.actionUndo)
        self.menuEdit_2.addAction(self.actionRedo)
        self.menuEdit_2.addSeparator()
        self.menuEdit_2.addAction(self.actionSelect_All_Ctrl_A)
        self.menu_bar.addAction(self.menuFile.menuAction())
        self.menu_bar.addAction(self.menuEdit_2.menuAction())
        self.menu_bar.addAction(self.menuView.menuAction())
        self.menu_bar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuView.setTitle(_translate("MainWindow", "View", None))
        self.menuFile.setTitle(_translate("MainWindow", "&File", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Run", None))
        self.menuEdit_2.setTitle(_translate("MainWindow", "Edit", None))
        self.action_bar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.graph_action_bar.setWindowTitle(_translate("MainWindow", "toolBar_2", None))
        self.action_Graph_Tools.setText(_translate("MainWindow", "&Graph Tools", None))
        self.actionFull_Screen.setText(_translate("MainWindow", "Enter Full Screen", None))
        self.action_Graph_Settings.setText(_translate("MainWindow", "Graph Settings", None))
        self.actionAnalysis_Bar.setText(_translate("MainWindow", "Analysis Bar", None))
        self.actionSave_Analysis.setText(_translate("MainWindow", "&Save analysis                               Ctrl+S   ", None))
        self.actionSave_analysis_as.setText(_translate("MainWindow", "Save analysis as...", None))
        self.actionSettings.setText(_translate("MainWindow", "Settings...", None))
        self.actionSave_analysis_write_up.setText(_translate("MainWindow", "&Save analysis write-up", None))
        self.actionSave_analysis_write_up_as.setText(_translate("MainWindow", "Save analysis write-up as..", None))
        self.actionRe_analyze.setText(_translate("MainWindow", "Re-analyze...", None))
        self.actionEdit_Analyze_Configurations.setText(_translate("MainWindow", "&Edit analysis configurations", None))
        self.actionRe_analyze_2.setText(_translate("MainWindow", "&Re-analyze", None))
        self.actionAdd_a_molecule.setText(_translate("MainWindow", "Add a molecule...", None))
        self.action_Exit.setText(_translate("MainWindow", "E&xit", None))
        self.actionSelect_All_Ctrl_A.setText(_translate("MainWindow", "Select All                       Ctrl+A", None))
        self.actionUndo.setText(_translate("MainWindow", "Undo                             Ctrl+Z", None))
        self.actionRedo.setText(_translate("MainWindow", "Redo                              Ctrl+Y", None))
        self.actionExport_cleaned_lines.setText(_translate("MainWindow", "Export cleaned lines..", None))

