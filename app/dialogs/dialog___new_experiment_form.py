# Author: Jasmine Oliveira
# Date: 08/22/2016

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import const
from app import error as error
from app.dialogs.frames.new_experiment.frame___new_experiment_form import Ui_Dialog    # Import frame
from app.events import display_error_message
from dialog___composition_selector import CompositionSelector
from app.events import LoadingProgressScreen

class NewExperimentForm(QDialog):

    def __init__(self):
        """

        """
        super(NewExperimentForm, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("New Experiment Form")
        self.resize(1025, 750)

        ''' Form Input Data '''
        self.file_path = None
        self.experiment_name = None
        self.author = None
        self.composition = None
        self.file_type = None
        self.databases = None
        self.units = None
        self.type = None
        self.notes = None

        ''' Setup GUI '''
        self.__set_up__()           # Setup UI Changes
        self.new_window = None

    def __set_up__(self):
        """
        Set up the UI with appropriate values, and settings.
        """

        ''' Choose Database'''
        self.ui.local_chk.click()
        # Temporarily disable additional database options
        self.ui.hitran_chk.setDisabled(True)
        self.ui.hitran_chk.setStyleSheet("color: gray;")
        self.ui.splatlog_chk.setDisabled(True)
        self.ui.splatlog_chk.setStyleSheet("color: gray;")

        ''' Units Combobox '''
        unit_list = self.to_tr(const.FREQUENCY_UNITS)
        self.ui.units_combobx.addItems(unit_list)
        self.ui.units_combobx.setCurrentIndex(0)

        ''' Experiment Combobox '''
        type_list = self.to_tr(const.EXPERIMENT_TYPES)
        self.ui.type_combobx.addItems(type_list)
        self.ui.type_combobx.setCurrentIndex(0)

        self.connect_buttons()  # Connect buttons to its respective function

    def analyze(self):

        self.collect_form_data()                         # Get information from fields
        has_errors = self.determine_errors()    # Check for field validity

        if has_errors is False:
            # No errors, may proceed to the next frame
            mid = self.import_entry()
            self.next_frame(mid)

    def back_frame(self):
        from dialog___main_menu import MainMenu  # Import Main Menu as (back_frame)
        self.close()
        window = MainMenu()
        window.exec_()

    def collect_form_data(self):
        """
        Gets data from the UI, and stores in its respective class variable.
        :return:
        """
        # Get File Path
        self.file_path = self.ui.select_file_txt.text()

        # Get Author
        #self.author = self.ui.author_txt.text()

        # Get Experiment name
        self.experiment_name = self.ui.name_txt.text()

        # Get Composition
        self.composition = self.ui.composition_txt.text()

        # Get Units
        self.units = self.ui.units_combobx.currentText()

        # Get Type
        self.type = self.ui.type_combobx.currentText()

        # Get notes
        self.notes = self.ui.notes_txt.text()

        # Set File type
        # Whether a peak file or a full spectrum file
        if self.ui.peak_type_rbtn.isChecked():
            self.file_type = "peak"
        else:
            self.file_type = "full"

        # Set Analysis Option
        self.databases = ["local"]

    def connect_buttons(self):
        # Get Buttons / Labels
        select_file_btn = self.ui.select_file_btn
        back_btn = self.ui.back_btn
        analyze_btn = self.ui.analyze_btn
        composition_btn = self.ui.composition_btn

        # Connect Buttons to Functions
        select_file_btn.clicked.connect(self.select_file)
        back_btn.clicked.connect(self.back_frame)
        analyze_btn.clicked.connect(self.analyze)
        composition_btn.clicked.connect(self.open_composition_selector)

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

    def import_entry(self):
        """
        Import experiment entry
        """
        import tables.molecules_table as molecules_table
        import tables.peaks_table as peaks_table
        import tables.experimentinfo_table as info_table
        from config import conn, db_dir
        import time

        ''' Start Loading Screen '''
        loading_screen = LoadingProgressScreen()
        loading_screen.start()

        ''' Add Entry '''
        loading_screen.set_caption('Adding Experiment Entry...')
        mid = molecules_table.new_molecule_entry(conn, str(self.experiment_name), "experiment")

        ''' Import File '''
        if self.file_type is "peaks":
            loading_screen.set_caption('Collecting data points...')
        else:
            loading_screen.set_caption('Collecting data, and finding peaks...')
        loading_screen.next_value(40)

        peaks_table.import_file(conn, str(self.file_path), mid)
        info_table.new_entry(conn, str(mid), str(self.type), str(self.units),
                             str(self.composition), str(self.notes))

        # If there is a full spectrum file, copy to SPECdata/data/experiments/mid.sp
        if self.file_type is not "peaks":
            loading_screen.next_value(80)
            loading_screen.set_caption('Saving full spectrum...')

            from shutil import copyfile
            experiment_file_path = os.path.join(db_dir, "experiments", (str(mid) + ".sp"))
            copyfile(str(self.file_path), experiment_file_path)

        loading_screen.next_value(100)

        '''End Loading Screen'''
        loading_screen.end()

        return mid

    def next_frame(self, mid):
        from dialog___open_experiment_view import OpenExperimentView
        # Go to next fame
        self.close()
        window = OpenExperimentView(str(self.experiment_name), mid)
        window.show()
        window.exec_()

    def open_composition_selector(self):
        """
        Opens a CompositionSelector dialog, and stores returning string in
        self.ui.composition_txt
        """
        widget = CompositionSelector(self.ui.composition_txt)
        widget.exec_()

    def select_file(self):

        w = QWidget()
        w.resize(320, 240)
        w.setWindowTitle("Open File")
        self.file_path = QFileDialog.getOpenFileName(w, 'Open File', os.path.curdir)
        self.ui.select_file_txt.setText(self.file_path)

    def to_tr(self, strings):
        tr_array = []
        for s in strings:
            tr_array.append(self.tr(s))

        return tr_array








