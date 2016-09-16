# Author: Jasmine Oliveira
# Date: 7/13/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from app.events import clickable
from dialog___import_single_file import ImportSingleFile     # Next Dialog Window
from frames.frame___import_menu import Ui_importmenu_frame  # import frame


class ImportMenu(QDialog):
    def __init__(self):
        super(ImportMenu, self).__init__()
        self.ui= Ui_importmenu_frame()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.resize(1025, 750)

        # Set up Menu
        self.connect_buttons()

    def connect_buttons(self):
        single_lbl = self.ui.single_lbl
        directory_lbl = self.ui.directory_lbl
        goback_lbl = self.ui.goback_lbl

        clickable(single_lbl).connect(self.import_single_file)

    def import_single_file(self):
        self.close()
        window = ImportSingleFile()
        window.exec_()

