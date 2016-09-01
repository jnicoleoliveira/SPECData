# Author: Jasmine Oliveira
# Date: 08/24/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from frames.frame___assignment_window import Ui_Dialog


class AssignmentWindow(QDialog):

    def __init__(self, match):
        super(AssignmentWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Experiment View")

        self.selection_widget = None
        self.list_widget = None
        self.title_label= None
        self.match = match

    def setup_layout(self):

        layout = QGridLayout()
        self.setLayout(layout)

        # Widgets
