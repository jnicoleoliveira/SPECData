# Author: Jasmine Oliveira
# Date: 12/16/2016

import os

from PyQt4.QtGui import *

from app.dialogs.dialog___composition_selector import CompositionSelector
from app.dialogs.frames.manage_database.frame___edit_entry import Ui_Dialog   # import frame
from app.events import display_question_message, select_file
from config import conn, resources
from images import LOGO_ICON
from tables import molecules_table, experimentinfo_table, knowninfo_table, peaks_table

class EditEntry(QDialog):

    ACCENT_COLOR = "#008080"

    def __init__(self, mid, parent=None):
        super(EditEntry, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        ''' UI Options'''
        self.setWindowTitle("Edit Entry")
        self.setWindowIcon(QIcon(QPixmap(LOGO_ICON)))

        self.resize(500, 750)
        self.show()

        self.mid = mid
        self.category = None
        self.original_data = []
        self.labels = []
        self.table_widget = self.ui.table_widget

        self.__setup__()

    def open_composition_selector(self):
        window = CompositionSelector(self.ui.composition_txt)
        window.exec_()

    def open_select_file(self):
        select_file(self.ui.file_txt)

    def delete_entry(self):
        action = display_question_message("Are you sure you want to remove this "
                                        "entry from the database? All information will be lost.",
                                        "Delete Entry")
        if action is True:
            molecules_table.remove_molecule(conn, self.mid)
            self.close()

    def exit(self):
        self.close()

    def get_table_data(self):
        rows = self.table_widget.rowCount()
        values = []
        for row in range(0, rows):
            w = self.ui.table_widget.item(0, row)
            values.append(w.text())

        return values

    def save_entry(self):
        values = self.get_table_data()
        # action = display_question_message("Are you want to accept these changes?",
        #                                   "Save changes")
        from app.error import is_valid_file
        # if action is True:
        for i in range(0, len(values)):
            if self.original_data[i] != values[i]:
                print self.labels[i]
                molecules_table.update(conn, self.mid, self.labels[i].lower(), values[i])

        if self.ui.composition_txt.isEnabled():
            molecules_table.update(conn, self.mid, 'composition', self.ui.composition_txt.text())

        file_path = self.ui.file_txt.text()
        if file_path and file_path is not "":
            if is_valid_file(file_path):
                peaks_table.remove_all(conn, self.mid)
                peaks_table.import_file(conn, str(file_path), self.mid)

        molecules_table.update(conn, self.mid, 'last_updated', None)

        self.close()

    ###############################################################################
    # Private Methods
    ###############################################################################

    def __get_table_items(self, mid, category):

        items = []

        name = molecules_table.get_name(conn, mid)
        items.append(QTableWidgetItem(name))

        if category == 'known':
            units = knowninfo_table.get_units(conn, mid)
            temperature = knowninfo_table.get_temperature(conn, mid)
            isotope = knowninfo_table.is_isotype(conn, mid)
            vibrational = knowninfo_table.is_vibrational(conn, mid)
            notes = knowninfo_table.get_notes(conn, mid)

            items.append(QTableWidgetItem(units))
            items.append(QTableWidgetItem(str(temperature)))
            items.append(QTableWidgetItem(str(isotope)))
            items.append(QTableWidgetItem(str(vibrational)))
            items.append(QTableWidgetItem(notes))

            labels = ['name', 'units', 'temperature', 'isotope', 'vibrational', 'notes']

        elif category == 'experiment':
            type = experimentinfo_table.get_type(conn, mid)
            units = experimentinfo_table.get_units(conn, mid)
            notes = experimentinfo_table.get_notes(conn, mid)

            items.append(QTableWidgetItem(str(units)))
            items.append(QTableWidgetItem(str(type)))
            items.append(QTableWidgetItem(notes))

            labels = ['Name', 'Units', 'Type', 'Notes']

        else:
            print category + " but here"
            notes = knowninfo_table.get_notes(conn, mid)
            items.append(QTableWidgetItem(notes))
            labels = ['Name', 'Notes']

        return items, labels

    def __load_entry__(self):
        """ Loads the data of the given mid """

        mid = self.mid
        category = self.category

        # Populate Table
        self.__populate_table(mid, category)

        # Fill out composition text
        if category == 'known':
            composition = knowninfo_table.get_composition(conn, mid)
            self.ui.composition_txt.setText(composition)
        elif category == 'experiment':
            composition = experimentinfo_table.get_composition(conn, mid)
            self.ui.composition_txt.setText(composition)
        else:
            self.ui.composition_txt.setDisabled(True)
            self.ui.composition_btn.setDisabled(True)

    def __populate_table(self, mid, category):
        items, labels = self.__get_table_items(mid, str(category))
        table_widget = self.table_widget
        self.labels = labels

        row_count = len(items)  # Number of rows
        column_count = 1  # Number of columns

        # Format Table
        table_widget.setRowCount(row_count)
        table_widget.setColumnCount(column_count)
        table_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)

        # Set Header Label
        header = table_widget.horizontalHeader()
        header.setStretchLastSection(True)
        header.setResizeMode(QHeaderView.Stretch)

        # Set Vertical Header
        table_widget.setVerticalHeaderLabels(labels)

        # Set Size Policy
        self.table_widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.table_widget.horizontalHeader().setVisible(False)

        # Set Colors
        stylesheet = "QHeaderView::section{Background-color:" + EditEntry.ACCENT_COLOR + \
                     ";border - radius:14px;}"
        self.table_widget.setStyleSheet(stylesheet)
        table_widget.setShowGrid(False)

        # Add Widget Items to Table
        for i in range(0, row_count):
            table_widget.setItem(0, i, items[i])

    def __setup__(self):
        """ Sets up UI """

        ''' Setup Display'''
        icon = QIcon(os.path.join(resources, "delete.png"))
        self.ui.delete_btn.setIcon(icon)

        ''' Connect Buttons '''
        self.ui.delete_btn.clicked.connect(self.delete_entry)
        self.ui.save_btn.clicked.connect(self.save_entry)
        self.ui.exit_btn.clicked.connect(self.exit)
        self.ui.composition_btn.clicked.connect(self.open_composition_selector)
        self.ui.file_btn.clicked.connect(self.open_select_file)

        ''' Get Data '''
        self.category = molecules_table.get_category(conn, str(self.mid))
        self.__load_entry__()
        self.original_data = self.get_table_data()
