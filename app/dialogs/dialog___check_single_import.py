from PyQt4.QtCore import *
from PyQt4.QtGui import *

from events import clickable
from frames.frame___check_single_import import Ui_checksingleimport_frame   # import frame

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

    def connect_buttons(self):
        # Get buttons/labels
        back_lbl = self.ui.back_lbl
        finish_lbl = self.ui.finish_lbl

        # Set Buttons
        clickable(finish_lbl).connect(self.finish)
        clickable(back_lbl).connect(self.back)

    #def do_import(self):

    def finish(self):
        """
        Closes current window, and opens ImportFinished window
        :return:
        """
        from dialog___import_finished import ImportFinished # Import window

        self.close()
        list = ["1test", "2test", "3"]
        window = ImportFinished(list)
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