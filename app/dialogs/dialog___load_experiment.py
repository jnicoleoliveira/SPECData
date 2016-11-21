# Author: Jasmine Oliveira
# Date: 09/12/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from frames.frame___load_experiment import Ui_Dialog              # Dialog Window

from config import conn
import tables.molecules_table as molecules_table
from ..events import display_error_message

class LoadExperiment(QDialog):

    def __init__(self):
        super(LoadExperiment, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Load Experiment")
        self.resize(1025, 750)

        self.list_widget = self.ui.listWidget
        self.new_window = None
        self.setup()

    def setup(self):

        self.populate_list_widget()

        back_btn = self.ui.back_btn
        load_btn = self.ui.load_btn

        back_btn.clicked.connect(self.back)
        load_btn.clicked.connect(self.load)

    def populate_list_widget(self):
        """
        Populates list widget with experiments available to load.
        """
        mids, names = molecules_table.get_experiment_list(conn)

        for i in range(0, len(mids)):
            line = str(i+1) + "\t" + str(mids[i]) + "\t" + names[i]
            self.list_widget.addItem(QListWidgetItem(line))

    def load(self):
        selected_items = self.list_widget.selectedItems()

        try:
            text = str((selected_items[0].text())).split()
            print text
            self.load_experiment(text[1], text[2])
        except ValueError:
            display_error_message("SELECTION ERROR", "You must select one item to load.",\
                                  "You have not selected one item, please select one item.")

    def back(self):
        from dialog___main_menu import MainMenu  # Import Main Menu as (back_frame)
        self.close()
        window = MainMenu()
        window.exec_()

    def load_experiment(self, mid, name):

        from dialog___experiment_view import ExperimentView
        self.new_window = ExperimentView(name, mid)
