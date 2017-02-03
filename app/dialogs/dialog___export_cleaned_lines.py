# Author: Jasmine Oliveira
# Date: 11/4/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from analysis.experiment_write_up import ExperimentWriteUp
from analysis.filetypes import *
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

        # Export Type #
        self.type = FileType.TEXT_FILE
        self.format = FileFormat.DELIMITER
        self.delimiter = " "
        self.shots = None

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
        invert_btn = self.ui.invert_btn
        options_btn = self.ui.options_btn

        ''' Connect buttons to associated functions '''
        select_file_btn.clicked.connect(self.save_file)
        select_all_btn.clicked.connect(self.select_all)
        deselect_all_btn.clicked.connect(self.deselect_all)
        ok_btn.clicked.connect(self.ok)
        cancel_btn.clicked.connect(self.cancel)
        invert_btn.clicked.connect(self.invert)
        options_btn.clicked.connect(self.open_choose_export_file_type_window)

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
        save_as_file(self.ui.select_file_txt, EXPORT_FILE_TYPES[self.type].extension)
        self.save_path = self.ui.select_file_txt.text()

    def select_all(self):
        """
        'Clicks' all checkboxes that are not checked
        :return:
        """
        for c in self.checkboxes:
            if c.checkbox.isChecked() is False:
                c.checkbox.click()

    def deselect_all(self):
        """
        'Clicks' all checkboxes that are checked
        :return:
        """
        for c in self.checkboxes:
            if c.checkbox.isChecked() is True:
                c.checkbox.click()

    def invert(self):
        """
        'Clicks' all checkboxes to invert the selections
        :return:
        """
        for c in self.checkboxes:
            c.checkbox.click()

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
        # writeup.export_cleaned_lines(validated_mids, self.save_path)
        writeup.export(validated_mids, self.save_path, self.type, self.format, self.delimiter, self.shots)

    def ok(self):

        # -- Check for save path errors -- #
        if self.save_path is None:
            # No Path Chosen
            self.throw_no_export_error("Please select an export location.",
                                       "You have not selected an export location. Please\
                                       select an export location to save to.")
            return

        # -- Get mids -- #
        mids = self.get_to_be_cleaned_mids()

        # -- Check for MID errors -- #
        if mids is None:
            self.throw_no_export_error("Please select at least (1) validation to be cleaned",
                                       "You have selected no valid molecule lines to be cleaned. You\
                                       must select at least (1).")
            return

        # No Errors, OK to do export!
        self.do_export(mids)

        # Show Export Completed
        display_informative_message("Export Complete!")
        self.close()

    def open_choose_export_file_type_window(self):
        from dialog___choose_export_cleaned_lines_file_type import ChooseExportFileType
        window = ChooseExportFileType()
        if window.exec_():
            self.type, self.format, self.delimiter, self.shots = window.get_values()

        self.ui.type_lbl.setText(self.type.title())
        self.ui.format_lbl.setText(self.format.title())

        if self.shots is not None:
            self.ui.data_title_lbl.setText("Shots")
            self.ui.data_lbl.setText(str(self.shots))
        elif self.delimiter is not None:
            self.ui.data_title_lbl.setText("Delimiter")
            if self.delimiter == " ":
                self.ui.data_lbl.setText("Space")
            elif self.delimiter == "\t":
                self.ui.data_lbl.setText("Tab")
            elif self.delimiter == ",":
                self.ui.data_lbl.setText("Comma")
            else:
                self.ui.data_lbl.setText(self.delimiter)
        else:
            # No additional data
            self.ui.data_title_lbl.setText("")
            self.ui.data_lbl.setText("")


class MoleculeBox:
    def __init__(self, checkbox, mid):
        self.checkbox = checkbox
        self.mid = mid






