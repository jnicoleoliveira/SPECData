# Author: Jasmine Oliveira
# Date: 7/12/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ImportMenu import ImportMenu
from frames.mainwindow_frame import Ui_MainWindow
from events import clickable


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_menu()

    def set_menu(self):
        import_lbl = self.ui.import_lbl

        clickable(import_lbl).connect(self.showImportMenu)

    def showImportMenu(self):
        self.close()
        window = ImportMenu()
        window.exec_()