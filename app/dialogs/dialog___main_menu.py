# Author: Jasmine Oliveira
# Date: 7/12/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from frames.frame___main_menu import Ui_mainmenu    # This window

from dialog___import_menu import ImportMenu         # import window
from dialog___new_experiment_form import NewExperimentForm    # New Experiment Window

from events import clickable


class MainMenu(QDialog):

    def __init__(self, parent=None):
        super(MainMenu, self).__init__()
        self.ui=Ui_mainmenu()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.connect_buttons()

    def connect_buttons(self):
        # Get Buttons/Labels
        import_lbl = self.ui.import_lbl
        new_experiment_lbl = self.ui.new_lbl

        # Connect Label to Functions
        clickable(import_lbl).connect(self.show_import_menu)
        clickable(new_experiment_lbl).connect(self.start_new_experiment)

    def show_import_menu(self):
        self.close()
        window = ImportMenu()
        window.exec_()

    def start_new_experiment(self):
        self.close()
        window = NewExperimentForm()
        window.exec_()