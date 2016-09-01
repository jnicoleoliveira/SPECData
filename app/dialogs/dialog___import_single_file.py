from PyQt4.QtCore import *
from PyQt4.QtGui import *

from app import error as error
from app.events import clickable
from app.events import display_error_message
from dialog___check_single_import import CheckSingleImport # Next Dialog
from frames.frame___import_single_file import Ui_importsingle_frame # import frame


class ImportSingleFile(QDialog):
    """
        Import a Single File class.
            UI: importsingle_form
            Gathers information to import a new file.
    """

    def __init__(self, file_path=None, name=None, category=None):
        super(ImportSingleFile, self).__init__()
        # Set up UI to form
        self.ui= Ui_importsingle_frame()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Variables for input
        self.file_path = file_path
        self.name = name
        self.category = category

        # Events
        self.show_cached_input() # If cached input, display
        self.connect_buttons()  # Connect buttons to associated action

    def show_cached_input(self):
        """
        Shows cached input, if returned to this form
        :return:
        """
        if self.file_path is not None:
            self.ui.selectfile_txt.setPlainText(self.file_path)

        if self.name is not None:
            self.ui.name_txt.setPlainText(self.name)

        if self.category is not None:
            if self.category is "known":
                self.ui.known_rbtn.click()
            elif self.category is "experiment":
                self.ui.experiment_rbtn.click()
            elif self.category is "artifact":
                self.ui.experiment_rbtn.click()

    def connect_buttons(self):
        # Get buttons/labels
        next_lbl = self.ui.next_lbl
        back_lbl = self.ui.back_lbl
        selectfile_btn = self.ui.selectfile_btn

        # Next and Back labels to buttons
        clickable(next_lbl).connect(self.next_frame)
        clickable(back_lbl).connect(self.back_frame)

        # Set Select File button
        selectfile_btn.clicked.connect(self.select_file)

    def determine_name(self):
        """
        Sets self.name to name_txt  plain text value input
        :return:
        """
        name_txt = self.ui.name_txt
        self.name = name_txt.toPlainText()

    def determine_checked_category(self):
        """
        Determines checked category
        The associated radio button, determines the value of self.category
        Category values: "known", "experiment", or "artifact"
        :return:
        """
        known_rbtn = self.ui.known_rbtn
        experiment_rbtn = self.ui.experiment_rbtn
        artifact_btn = self.ui.artifact_btn

        if known_rbtn.isChecked():
            self.category = "known"
        elif experiment_rbtn.isChecked():
            self.category = "experiment"
        elif artifact_btn.isChecked():
            self.category = "artifact"
        else:
            self.category = None

    def has_error(self):

        error_msg = ""
        has_error = True

        # Determine if no empty fields
        if self.file_path is None or self.file_path is "":
            error_msg += "ERROR: File Path incomplete."
        if self.name is None or self.name is "":
            error_msg += "\nERROR: Name is incomplete."
        if self.category is None or self.category is "":
            error_msg += "\nERROR: Category is incomplete."

        # Determine if valid file
        if error.is_valid_file(self.file_path) is False:
            error_msg += error.get_file_error_message(self.file_path)

        # If Error Message is empty, then error is false.
        if error_msg is "":
            has_error = False

        # If error exists, display error message window
        if has_error is True:
            display_error_message("Invalid input.", "Be sure to check that all fields are complete.", error_msg)

        return has_error

    def next_frame(self):
        """
        Determines if all requirements are complete
        If requirements are fulfilled, continues to next frame (check single import)
            Requirements: Filename, Entry Name, and Category
        :return: False if requirements are not complete
        """

        self.determine_checked_category()   # get category selection
        self.determine_name()               # get name field data

        # If there is an error, return
        if self.has_error() is True:
            return

        # All requirements filled
        # Next frame 'Check Single Import'
        self.close()
        window = CheckSingleImport(self.file_path, self.name, self.category)
        window.exec_()

    def back_frame(self):
        from dialog___import_menu import ImportMenu  # import back dialog window
        self.close()
        window = ImportMenu()
        window.exec_()

    def select_file(self):
        w = QWidget()
        w.resize(320, 240)
        w.setWindowTitle("Open File")
        self.file_path = QFileDialog.getOpenFileName(w, 'Open File', 'C:\\')
        self.ui.selectfile_txt.setPlainText(self.file_path)
