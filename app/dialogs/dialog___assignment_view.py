# Author: Jasmine Oliveira
# Date: 06/06/2017
# Description:
#   Updated AssignmentView from previous AssignmentWindow (8/24/2016)

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from app.dialogs.frames.assignment_view.frame___assignment_window import Ui_Dialog              # Dialog Window
from app.widgets.widget___assignment_graph_options import AssignmentGraphOptionsWidget  # Graph Options Widget
from app.widgets.widget___assignment_window_info import AssignmentInfoWidget  # Assignment Info Widget
from app.widgets.widget___experiment_graph_widget import ExperimentGraphWidget
from config import conn
from config import resources
from images import LOGO_ICON
from tables.molecules_table import get_category

class AssignmentWindow(QDialog):

    def __init__(self, match, color, experiment):
        super(AssignmentWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowIcon(QIcon(QPixmap(LOGO_ICON)))

        self.setWindowTitle("Assignment View")
        self.resize(1500, 750)

        # Widgets
