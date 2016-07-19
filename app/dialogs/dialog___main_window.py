# Author: Jasmine Oliveira
# Date: 7/12/2016

from PyQt4.QtGui import *

from frames.frame___main_window import Ui_MainWindow # import frame

from dialog___import_menu import ImportMenu # import next window
from events import clickable


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_menu()

    def set_menu(self):
        import_lbl = self.ui.import_lbl
        clickable(import_lbl).connect(self.show_import_menu)

    def show_import_menu(self):
        self.close()
        window = ImportMenu()
        window.exec_()