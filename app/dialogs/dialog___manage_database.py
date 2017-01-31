# Author: Jasmine Oliveira
# Date: 11/12/2016

from PyQt4.QtGui import *

from analysis.composition import Composition, CompositionQuery
from app.dialogs.frames.manage_database.frame___manage_database import Ui_Dialog   # import frame
from config import conn
from dialog___composition_selector import CompositionSelector
from dialog___edit_entry import EditEntry
from images import *
from tables import molecules_table, experimentinfo_table, knowninfo_table, peaks_table
from ..events import display_question_message

class ManageDatabase(QDialog):

    ACCENT_COLOR = "#008080"

    def __init__(self, parent=None):
        super(ManageDatabase, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        ''' UI Options'''
        self.setWindowTitle("Manage Database")
        self.resize(1200, 750)
        self.show()

        ''' Data '''
        self.selected_mids = []
        self.current_mid = []

        ''' Widgets '''
        self.molecules_table_widget = self.ui.molecules_table
        self.info_table_widget = self.ui.info_table
        self.peaks_list_widget = self.ui.peak_table

        self.__setup__()

    def clear_selected(self):

        self.ui.experiment_chk.setChecked(False)
        self.ui.known_chk.setChecked(False)
        self.ui.artifact_chk.setChecked(False)

        self.ui.mhz_chk.setChecked(False)
        self.ui.ghz_chk.setChecked(False)
        self.ui.cm1_chk.setChecked(False)

        self.ui.temp_min_spinbx.setValue(0.0)
        self.ui.temp_max_spinbx.setValue(0.0)

        self.ui.dicharge_chk.setChecked(False)
        self.ui.heated_nozzle_chk.setChecked(False)
        self.ui.stable_chk.setChecked(False)
        self.ui.laser_ablation_chk.setChecked(False)

        self.ui.isotope_chk.setChecked(False)
        self.ui.vibrational_chk.setChecked(False)

    def delete_selected(self):
        action = display_question_message("Are you sure you want to remove this "
                                        "entry from the database? All information of this "
                                        "entry will be lost.",
                                        "Delete Entry")
        if action is True:
            molecules_table.remove_molecule(conn, self.current_mid)

        self.selected_mids.remove(self.current_mid)
        self.clear_tables()
        self.populate_molecule_table_widget(self.selected_mids)

    def clear_tables(self):
        self.molecules_table_widget.clear()
        self.info_table_widget.clear()
        self.peaks_list_widget.clear()

    def get_selected_categories(self):

        selected = []

        if self.ui.experiment_chk.isChecked():
            selected.append('experiment')

        if self.ui.known_chk.isChecked():
            selected.append('known')

        if self.ui.artifact_chk.isChecked():
            selected.append('artifact')

        return selected

    def get_selected_frequency_units(self):

        selected = []

        if self.ui.mhz_chk.isChecked():
            selected.append('MHz')
        if self.ui.cm1_chk.isChecked():
            selected.append('cm-1')
        if self.ui.ghz_chk.isChecked():
            selected.append('GHz')

        return selected

    def get_selected_experiment_types(self):

        selected = []

        if self.ui.dicharge_chk.isChecked():
            selected.append('Discharge')
        elif self.ui.stable_chk.isChecked():
            selected.append('Stable')
        elif self.ui.heated_nozzle_chk.isChecked():
            selected.append('Heated Nozzle')
        elif self.ui.laser_ablation_chk.isChecked():
            selected.append('Laser Ablation')

        return selected

    def go_back_to_main_menu(self):
        from dialog___main_menu import MainMenu  # Import Main Menu as (back_frame)
        self.close()
        window = MainMenu()
        window.exec_()

    def open_edit_entry(self):
        window = EditEntry(self.current_mid)
        window.exec_()

        if molecules_table.mid_exists(conn, self.current_mid):

            self.populate_info_table_widget(self.current_mid)
            self.populate_peak_table_widget(self.current_mid)
        else:
            self.selected_mids.remove(self.current_mid)

        self.populate_molecule_table_widget(molecules_table.get_all_mid_list(conn))

    def open_composition_selector(self):
        window = CompositionSelector(self.ui.composition_txt)
        window.exec_()

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
                self.populate_info_table_as_experiment(mid, table_widget)
            else:
                table_widget.clearContents()
                return
        elif category == "known":
            if knowninfo_table.info_exists(conn, mid):
                self.populate_info_table_as_known(mid, table_widget)
            else:
                table_widget.clearContents()
                return
        else:
            if knowninfo_table.info_exists(conn, mid):
                self.populate_info_table_as_artifact(mid, table_widget)
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

    ###############################################################################
    # Private Methods
    ###############################################################################

    def __filter_action(self):
        """ Gets appropriate mid list to display on the list widget"""

        print "FILTERING! "
        mids = []

        ''' Category '''
        categories = self.get_selected_categories()
        if len(categories) is not 0:
            mids = molecules_table.get_mids_where_category_in(conn, categories)
        else:
            mids = molecules_table.get_all_mid_list(conn)

        ''' Frequency Units '''
        frequency_units = self.get_selected_frequency_units()
        if len(frequency_units) is not 0:
            m2 = set(molecules_table.get_mids_where_units_in(conn, frequency_units))
            mids = list(set(mids) & set(m2))    # Intersection

        ''' Temperature '''
        min = None if self.ui.temp_min_spinbx.value() is 0 else self.ui.temp_min_spinbx.value()
        max = None if self.ui.temp_max_spinbx.value() is 0 else self.ui.temp_max_spinbx.value()
        if min or max:
            m2 = set(molecules_table.get_mids_in_temperature_range(conn, min, max))
            mids = list(set(mids) & set(m2))    # Intersection

        ''' Type '''
        types = self.get_selected_experiment_types()
        if len(types) is not 0:
            m2 = set(molecules_table.get_mids_where_types_in(conn, types))
            mids = list(set(mids) & set(m2))    # Intersection

        ''' Isotope '''
        if self.ui.isotope_chk.isChecked():
            m2 = set(molecules_table.get_mids_where_is_isotope(conn, True))
            mids = list(set(mids) & set(m2))  # Intersection

        ''' Vibrational '''
        if self.ui.vibrational_chk.isChecked():
            m2 = set(molecules_table.get_mids_where_is_vibrational(conn, True))
            mids = list(set(mids) & set(m2))    # Intersection

        ''' Composition '''
        text = Composition(str(self.ui.composition_txt.text()))
        if self.ui.composition_has_rdio.isChecked():
            m2 = CompositionQuery.have(conn, text)
            mids = list(set(mids) & set(m2))  # Intersection
        elif self.ui.composition_exactly_rdo.isChecked():
            m2 = CompositionQuery.is_exactly(conn, text)
            mids = list(set(mids) & set(m2))  # Intersection
        elif self.ui.composition_nothave_rdio.isChecked():
            m2 = CompositionQuery.not_have(conn, text)
            mids = list(set(mids) & set(m2))  # Intersection


        self.selected_mids = mids
        self.populate_molecule_table_widget(mids)

    def __handle_molecule_table_row_click(self):
        """
        Displays info and peaks to respective tables based on
        :return:
        """
        item = self.molecules_table_widget.selectedItems()[0]
        mid = int(item.text())
        self.current_mid = mid
        print mid
        self.populate_info_table_widget(mid)
        self.populate_peak_table_widget(mid)

    def __setup__(self):
        """
        Sets up the ui file
        """

        ''' Load data to Lists/Frames '''
        mids = molecules_table.get_all_mid_list(conn)
        self.selected_mids = mids
        self.populate_molecule_table_widget(mids)

        ''' Connect to Appropriate Functions'''
        self.molecules_table_widget.itemClicked.connect(self.__handle_molecule_table_row_click)
        self.ui.back_btn.clicked.connect(self.go_back_to_main_menu)
        self.ui.filter_btn.clicked.connect(self.__filter_action)
        self.ui.reset_btn.clicked.connect(self.clear_selected)
        self.ui.edit_btn.clicked.connect(self.open_edit_entry)
        self.ui.delete_btn.clicked.connect(self.delete_selected)
        self.ui.composition_btn.clicked.connect(self.open_composition_selector)

        ''' Display Options '''
        icon = QIcon(TRASH_ICON)
        self.ui.delete_btn.setIcon(icon)

        icon = QIcon(EDIT_ICON)
        self.ui.edit_btn.setIcon(icon)

    ###############################################################################
    # Static Methods
    ###############################################################################

    @staticmethod
    def populate_info_table_as_experiment(mid, table_widget):

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
    def populate_info_table_as_known(mid, table_widget):

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
    def populate_info_table_as_artifact(mid, table_widget):

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


