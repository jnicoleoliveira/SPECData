# Author: Jasmine Oliveira
# Date: 11/12/2016

from PyQt4.QtGui import *

from frames.frame___manage_database import Ui_Dialog   # import frame


class ManageDatabase(QDialog):

    def __init__(self, parent=None):
        super(ManageDatabase, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Make Queries")

        self.resize(1500, 750)
        self.show()
