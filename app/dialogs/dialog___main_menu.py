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
        self.ui = Ui_mainmenu()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.connect_buttons()
        self.load_logo()

    def connect_buttons(self):
        # Get Buttons/Labels
        import_lbl = self.ui.import_lbl
        new_experiment_lbl = self.ui.new_lbl
        load_experiment_lbl = self.ui.load_lbl

        # Connect Label to Functions
        clickable(import_lbl).connect(self.show_import_menu)
        clickable(new_experiment_lbl).connect(self.start_new_experiment)
        clickable(load_experiment_lbl).connect(self.load_experiment)

    def load_logo(self):
        import os
        from config import resources
        pix_map = QPixmap(os.path.join(resources, 'specdata_logo.png'))
        self.ui.logo_lbl.setPixmap(pix_map)

    def show_import_menu(self):
        self.close()
        window = ImportMenu()
        window.exec_()

    def start_new_experiment(self):
        self.close()
        window = NewExperimentForm()
        window.exec_()

    def load_experiment(self):
        from dialog___experiment_view import ExperimentView
        # Go to next fame
        self.close()
        window = ExperimentView('exp892',156)
        window.show()
        window.exec_()
