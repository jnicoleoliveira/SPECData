# Author: Jasmine Oliveira
# Date: 7/12/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from dialog___new_experiment_form import NewExperimentForm    # New Experiment Window
from frames.frame___main_menu import Ui_mainmenu    # This window


class MainMenu(QDialog):

    def __init__(self, parent=None):
        super(MainMenu, self).__init__()
        self.ui = Ui_mainmenu()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Main Menu")
        self.resize(1025, 750)

        self.connect_buttons()
        self.load_logo()

    def connect_buttons(self):
        # Get Buttons/Labels
        import_btn = self.ui.import_btn
        new_experiment_btn = self.ui.new_experiment_btn
        load_experiment_btn = self.ui.load_experiment_btn
        manage_database_btn = self.ui.manage_database_btn

        # Connect Label to Functions
        import_btn.clicked.connect(self.import_files)
        new_experiment_btn.clicked.connect(self.start_new_experiment)
        load_experiment_btn.clicked.connect(self.load_experiment)
        manage_database_btn.clicked.connect(self.manage_database)

    def load_logo(self):
        import os
        from config import resources
        pix_map = QPixmap(os.path.join(resources, 'specdata_logo.png'))
        self.ui.logo_lbl.setPixmap(pix_map)

    def import_files(self):
        self.close()
        from dialog___import_files import ImportFiles
        window = ImportFiles()
        window.exec_()

    def start_new_experiment(self):
        self.close()
        window = NewExperimentForm()
        window.show()
        window.exec_()

    def load_experiment(self):
        from dialog___experiment_view import ExperimentView
        from dialog___load_experiment import LoadExperiment
        # Go to next fame
        self.close()
        #window = ExperimentView('exp1435', 142)
        #window = ExperimentView('168-175-pzf1', 143)
        window = LoadExperiment()
        window.show()
        window.exec_()

    def manage_database(self):

        # temp testing
        from dialog___composition_selector import CompositionSelector
        window = CompositionSelector()
        window.exec_()
        #from dialog___manage_database import ManageDatabase
        #window = ManageDatabase()
        #self.close()
        #window.show()
        #window.exec_()