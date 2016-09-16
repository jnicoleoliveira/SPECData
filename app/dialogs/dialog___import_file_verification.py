# Author: Jasmine Oliveira
# Date: 09/15/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from frames.frame___import_file_verification import Ui_Dialog
from app.events import display_error_message
from ..error import is_valid_file, get_file_error_message

from config import conn

class ImportFileVerification(QDialog):
    """
        Verify File and add add entry information
            UI:          import_file_verification.ui
            Dialog:      frame___import_file_verification.py
            Next Dialog: None
            Back Dialog: None
    """
    def __init__(self, file_path, i , total):
        super(ImportFileVerification, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Import File")
        self.resize(1025, 750)

        # Data
        self.file_path = str(file_path)
        self.i = i
        self.total = total
        self.name = None
        self.category = None
        self.composition = None

        # Setup
        self.__setup__()

    def __setup__(self):\

        # Set File Name Label
        self.ui.file_name_lbl.setText(self.file_path)
        self.ui.index_lbl.setText('(' + str(self.i) + '/' + str(self.total) + ')')

        # Connect Buttons
        self.connect_buttons()

    def connect_buttons(self):
        cancel_btn = self.ui.cancel_btn
        ok_btn = self.ui.ok_btn

        cancel_btn.clicked.connect(self.cancel)
        ok_btn.clicked.connect(self.okay)

    def collect_form_data(self):
        """
        Collects data from input widgets, and stores in associated variables.
        """
        self.name = str(self.ui.name_txt.text())
        self.composition = str(self.ui.composition_txt.text())

        if self.ui.artifact_rdio.isChecked():
            self.category = "artifact"
        elif self.ui.known_rdio.isChecked():
            self.category = "known"

    def cancel(self):
        self.close()

    def okay(self):
        self.collect_form_data()
        if self.determine_errors() is False:
            self.import_entry()
            self.close()

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
        if self.category is None or not self.category:
            error_msg += "ERROR: Category field incomplete."
        if self.name is None or not self.name:
            error_msg += "\nERROR: Entry Name is incomplete."
        if self.composition is None or not self.composition:
            error_msg += "\nERROR: Composition is incomplete."

        # Determine if valid file
        if is_valid_file(self.file_path) is False:
            error_msg += "\n" + get_file_error_message(self.file_path)

        # If error Message is empty, then error is false.
        if error_msg is "":
            has_error = False

        # If error exists, display error message window
        if has_error is True:
            display_error_message("Invalid input.",
                                  "Be sure to check that all fields are complete.",
                                  error_msg)

        return has_error

    def import_entry(self):
        import tables.entry.entry_molecules as molecules
        import tables.entry.entry_peaks as peaks
        import tables.entry.entry_info as info

        if molecules.get_mid(conn, self.name, self.category) is None:
            mid = molecules.new_molecule_entry(conn, self.name, self.category)
            peaks.import_file(conn, self.file_path, mid)
