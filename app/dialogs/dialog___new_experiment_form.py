# Author: Jasmine Oliveira
# Date: 08/22/2016

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from app import error as error
from app.events import display_error_message
from frames.frame___new_experiment_form import Ui_Dialog    # Import frame


class NewExperimentForm(QDialog):

    def __init__(self):
        super(NewExperimentForm, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("New Experiment Form")
        self.resize(1025, 750)

        # Variables to hold form input
        self.file_path = None
        self.experiment_name = None
        self.author = None
        self.composition = None
        self.file_type = None
        self.databases = None

        # Set Up
        self.connect_buttons()  # Connect buttons to its respective function

    def connect_buttons(self):
        # Get Buttons / Labels
        select_file_btn = self.ui.select_file_btn
        back_btn = self.ui.back_btn
        analyze_btn = self.ui.analyze_btn

        # Connect Buttons to Functions
        select_file_btn.clicked.connect(self.select_file)
        back_btn.clicked.connect(self.back_frame)
        analyze_btn.clicked.connect(self.analyze)

    def select_file(self):

        w = QWidget()
        w.resize(320, 240)
        w.setWindowTitle("Open File")
        self.file_path = QFileDialog.getOpenFileName(w, 'Open File', os.path.curdir)
        self.ui.select_file_txt.setText(self.file_path)

    def next_frame(self, mid):
        from dialog___experiment_view import ExperimentView
        # Go to next fame
        self.close()
        window = ExperimentView(str(self.experiment_name), mid)
        window.show()
        window.exec_()

    def back_frame(self):
        from dialog___main_menu import MainMenu  # Import Main Menu as (back_frame)
        self.close()
        window = MainMenu()
        window.exec_()

    def analyze(self):

        self.collect_form_data()                         # Get information from fields
        has_errors = self.determine_errors()    # Check for field validity

        if has_errors is False:
            # No errors, may proceed to the next frame
            mid = self.import_entry()
            self.next_frame(mid)

    def import_entry(self):
        """
        Import experiment entry
        """
        import tables.entry.entry_molecules as molecules
        import tables.entry.entry_peaks as peaks
        from config import conn, db_dir

        mid = molecules.new_molecule_entry(conn, str(self.experiment_name), "experiment")
        peaks.import_file(conn, str(self.file_path), mid)

        # If there is a full spectrum file, copy to SPECdata/data/experiments/mid.sp
        if self.file_type is not "peaks":
            from shutil import copyfile
            experiment_file_path = os.path.join(db_dir, "experiments", (str(mid) + ".sp"))
            copyfile(str(self.file_path), experiment_file_path)

        return mid

    def collect_form_data(self):
        """
        Gets data from the UI, and stores in its respective class variable.
        :return:
        """
        # Get File Path
        self.file_path = self.ui.select_file_txt.text()

        # Get Author
        self.author = self.ui.author_txt.text()

        # Get Experiment name
        self.experiment_name = self.ui.name_txt.text()

        # Get Composition
        self.composition = self.ui.composition_txt.text()

        # Set File type
        # Whether a peak file or a full spectrum file
        if self.ui.peak_type_rbtn.isChecked():
            self.file_type = "peak"
        else:
            self.file_type = "full"

        # Set Analysis Option
        self.databases = ["local"]

    def determine_errors(self):
        """
        Determines if there are any UI form errors.
        Displays an error message if true, and Returns True
        Returns False otherwise.
        :return: True if errors exist, otherwise False.
        """
        error_msg = ""
        has_error = True

        # Determine Error Message
        if self.file_path is None or not self.file_path:
            error_msg += "ERROR: File Path incomplete."
        if self.author is None or not self.author:
            error_msg += "\nERROR: Author is incomplete."
        if self.experiment_name is None or not self.experiment_name:
            error_msg += "\nERROR: Experiment Name is incomplete."
        if self.composition is None or not self.composition:
            error_msg += "\nERROR: Composition is incomplete."

        # Determine if valid file
        if error.is_valid_file(self.file_path) is False:
            error_msg += "\n" + error.get_file_error_message(self.file_path)

        # If error Message is empty, then error is false.
        if error_msg is "":
            has_error = False

        # If error exists, display error message window
        if has_error is True:
            display_error_message("Invalid input.", "Be sure to check that all fields are complete.", error_msg)

        return has_error
