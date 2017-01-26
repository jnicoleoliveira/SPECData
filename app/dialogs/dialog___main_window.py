# Author: Jasmine Oliveira
# Date: 7/19/2016

import sys

from PyQt4.QtGui import *

from app.dialogs.dialog___main_menu import MainMenu
from app.dialogs.frames.main.frame___main_window import Ui_MainWindow  # import frame

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

    def start_main_menu(self):
        self.close()
        status = MainMenu().exec_()

        sys.exit(status)
