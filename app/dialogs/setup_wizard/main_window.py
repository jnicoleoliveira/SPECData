# Author: Jasmine Oliveira
# Date: 5/17/2016

import sys

from PyQt4.QtGui import *

from app.dialogs.frames.main.frame___main_window import Ui_MainWindow  # import frame
from app.dialogs.setup_wizard.dialog___welcome import WelcomeWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

    def start_main_menu(self):
        self.close()
        status = WelcomeWindow().exec_()

        sys.exit(status)
