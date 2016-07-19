# Author: Jasmine Oliveira
# Date: 7/12/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from frames.frame___main_menu import Ui_mainmenu
from dialog___import_menu import ImportMenu # import next window
from events import clickable


class MainMenu(QDialog):

    def __init__(self, parent=None):
        super(MainMenu, self).__init__()
        self.ui=Ui_mainmenu()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.set_menu()

    def set_menu(self):
        import_lbl = self.ui.import_lbl
        clickable(import_lbl).connect(self.show_import_menu)

    def show_import_menu(self):
        self.close()
        window = ImportMenu()
        window.exec_()