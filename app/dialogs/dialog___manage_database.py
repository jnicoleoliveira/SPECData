# Author: Jasmine Oliveira
# Date: 11/12/2016

from PyQt4.QtGui import *

from frames.frame___manage_database import Ui_Dialog   # import frame
from tables import molecules_table, experimentinfo_table, knowninfo_table, peaks_table
from config import conn

class ManageDatabase(QDialog):

    ACCENT_COLOR = "#008080"

    def __init__(self, parent=None):
        super(ManageDatabase, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        ''' UI Options'''
        self.setWindowTitle("Manage Database")
        self.resize(1500, 750)
        self.show()

        ''' Data '''
        self.selected_mids = []

        ''' Widgets '''
        self.molecules_table_widget = self.ui.molecules_table
        self.info_table_widget = self.ui.info_table
        self.peaks_list_widget = self.ui.peak_table

        self.__setup__()

    def __setup__(self):
        """
        Sets up the ui file
        """

        ''' Set default to All'''
        self.__load_default__()

        ''' Connect to Appropriate Functions'''
        self.molecules_table_widget.itemClicked.connect(self.handle_molecule_table_row_click)
        self.ui.back_btn.clicked.connect(self.go_back_to_main_menu)

    def go_back_to_main_menu(self):
        from dialog___main_menu import MainMenu  # Import Main Menu as (back_frame)
        self.close()
        window = MainMenu()
        window.exec_()

    def handle_molecule_table_row_click(self):
        """
        Displays info and peaks to respective tables based on
        :return:
        """
        item = self.molecules_table_widget.selectedItems()[0]
        mid = int(item.text())
        print mid
        self.populate_info_table_widget(mid)
        self.populate_peak_table_widget(mid)

    def __load_default__(self):
        """
        Checks off "all", and loads all molecules in database.
        """

        ''' Load data to Lists/Frames '''
        mids = molecules_table.get_all_mid_list(conn)
        self.populate_molecule_table_widget(mids)
        self.populate_info_table_widget(18)
        self.populate_peak_table_widget(18)

    def populate_molecule_list_widget(self, mids):
        """
        Populates list widget with Molecule entries of given mids
        """

        for i in range(0, len(mids)):
            mid = mids[i]
            name = molecules_table.get_name(conn, mid)
            category = molecules_table.get_category(conn, mid)
            line = str(mid) + "\t" + str(category) + "\t" + str(name)
            self.list_widget.addItem(QListWidgetItem(line))

    def populate_molecule_table_widget(self, mids):
        """
        Populates the molecule table widget with the appropriate values
        of the given list of mids
        :param mids: List of mids
        """
        table_widget = self.molecules_table_widget

        row_count = len(mids)   # Number of Rows
        column_count = 3        # Number of Columnns [mid, name, category]

        # Format Table
        table_widget.setRowCount(row_count)
        table_widget.setColumnCount(column_count)
        table_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        table_widget.setSortingEnabled(True)

        # Set Header Label
        header = table_widget.horizontalHeader()
        header.setStretchLastSection(True)
        header.setResizeMode(QHeaderView.Stretch)
        table_widget.setHorizontalHeaderLabels(["MID", "Name", "Category"])

        for i in range(0, row_count):

            # Get row data
            mid = mids[i]
            name = molecules_table.get_name(conn, mid)
            category = molecules_table.get_category(conn, mid)

            # Convert Data to QTableWidgetItem
            mid_item = QTableWidgetItem(str(mid))
            name_item = QTableWidgetItem(str(name))
            category_item = QTableWidgetItem(str(category))

            # Add Widget Items to Table
            table_widget.setItem(i, 0, mid_item)
            table_widget.setItem(i, 1, name_item)
            table_widget.setItem(i, 2, category_item)

        # --- Set Size Policy --- #
        table_widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        # -- Set Additional Options -- #
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # disallow in-table editing
        table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        table_widget.setShowGrid(False)
        table_widget.verticalHeader().setVisible(False)

        # -- Set Colors -- #
        stylesheet = "QHeaderView::section{Background-color:"+ ManageDatabase.ACCENT_COLOR + \
                     ";border - radius:14px;}"
        table_widget.setStyleSheet(stylesheet)

    def populate_info_table_widget(self, mid):
        """
        Populates the info table widget with the appropriate values
        of the given list of mid
        :param mid: A single mid
        """
        table_widget = self.info_table_widget

        category = molecules_table.get_category(conn,mid)
        print category
        if category == "experiment":
            if experimentinfo_table.info_exists(conn, mid):
                self.__populate_info_table_as_experiment(mid, table_widget)
            else:
                table_widget.clearContents()
                return
        elif category == "known":
            if knowninfo_table.info_exists(conn, mid):
                self.__populate_info_table_as_known(mid, table_widget)
            else:
                table_widget.clearContents()
                return
        else:
            if knowninfo_table.info_exists(conn, mid):
                self.__populate_info_table_as_artifact(mid, table_widget)
            else:
                table_widget.clearContents()
                return


        # --- Set Size Policy --- #
        table_widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        # -- Set Additional Options -- #
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # disallow in-table editing
        table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_widget.setShowGrid(False)
        table_widget.horizontalHeader().setVisible(False)

        # -- Set Colors -- #
        stylesheet = "QHeaderView::section{Background-color:" + ManageDatabase.ACCENT_COLOR + \
                     ";border - radius:14px;}"
        table_widget.setStyleSheet(stylesheet)

    def populate_peak_table_widget(self, mid):
        """
        Populates the molecule table widget with the appropriate values
        of the given list of mids
        :param mids: List of mids
        """
        table_widget = self.peaks_list_widget

        # Get Peaks
        frequencies, intensities = peaks_table.get_frequency_intensity_list(conn, mid)

        row_count = len(frequencies)   # Number of Rows
        column_count = 3             # Number of Columnns [mid, name, category]

        # Format Table
        table_widget.setRowCount(row_count)
        table_widget.setColumnCount(column_count)
        table_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        table_widget.setSortingEnabled(True)

        # Set Header Label
        header = table_widget.horizontalHeader()
        header.setStretchLastSection(True)
        header.setResizeMode(QHeaderView.Stretch)
        table_widget.setHorizontalHeaderLabels(["PID", "Frequency", "Intensity"])

        for i in range(0, row_count):

            # Get row data
            pid = i
            frequency = frequencies[i]
            intensity = intensities[i]

            # Convert Data to QTableWidgetItem
            pid_item = QTableWidgetItem(str(pid))
            freq_item = QTableWidgetItem(str(frequency))
            inte_item = QTableWidgetItem(str(intensity))

            # Add Widget Items to Table
            table_widget.setItem(i, 0, pid_item)
            table_widget.setItem(i, 1, freq_item)
            table_widget.setItem(i, 2, inte_item)

        # --- Set Size Policy --- #
        table_widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        # -- Set Additional Options -- #
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # disallow in-table editing
        table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_widget.setShowGrid(False)
        #table_widget.verticalHeader().setVisible(False)

        # -- Set Colors -- #
        stylesheet = "QHeaderView::section{Background-color:"+ ManageDatabase.ACCENT_COLOR + \
                     ";border - radius:14px;}"
        table_widget.setStyleSheet(stylesheet)

    @staticmethod
    def __populate_info_table_as_experiment(mid, table_widget):

        row_count = 6  # Number of Rows
        column_count = 1  # Number of Columnns [mid, name, category]

        # Format Table
        table_widget.setRowCount(row_count)
        table_widget.setColumnCount(column_count)
        table_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        table_widget.setSortingEnabled(True)

        # Set Header Label
        header = table_widget.horizontalHeader()
        header.setStretchLastSection(True)
        header.setResizeMode(QHeaderView.Stretch)

        # Set Vertical Header
        table_widget.setVerticalHeaderLabels(["EID", "Type", "Units", "Composition",
                                              "Notes", "Last-Updated"])
        # Get row data
        eid = experimentinfo_table.get_eid(conn, mid)
        type = experimentinfo_table.get_type(conn, mid)
        units = experimentinfo_table.get_units(conn, mid)
        composition = experimentinfo_table.get_composition(conn, mid)
        notes = experimentinfo_table.get_notes(conn, mid)
        updated = experimentinfo_table.get_last_updated(conn, mid)

        # Convert Data to QTableWidgetItem
        eid_item = QTableWidgetItem(str(eid))
        type_item = QTableWidgetItem(str(type))
        units_item = QTableWidgetItem(str(units))
        composition_item = QTableWidgetItem(str(composition))
        notes_item = QTableWidgetItem(str(notes))
        updated_item = QTableWidgetItem(str(updated))

        # Add Widget Items to Table
        table_widget.setItem(0, 0, eid_item)
        table_widget.setItem(0, 1, type_item)
        table_widget.setItem(0, 2, units_item)
        table_widget.setItem(0, 3, composition_item)
        table_widget.setItem(0, 4, notes_item)
        table_widget.setItem(0, 5, updated_item)

    @staticmethod
    def __populate_info_table_as_known(mid, table_widget):

        row_count = 8  # Number of Rows
        column_count = 1  # Number of Columnns [mid, name, category]

        # Format Table
        table_widget.setRowCount(row_count)
        table_widget.setColumnCount(column_count)
        table_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        table_widget.setSortingEnabled(True)

        # Set Header Label
        header = table_widget.horizontalHeader()
        header.setStretchLastSection(True)
        header.setResizeMode(QHeaderView.Stretch)

        # Set Vertical Header
        table_widget.setVerticalHeaderLabels(["KID", "Units", "Temperature", "Composition",
                                              "Isotope", "Vibrational", "Notes", "Last-Updated"])
        # Get row data
        kid = knowninfo_table.get_kid(conn, mid)
        units = knowninfo_table.get_units(conn, mid)
        temperature = knowninfo_table.get_temperature(conn, mid)
        composition = knowninfo_table.get_composition(conn, mid)
        isotope = knowninfo_table.is_isotype(conn, mid)
        vibrational = knowninfo_table.is_vibrational(conn, mid)
        notes = knowninfo_table.get_notes(conn, mid)
        updated = knowninfo_table.get_last_updated(conn, mid)


        # Convert Data to QTableWidgetItem
        eid_item = QTableWidgetItem(str(mid))
        units_item = QTableWidgetItem(str(units))
        temperature_item = QTableWidgetItem(str(temperature))
        composition_item = QTableWidgetItem(str(composition))
        isotope_item = QTableWidgetItem(str(isotope))
        vibrational_item = QTableWidgetItem(str(vibrational))
        notes_item = QTableWidgetItem(str(notes))
        updated_item = QTableWidgetItem(str(updated))

        # Add Widget Items to Table
        table_widget.setItem(0, 0, eid_item)
        table_widget.setItem(0, 1, units_item)
        table_widget.setItem(0, 2, temperature_item)
        table_widget.setItem(0, 3, composition_item)
        table_widget.setItem(0, 4, isotope_item)
        table_widget.setItem(0, 5, vibrational_item)
        table_widget.setItem(0, 6, notes_item)
        table_widget.setItem(0, 7, updated_item)

    @staticmethod
    def __populate_info_table_as_artifact(mid, table_widget):

        row_count = 3  # Number of Rows
        column_count = 1  # Number of Columnns [mid, name, category]

        # Format Table
        table_widget.setRowCount(row_count)
        table_widget.setColumnCount(column_count)
        table_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        table_widget.setSortingEnabled(True)

        # Set Header Label
        header = table_widget.horizontalHeader()
        header.setStretchLastSection(True)
        header.setResizeMode(QHeaderView.Stretch)

        # Set Vertical Header
        table_widget.setVerticalHeaderLabels(["KID", "Notes", "Last-Updated"])
        # Get row data
        kid = knowninfo_table.get_kid(conn, mid)
        notes = knowninfo_table.get_notes(conn, mid)
        updated = knowninfo_table.get_last_updated(conn, mid)

        # Convert Data to QTableWidgetItem
        eid_item = QTableWidgetItem(str(mid))
        notes_item = QTableWidgetItem(str(notes))
        updated_item = QTableWidgetItem(str(updated))

        # Add Widget Items to Table
        table_widget.setItem(0, 0, eid_item)
        table_widget.setItem(0, 1, notes_item)
        table_widget.setItem(0, 2, updated_item)
