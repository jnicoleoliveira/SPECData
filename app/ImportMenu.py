# Author: Jasmine Oliveira
# Date: 7/13/2016

from frames.importmenu_frame import Ui_importmenu_frame
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ImportMenu(QDialog):
    def __init__(self):
        super(ImportMenu, self).__init__()
        self.ui= Ui_importmenu_frame()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)