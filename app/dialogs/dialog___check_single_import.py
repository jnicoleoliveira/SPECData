from PyQt4.QtCore import *
from PyQt4.QtGui import *

from events import clickable
from frames.frame___check_single_import import Ui_checksingleimport_frame   # import frame

# Database Import
import sqlite3
import config
from tables.entry import entry_molecules, entry_peaks, entry_info
from tables.get import get_peaks


class CheckSingleImport(QDialog):

    def __init__(self, file_path, name, category):
        super(CheckSingleImport, self).__init__()
        self.ui= Ui_checksingleimport_frame()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Data
        self.file_path = file_path
        self.name = name
        self.category = category

        self.connect_buttons()
        self.populate_tbl() # Populates info table

        self.log = []

    def connect_buttons(self):
        # Get buttons/labels
        back_lbl = self.ui.back_lbl
        finish_lbl = self.ui.finish_lbl

        # Set Buttons
        clickable(finish_lbl).connect(self.finish)
        clickable(back_lbl).connect(self.back)

    def do_import(self):

        log = self.log
        name = str(self.name)
        category = str(self.category)
        file_path = str(self.file_path)

        # Get SQlite Connection
        conn = sqlite3.connect(config.db_filepath)

        # Determine if information exists
        mid = entry_molecules.get_mid(conn, name, category)
        if mid is not None:
            # Already exists. Add info to log, and exit
            log.append("ERROR: Cannot enter entry")
            log.append("ERROR: Molecule entry already exists. MID: " + str(mid))
            return False

        # Entry is not duplicate
        # Import Molecule Entry
        mid = entry_molecules.new_molecule_entry(conn, name, category)
        log.append("Successfully added Molecule Entry: " + str(mid) + " " + name + " " + category)

        # Import Info Table
        # iid = entry_info()
        # log.append....

        # Import Peaks Entry
        entry_success = entry_peaks.import_file(conn, file_path, mid)

        # Determine if peak entry was a success
        if entry_success is False:
            # Entry was not a success. Add to log, and return False
            log.append("ERROR: Peaks could not be added. Please check your file.")
        else:
            pid_count = len(get_peaks.get_pid_list(conn,mid))
            log.append("Successfully added " + str(pid_count) + " peaks")

        return True

    def finish(self):
        """
        Closes current window, and opens ImportFinished window
        :return:
        """
        from dialog___import_finished import ImportFinished # Import window

        self.do_import()    # Do Import
        self.close()        # Close current window
        window = ImportFinished(self.log)   # Open Next Window
        window.exec_()

    def back(self):
        """
        Returns to previous frame (import single file)
        Maintains the fields (path, name, category)
        :return:
        """
        from dialog___import_single_file import ImportSingleFile    # Import Window

        self.close()
        window = ImportSingleFile(self.file_path, self.name, self.category)
        window.exec_()

    def populate_tbl(self):
        """
        Populates Info table to be reconfirmed for errors
        The values displayed will be imported to the database
        :return:
        """
        # Values for Table
        fields = ["Molecule Name", "Molecule Category", "Molecule File Path"]
        values = [self.name, self.category, self.file_path]

        row_count = len(fields) # Number of values
        column_count = 2        # field, value

        # Format Table
        info_tbl = self.ui.info_tbl
        info_tbl.setRowCount(row_count)
        info_tbl.setColumnCount(column_count)

        # Input field/values into table
        # by converting string values to table widget items
        for i in range(0, len(fields)):

            # Create Table Widget items for input
            field = QTableWidgetItem(values[i])
            value = QTableWidgetItem(fields[i])

            # Input widget items in table
            info_tbl.setItem(i, 1, field)
            info_tbl.setItem(i, 0, value)