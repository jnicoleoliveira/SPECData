# Author: Jasmine Oliveira
# Date: 5/17/2016

import sys

from PyQt4.QtGui import *

from analysis.experiment import Experiment
from app.dialogs.dialog___assignment_view import AssignmentWindow
from app.dialogs.frames.main.frame___main_window import Ui_MainWindow  # import frame


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

    def start_main_menu(self):
        experiment = Experiment("Name", 122)
        experiment.get_assigned_molecules()

        self.close()

        status = AssignmentWindow(experiment.molecule_matches.values()[1], "blue", experiment).exec_()

        sys.exit(status)
