# Author: Jasmine Oliveira
# Date: 08/22/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from frames.frame___new_experiment_form import Ui_Dialog    # Import frame

# Dialog Functions
from events import display_error_message

import os
import error as error


class NewExperimentForm(QDialog):
    def __init__(self):
        super(NewExperimentForm, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("New Experiment Form")

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
        self.ui.select_file_txt.setPlainText(self.file_path)

    def next_frame(self):
        # Go to next fame
        # STUB
        return True

    def back_frame(self):
        from dialog___main_menu import MainMenu  # Import Main Menu as (back_frame)
        self.close()
        window = MainMenu()
        window.exec_()

    def analyze(self):

        self.get_data()                         # Get information from fields
        has_errors = self.determine_errors()    # Check for field validity

        if has_errors is False:
            # No errors, may proceed to the next frame
            self.next_frame()
            return

    def get_data(self):
        """
        Gets data from the UI, and stores in its respective class variable.
        :return:
        """
        # Get File Path
        self.file_path = self.ui.select_file_txt.toPlainText()

        # Get Author
        self.author = self.ui.author_txt.toPlainText()

        # Get Experiment name
        self.experiment_name = self.ui.name_txt.toPlainText()

        # Get Composition
        self.composition = self.ui.composition_txt.toPlainText()

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
        if self.file_path is None or self.file_path:
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
