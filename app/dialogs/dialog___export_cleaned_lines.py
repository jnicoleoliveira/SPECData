# Author: Jasmine Oliveira
# Date: 11/4/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from analysis.experiment_write_up import ExperimentWriteUp
from app.dialogs.frames.experiment_view.frame___export_cleaned_lines import Ui_Dialog
from ..events import display_error_message, save_as_file, display_informative_message


class ExportCleanedLines(QDialog):

    def __init__(self, experiment):
        super(ExportCleanedLines, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Export Cleaned Lines")
        self.resize(500, 750)

        # Given Experiment
        self.experiment = experiment

        # Variables to hold form input
        self.clean_mids_list = []
        self.save_path = None
        self.checkboxes = []

        self.setup_selection_widget()
        self.connect_buttons()

    def setup_selection_widget(self):

        # -- Set Scrollable Area layout -- #
        layout = QVBoxLayout()
        self.ui.scrollArea.setLayout(layout)

        # -- Get Validated Mids, and Create Checkboxes -- #
        for molecule in self.experiment.validated_matches.values():
            name = molecule.name
            mid = molecule.mid
            lines_count = molecule.m

            checkbox = QCheckBox()
            text = name + "(" + str(lines_count) + ")"
            checkbox.setText(text)

            self.checkboxes.append(MoleculeBox(checkbox, mid))
            layout.addWidget(checkbox)
            #layout.addItem(QLine)
            #layout.addWidget(QLine())

        self.show()

    def connect_buttons(self):
        """
        Connects Buttons to associated functions.
        """
        ''' Get Buttons '''
        select_file_btn = self.ui.select_file_btn
        select_all_btn = self.ui.select_all_btn
        deselect_all_btn = self.ui.deselect_all_btn
        ok_btn = self.ui.ok_btn
        cancel_btn = self.ui.cancel_btn

        ''' Connect buttons to associated functions '''
        select_file_btn.clicked.connect(self.save_file)
        select_all_btn.clicked.connect(self.select_all)
        deselect_all_btn.clicked.connect(self.deselect_all)
        ok_btn.clicked.connect(self.ok)
        cancel_btn.clicked.connect(self.cancel)

    def cancel(self):
        """
        Cancel Function, closes the current dialog window.
        """
        self.close()

    def save_file(self):
        """
        Save file, opens file selector, and determines the location and
        name of the intended file.
        """
        #select_file(self.ui.select_file_txt)
        save_as_file(self.ui.select_file_txt)
        self.save_path = self.ui.select_file_txt.text()

    def deselect_all(self):
        print "DESELECT ALL"

    def select_all(self):
        print "stub"

    def get_to_be_cleaned_mids(self):
        mids = []

        for box in self.checkboxes:
            widget = box.checkbox
            mid = box.mid

            if widget.isChecked():
                mids.append(mid)

        return mids

    def throw_no_export_error(self, info, detail):
        text = "Error: Cannot do export!"
        display_error_message(text,info, detail)

    def do_export(self, validated_mids):
        # -- Create Write Up -- #
        writeup = ExperimentWriteUp(self.experiment)

        # -- Export Cleaned Lines -- #
        writeup.export_cleaned_lines(validated_mids, self.save_path)

    def ok(self):

        # -- Check for save path errors -- #
        if self.save_path is None:
            # No Path Chosen
            self.throw_no_export_error("Please select an export location.",
                                       "You have not selected an export location. Please\
                                       select an export location to save to.")
            return
        #elif not path_exists(self.save_path):
        #    # Path does not exist
        #    msg = get_file_error_message(self.save_path)
        #    self.throw_no_export_error("Invalid save location, please choose another.", msg)
        #    return

        # -- Get mids -- #
        mids = self.get_to_be_cleaned_mids()

        # -- Check for MID errors -- #
        if mids is None:
            self.throw_no_export_error("Please select at least (1) validation to be cleaned",
                                       "You have selected no valid molecule lines to be cleaned. You\
                                       must select at least (1).")
            return

        # Create File Type
        self.save_path += ".lines"

        # No Errors, OK to do export!
        self.do_export(mids)

        # Show Export Completed
        display_informative_message("Export Complete!")
        self.close()


class MoleculeBox:
    def __init__(self, checkbox, mid):
        self.checkbox = checkbox
        self.mid = mid






