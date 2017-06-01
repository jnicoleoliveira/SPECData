# Author: Jasmine Oliveira
# Date: 08/24/2016

import sys
from copy import deepcopy

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget

import images
from analysis import experiment
from app.dialogs.frames.experiment_view.frame___experiment_view import Ui_MainWindow
from app.events import LoadingProgressScreen, save_as_file, display_informative_message
from app.experiment_analysis import MainGraph
from app.time_machine import TimeMachine
from app.widgets.widget___experiment_info import ExperimentInfoWidget
from app.widgets.widget___graph_toolbox_dock import GraphToolBoxDock
from app.widgets.widget___main_graph_options import MainGraphOptionsWidget
from app.widgets.widget___molecule_selection import MoleculeSelectionWidget
from app.widgets.widget___rotated_button import RotatedButton
from app.widgets.widget___splatalogue_dock import SplatalogueDockWidget
from config import *


class ExperimentView(QMainWindow):
    """
    Experiment View
    """

    # Define Colors
    COLOR_PENDING = "#D4AC0D"
    COLOR_INVALID = "#A93226"
    COLOR_VALID = "#229954"

    def __init__(self, experiment_name, mid, parent=None):
        super(ExperimentView, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ''' Window Settings '''
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowIcon(QIcon(QPixmap(images.LOGO_ICON)))

        self.setWindowTitle("Experiment View")
        self.resize(1800, 900)

        ''' Status '''
        self.setup_done = False

        ''' Widgets '''
        # -- Graph  -- #
        self.matplot_widget = None
        # -- Graph Options -- #
        self.graph_options_widget = None
        # -- Experiment Info Widget -- #
        self.info_widget = None
        # -- Splatalogue Dock Widget -- #
        self.splatalogue_dock_widget = None
        # -- Molecule Selection Widgets -- #
        self.selection_widget = None                # Pending
        self.validated_selection_widget = None      # Accepted
        self.invalidated_selection_widget = None    # Rejected
        # -- Selection Containers -- #
        self.selection_tab_widget = None
        self.pending_scroll_selection_container = None
        self.validated_scroll_selection_container = None
        self.invalidated_scroll_selection_container = None
        # -- Table Widget -- #
        self.table_widget = None
        # -- Buttons -- #
        self.redisplay_btn = None       # Redisplay (Redisplay __setup_graph with current selections)
        self.select_all_btn = None      # Select all (for molecule selection)
        self.deselect_all_btn = None    # Deselect all (for molecule selection)
        self.main_menu_btn = None       # Main Menu (exits, returns to main menu)
        self.delete_btn = None          # Delete Button, removes associated lines from analysis

        ''' Toolboxes '''
        self.info_toolbox = None
        self.graph_toolbox = None
        self.table_toolbox = None


        ''' Undo/Redo (Time Machine) '''
        self.time_machine = None
        self.undo_action = None     # action_bar undo button
        self.redo_action = None     # action_bar redo button

        ''' Menu Bar '''
        self.action_show_validations = None
        self.show_validations_on_graph = True

        ''' Data '''
        self.experiment = None          # Experiment Object
        self.experiment_graph = None    # ExperimentGraph Object
        self.loading_screen = None      # LoadingProgressScreen Object

        '''Start Up'''
        self.__setup__(experiment_name, mid)
        self.show()
        self.cid_pick = self.matplot_widget.getFigure().canvas.mpl_connect('pick_event', self.__on_graph_line_pick)

    ###############################################################################
    # Toolbar Methods
    ###############################################################################
    def do_analysis(self):
        self.experiment.get_assigned_molecules()

    def export_cleaned_lines(self):
        from dialog___export_cleaned_lines import ExportCleanedLines
        window = ExportCleanedLines(self.experiment)
        window.exec_()

    def export_analysis_summary(self):
        from analysis.experiment_write_up import export_analysis_summary
        # Open Save File Event
        text_box = QLineEdit()  # Temp widget
        save_as_file(text_box, ".txt")

        # Retrieve path
        path = text_box.text()

        # Do Export : make sure name before ext is not empty
        if path is not None and path.split(".")[0] != "":
            export_analysis_summary(self.experiment, path)
            display_informative_message("Export Complete!")

    def export_assignment_data(self):
        from analysis.experiment_write_up import export_assignment_data
        # Open Save File Event
        text_box = QLineEdit()  # Temp widget
        save_as_file(text_box, ".csv")

        # Retrieve path
        path = text_box.text()

        # Do Export : make sure name before ext is not empty
        if path is not None and path.split(".")[0] != "":
            export_assignment_data(self.experiment, path)
            display_informative_message("Export Complete!")

    def go_to_main_menu(self):
        from app.dialogs.dialog___main_menu import MainMenu
        window = MainMenu()
        # self.close()
        self.hide()
        window.show()
        window.exec_()
        # self.clse()

    def add_a_molecule(self):
        from dialog___add_a_molecule import AddAMolecule
        window = AddAMolecule(self.selection_widget, self.experiment)
        window.exec_()

    def save_analysis(self):
        self.experiment.save_affirmed_matches(True)
        display_informative_message("Save Complete!")

    ###############################################################################
    # Selection Widget Functions
    ###############################################################################

    def deselect_all(self):
        """
        Select all button function.
        Checks all selections in selection widget
        """
        current_widget = self.current_selection_widget()
        current_widget.deselect_all()

    def invalidate_selections(self, save=True):

        # -- Get currently selected widget -- #
        current_widget = self.current_selection_widget()

        # -- Get Selected Mids -- #
        selected_mids = current_widget.get_selected_mids()

        # -- Validate Selections in Experiment -- #
        for mid in selected_mids:
            self.experiment.invalidate_a_match(mid)

        # Remove selected rows, and get those selections #
        matches, colors = current_widget.remove_selections()

        for i in range(0, len(matches)):
            self.invalidated_selection_widget.add_row(matches[i], colors[i])

        # Repopulate table widget to show updated validations
        self.populate_table_widget()

        if save:
            self.__save_state()

        self.update_info()

        if self.setup_done is True:
            # Refresh Dependent Widgets
            self.splatalogue_dock_widget.refresh_analysis()

        # Regraph
        try:
            self.select_all()
            self.redisplay_graph()
            self.deselect_all()
        except AttributeError:
            self.deselect_all()

    def get_selections(self):
        return self.selection_widget.get_selections()

    def populate_selection_widget(self):
        self.selection_widget.add_all(self.experiment.get_sorted_molecule_matches())

    def organize_matches(self):
        elements = self.selection_widget.get_elements()
        self.deselect_all()
        # Validated
        for key, value in elements.iteritems():
            if value.match.is_validated():
                value.checkbox.click()

        self.validate_selections(save=False)
        self.deselect_all()

        # Validated
        for key, value in elements.iteritems():
            if value.match.is_invalidated():
                value.checkbox.click()

        self.invalidate_selections(save=False)
        self.select_all()

    def select_all(self):
        """
        Select all button function.
        Checks all selections in selection widget
        """
        current_widget = self.current_selection_widget()
        current_widget.select_all()

    def validate_selections(self, save=True):
        # -- Get currently selected widget -- #
        current_widget = self.current_selection_widget()

        # -- Get Selected Mids -- #
        selected_mids = current_widget.get_selected_mids()

        # -- Validate Selections in Experiment -- #
        for mid in selected_mids:
            self.experiment.validate_a_match(mid)

        # Remove selected rows, and get those selections #
        matches, colors = current_widget.remove_selections()

        for i in range(0, len(matches)):
            self.validated_selection_widget.add_row(matches[i], colors[i])

        # Repopulate table widget to show updated validations
        self.populate_table_widget()

        if save:
            self.__save_state()
        self.update_info()

        if self.setup_done is True:
            # Refresh Dependent Widgets
            self.splatalogue_dock_widget.refresh_analysis()

        # Regraph
        try:
            self.select_all()
            self.redisplay_graph()
            self.deselect_all()
        except AttributeError:
            self.deselect_all()

    def current_selection_widget(self):
        return self.selection_tab_widget.currentWidget().widget()

    ###############################################################################
    # Table Widget Functions
    ###############################################################################

    def highlight_table_row(self, frequency):
        """
        Highlights corresponding rows with the parameter pid
        :param frequency
        """
        # -- Set table to Multi Selection Mode -- #
        self.table_widget.setSelectionMode(QAbstractItemView.MultiSelection)

        # -- Get items that match pid -- #
        items = self.table_widget.findItems(QString(str(frequency)), Qt.MatchExactly)

        # -- Select rows of matched items -- #
        for item in items:
            self.table_widget.selectRow(item.row())

        # -- Set table back to Extended Selection Mode -- #
        self.table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def populate_table_widget(self):
        """
        Populate table_widget with the following __setup_graph data:
            Experiment PID, Frequency, Intensity with its associative
            match's PID, frequency, and intensity
        """
        import tables.peaks_table as peaks_table
        from config import conn
        matches = self.experiment.get_all_matches_list()
        unassigned = self.experiment.get_unassigned_peaks()
        row_count = len(matches) + len(unassigned)  # Number of values
        column_count = 5         # Columns

        # Format Table
        self.table_widget.setRowCount(row_count)
        self.table_widget.setColumnCount(column_count)
        self.table_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.table_widget.setSortingEnabled(True)

        # Set Header Label
        self.table_widget.setHorizontalHeaderLabels(["Exp PID", "Frequency", "Intensity",
                                                     "Match", "Status"])

        for i in range(0, row_count):

            if i >= len(matches):
                index = i - len(matches)
                exp_pid = unassigned[index].pid
                exp_frequency = unassigned[index].frequency
                exp_intensity = unassigned[index].intensity
                name = "-"
                mid = "-"
                status = "unassigned"
            else:
                # Get Row Data
                exp_pid = matches[i].exp_pid
                exp_frequency, exp_intensity = peaks_table.get_frequency_intensity(conn, exp_pid)
                name = matches[i].name
                mid = matches[i].mid
                status = "pending"

                # Determine if status is valid
                if self.experiment.is_validated_molecule(mid):
                    status = "valid"
                elif self.experiment.is_invalidated_molecule(mid):
                    name = "-"
                    mid = "-"
                    status = "unassigned"

            # Convert Data to QTableWidgetItem
            exp_pid_item = QTableWidgetItem(str(exp_pid))
            exp_frequency_item = QTableWidgetItem(str(exp_frequency))
            exp_intensity_item = QTableWidgetItem(str(exp_intensity))
            name_item = QTableWidgetItem(name)
            status_item = QTableWidgetItem(status)

            # Get status color, default pending status is black
            if status is not "unassigned":
                if status is "valid":
                    color = QColor(self.COLOR_VALID)
                elif status is "pending":
                    color = QColor(self.COLOR_PENDING)
                name_item.setBackgroundColor(color)
                status_item.setBackgroundColor(color)

            # Add Widget Items to Table
            self.table_widget.setItem(i, 0, exp_pid_item)
            self.table_widget.setItem(i, 1, exp_frequency_item)
            self.table_widget.setItem(i, 2, exp_intensity_item)
            self.table_widget.setItem(i, 3, name_item)
            self.table_widget.setItem(i, 4, status_item)

        # --- Set Size Policy --- #
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

        # -- Set Additional Options -- #
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # disallow in-table editing

        #width = self.table_widget.horizontalHeader().width()
        #self.table_widget.setFixedWidth(width)
        #self.table_widget.setMaximumWidth(width)

    ###############################################################################
    # Graphing Widget Functions
    ###############################################################################

    def determine_graphing_options(self):

        # -- Get Values for Options -- #
        full_spectrum = self.graph_toolbox.full_spectrum_slider.is_toggled_on()
        show_validations = self.graph_toolbox.show_validations_slider.is_toggled_on()
        if show_validations is False:
            self.validated_selection_widget.deselect_all()

        sharey = self.graph_toolbox.share_yaxis_slider.is_toggled_on()
        y_to_experiment_intensities = self.graph_toolbox.share_intensities_slider.is_toggled_on()

        #full_spectrum = self.graph_options_widget.full_spectrum_chk.isChecked()
        #sharey = self.graph_options_widget.sharey_chk.isChecked()
        color_experiment = self.graph_options_widget.color_experiment_chk.isChecked()
        #y_to_experiment_intensities = self.graph_options_widget.y_exp_intensities_chk.isChecked()
        #show_validations = self.show_validations_on_graph

        # Set Options in __setup_graph #
        self.experiment_graph.set_options(full_spectrum=full_spectrum, sharey=sharey,
                                          y_to_experiment_intensities=y_to_experiment_intensities,
                                          color_experiment=color_experiment, show_validations=show_validations)

    def redisplay_graph(self):
        """
        Redisplay button function.
        Clears current experiment __setup_graph, and redisplays __setup_graph from checkbox selections.
        """

        # xlim, ylim = self.experiment_graph.get_zoom_coordinates()
        # print str(xlim) + " " + str(ylim)

        # Clear Graph
        self.experiment_graph.clear()

        # Get options
        self.determine_graphing_options()

        # Determine graphing selections
        matches, colors = self.selection_widget.get_selections()

        if self.show_validations_on_graph:
            valid_matches, valid_colors = self.validated_selection_widget.get_selections()
            matches.extend(valid_matches)
            colors.extend(valid_colors)

        # Graph
        self.experiment_graph.graph(matches, colors)

        # Draw
        self.experiment_graph.draw()
        self.cid_pick = self.matplot_widget.getFigure().canvas.mpl_connect('pick_event', self.__on_graph_line_pick)

    def reset_options(self):
        self.graph_toolbox.reset()

    def toggle_validations_on_graph(self):
        """
        Process action_show_validations button.
        :return:
        """
        if self.show_validations_on_graph is True:
            self.show_validations_on_graph = False
            self.action_show_validations.setIcon\
                (QIcon(QPixmap(os.path.join(resources, 'show-validations-off.png'))))
        else:
            self.show_validations_on_graph = True
            self.action_show_validations.setIcon \
                (QIcon(QPixmap(os.path.join(resources, 'show-validations.png'))))

            # print "Show Validations: " + str(self.show_validations_on_graph)

    def __on_graph_line_pick(self, event):
        """
        When picking a line on the __setup_graph, highlights associated
        row in the table-widget.
        :param event:
        """
        # print str(event.xdata)
        rect = event.artist
        x,y = rect.xy
        self.highlight_table_row(x)

        #print (rect.xy)
        # print "picked x" + str(x)

    ###############################################################################
    # Time Machine Functions
    ###############################################################################

    def undo(self):
        state = self.time_machine.undo()
        self.__restore_state(state)

        self.redo_action.setIcon(QIcon(images.REDO))
        self.redo_action.setEnabled(True)

        if self.time_machine.can_undo is False:
            self.undo_action.setEnabled(False)
            self.undo_action.setIcon(QIcon(images.UNDO_DISABLED))
        else:
            self.undo_action.setEnabled(True)
            self.undo_action.setIcon(QIcon(images.UNDO))

    def redo(self):
        state = self.time_machine.redo()
        self.__restore_state(state)

        if self.time_machine.can_redo() is False:
            self.redo_action.setIcon(QIcon(images.REDO_DISABLED))
            self.redo_action.setEnabled(False)

    def __restore_state(self, state):
        """
        Restores the data from a given state object.
        :param state:
        :return:
        """
        if state is None:
            return

        ''' Selection Widgets '''
        pending_data = state.pending_matches
        accepted_data = state.accepted_matches
        rejected_data = state.rejected_matches

        self.selection_widget.set_matches(pending_data[0], pending_data[1])
        self.invalidated_selection_widget.set_matches(rejected_data[0], rejected_data[1])
        self.validated_selection_widget.set_matches(accepted_data[0], accepted_data[1])

        ''' Experiment Data '''

        experiment = state.experiment
        self.experiment.validated_matches = deepcopy(experiment.validated_matches)
        self.experiment.molecule_matches = deepcopy(experiment.molecule_matches)
        self.experiment.experiment_peaks = deepcopy(experiment.experiment_peaks)
        self.populate_table_widget()

        # print "*****************"
        # print self.experiment.validated_matches
        # for m in self.experiment.get_sorted_molecule_matches():
        #     print str(m.mid) + "    " + m.status
        # print "*****************"

        self.info_widget.update(self.experiment)
        self.splatalogue_dock_widget.refresh_analysis()
        #self.experiment.validated_matches = experiment_data.validated_matches

    def __save_state(self):
        """
        Saves the current state by adding it to the TimeMachine.
        :return:
        """
        state = State(self.experiment,
                      self.selection_widget,
                      self.validated_selection_widget,
                      self.invalidated_selection_widget)
        self.time_machine.add_state(state)

    ###############################################################################
    # Setup Functions
    ###############################################################################
    def __setup__(self, experiment_name, mid):
        """
        Start-up example, does the following behind a loading progress screen:
        (1) Creates experiment from mid and experiment_name
        (2) Does Experiment analysis
        (3) Sets up layout with respective analysis data
        (4) Draws __setup_graph
        :param experiment_name: Experiment name
        :param mid: Experiment molecule ID
        """

        '''Start Loading Screen'''
        self.loading_screen = LoadingProgressScreen()
        self.loading_screen.start()     # Start Loading Screen

        # -- Do Things -- #

        ''' Create Experiment '''
        self.loading_screen.set_caption('Creating experiment...')
        self.experiment = experiment.Experiment(experiment_name, mid)  # Create experiment obj
        self.loading_screen.next_value(20)

        '''Analyze Experiment'''
        self.loading_screen.set_caption('Analyzing...')
        self.do_analysis()                      # Run Analysis
        self.loading_screen.next_value(40)

        '''Setup Layout'''
        self.loading_screen.set_caption('Setting up...')
        self.__setup_layout()                     # Setup Layout
        self.loading_screen.next_value(60)

        ''' Setup Splatalogue Dock Widget '''
        self.splatalogue_dock_widget.__setup__()  # Note: Setup here, to stop pop-up windows in load

        '''Add Assignments to Selection Widget'''
        self.populate_selection_widget()        # Add assignments
        self.organize_matches()
        self.loading_screen.next_value(80)

        '''Graph Main Graph'''
        self.__setup_graph()                            # Graph
        self.loading_screen.next_value(90)

        ''' Setup User History Time Machine '''
        base_state = State(self.experiment,
                           self.selection_widget,
                           self.validated_selection_widget,
                           self.invalidated_selection_widget)
        self.time_machine = TimeMachine(base_state, 20)

        self.deselect_all()  # deselect all
        # -- Stop Doing Things -- #

        '''End Loading Screen'''
        self.loading_screen.end()

    def __setup_graph(self):
        # Get Info for Experiment __setup_graph
        self.experiment_graph = MainGraph(self.matplot_widget, self.graph_options_widget, self.experiment)
        matches, colors = self.selection_widget.get_selections()

        # Graph
        self.experiment_graph.graph(matches, colors)

        # Draw Subplots
        self.experiment_graph.draw()

        if self.experiment_graph.full_spectrum_exists() is False:
            self.graph_options_widget.full_spectrum_chk.setEnabled(False)
            self.graph_options_widget.full_spectrum_chk.setWhatsThis("Data not available.")
            self.graph_options_widget.full_spectrum_chk.setStyleSheet("color: rgb(85, 85, 85);")

    def __setup_layout(self):
        """
        Sets up default layout of ExperimentView
        """

        '''
        Set-up QMainWindow layout
        '''
        layout = QGridLayout()  # Create Grid Layout

        # QMainWindow requires central widget
        # Created blank QWidget, and set layout to GridLayout
        outer_layout = QGridLayout()
        widget = QWidget()
        widget.setLayout(outer_layout)
        self.setCentralWidget(widget)
        '''
        Set-up Widgets
        '''
        # -- Graph  -- #
        self.matplot_widget = MatplotlibWidget()
        # -- Graph Options -- #
        self.graph_options_widget = MainGraphOptionsWidget()
        self.graph_toolbox = GraphToolBoxDock()
        # -- Molecule Selection Widget -- #
        self.selection_widget = MoleculeSelectionWidget(self.experiment)
        # -- Validated Selection Widget --#
        self.validated_selection_widget = MoleculeSelectionWidget(self.experiment)
        # -- Invalidated Selection Widget --#
        self.invalidated_selection_widget = MoleculeSelectionWidget(self.experiment)
        # -- Experiment Info Widget -- #
        self.info_widget = ExperimentInfoWidget(self.experiment)
        # -- Buttons -- #
        self.main_menu_btn = QPushButton()       # Main Menu (exits, returns to main menu)
        # --  Table -- #
        self.table_widget = QTableWidget()       # Table Widget (molecule assignment and peaks)
        self.populate_table_widget()
        # -- Splatalogue Widget -- #
        self.splatalogue_dock_widget = SplatalogueDockWidget(self.experiment)

        '''
        Create Inner Layouts / Containers
        '''

        # ------------------------------------------------------------------ #
        # Create Docked Tool Box Widget
        # ------------------------------------------------------------------ #
        # --- 1st Tab: Graph options
        # --- 2nd Tab : Peak List

        # Create Tool Box
        # tool_box = QToolBox()
        # #text = QString("Graph Options")
        # text = QString("Experiment Info")
        # #self.table_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        # #tool_box.addItem(self.info_widget, text)
        #
        # #tool_box.addItem(self.graph_options_widget, text)
        # tool_box.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        # text = QString("Peak List")
        # #tool_box.addItem(self.table_widget, text)

        # Dock the tool box
        # dock_tools = QDockWidget(self.window())
        # dock_tools.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        # dock_tools.setFeatures(QDockWidget.DockWidgetClosable |
        #                        QDockWidget.DockWidgetMovable |
        #                        QDockWidget.DockWidgetFloatable |
        #                        QDockWidget.DockWidgetVerticalTitleBar)

        # ------------------------------------------------------------------ #
        # Molecule Selection Widgets in Tabs (Pending, Validated, Invalidated)
        # ------------------------------------------------------------------ #
        # --- 1st tab: Pending
        # --- 2nd tab: Validated
        # --- 3rd tab: Invalidated

        # 1st Container (pending)
        pending_scroll_selection_container = QScrollArea()
        pending_scroll_selection_container.setWidget(self.selection_widget)
        pending_scroll_selection_container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        pending_scroll_selection_container.setFrameShadow(QFrame.Raised)

        # 2nd Container (validated)
        validated_scroll_selection_container= QScrollArea()
        validated_scroll_selection_container.setWidget(self.validated_selection_widget)
        validated_scroll_selection_container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        validated_scroll_selection_container.setFrameShadow(QFrame.Raised)

        # 2nd Container (validated)
        invalidated_scroll_selection_container = QScrollArea()
        invalidated_scroll_selection_container.setWidget(self.invalidated_selection_widget)
        invalidated_scroll_selection_container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        invalidated_scroll_selection_container.setFrameShadow(QFrame.Raised)

        # Create Tab Widget
        selection_tab_widget = QTabWidget()
        selection_tab_widget.addTab(pending_scroll_selection_container, "Pending")
        selection_tab_widget.addTab(validated_scroll_selection_container, "Validated")
        selection_tab_widget.addTab(invalidated_scroll_selection_container, "Invalidated")

        selection_tab_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.selection_tab_widget = selection_tab_widget
        # self.selection_tab_widget.setAutoFillBackground(True)
        # self.selection_tab_widget.setStyleSheet("background-color: #353535")
        self.selection_tab_widget.tabBar().setAutoFillBackground(True)

        # self.selection_tab_widget.tabBar().setStyleSheet("color:white; background")  # tab color fix (windows)
        self.selection_tab_widget.setStyleSheet('QTabBar::tab {background-color: #333333; font-size: 12px;'
                                                'border: 2px solid #262626; border-style: outset;} '
                                                'QTabBar {background-color: #262626;}')
        # Save
        self.pending_scroll_selection_container = pending_scroll_selection_container
        self.validated_scroll_selection_container = validated_scroll_selection_container
        self.invalidated_scroll_selection_container = invalidated_scroll_selection_container

        ''' Dock Widgets '''
        self.table_toolbox = QDockWidget()
        self.table_toolbox.setWidget(self.table_widget)
        # dock_tools.setWidget(tool_box)

        self.info_toolbox = QDockWidget()
        self.info_toolbox.setWidget(self.info_widget)
        self.info_toolbox.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)


        '''
        Add widgets to Layout
        '''

        hlayout = QHBoxLayout()
        v1 = QVBoxLayout()
        v3 = QVBoxLayout()
        v2 = QVBoxLayout()

        #v3.addWidget(self.info_widget)
        #v3.addWidget(self.table_widget)
        v1.addWidget(selection_tab_widget)
        v2.addWidget(self.matplot_widget)

        hlayout.addLayout(v3)
        hlayout.addLayout(v1)
        hlayout.addLayout(v2)

        outer_layout.addLayout(hlayout, 0, 0)

        self.window().addDockWidget(Qt.LeftDockWidgetArea, self.info_toolbox)
        self.window().addDockWidget(Qt.LeftDockWidgetArea, self.table_toolbox)
        self.window().addDockWidget(Qt.RightDockWidgetArea, self.graph_toolbox)
        self.window().addDockWidget(Qt.RightDockWidgetArea, self.splatalogue_dock_widget)
        self.graph_toolbox.hide()
        self.splatalogue_dock_widget.hide()

        self.table_widget.setMaximumWidth(450)

        '''
        Toolbar and ShortCuts
        '''
        self.__setup_toolbar_and_shortcuts()

        ''' Button Connections '''
        self.graph_options_widget.deselect_all_btn.clicked.connect(self.deselect_all)
        self.graph_options_widget.redisplay_btn.clicked.connect(self.redisplay_graph)
        self.graph_options_widget.select_all_btn.clicked.connect(self.select_all)
        self.graph_options_widget.show_validations_btn.clicked.connect(self.toggle_validations_on_graph)
        self.graph_toolbox.ui.reset_btn.clicked.connect(self.reset_options)
        self.graph_toolbox.ui.graph_btn.clicked.connect(self.redisplay_graph)

    def __setup_toolbar_and_shortcuts(self):

        self.ui.menu_bar.setStyleSheet("""QMenuBar::item {
             background-color: #353535;
        }""")
        action_bar = self.ui.action_bar
        action_bar.setMovable(False)
        # action_bar.setAutoFillBackground(True)
        # self.setStyleSheet("background-color: #353535; color:white;")

        #self.ui.action_bar.setStyleSheet("color: gray")

        ''' Home Button '''
        pix_map = QPixmap(os.path.join(resources, 'home.png'))
        action_bar.addAction(QIcon(pix_map), "Main Menu", self.go_to_main_menu)

        ''' Save Button'''
        # -- Toolbar - #
        pix_map = QPixmap(os.path.join(resources, 'save-button.png'))
        action_bar.addAction(QIcon(pix_map), "Save Analysis (Ctrl+S)", self.save_analysis)
        # Short cut
        self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_S), self),
                     SIGNAL('activated()'), self.save_analysis)

        action_bar.addSeparator()
        ##############################################
        ''' Undo '''
        # -- Toolbar - #
        action = QAction("Undo (Ctrl+Z)", self)
        action.setIcon(QIcon(os.path.join(resources, 'undo-disabled.png')))
        action.triggered.connect(self.undo)
        action_bar.addAction(action)
        self.undo_action = action

        # Short cut
        self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Z), self),
                     SIGNAL('activated()'), self.undo)
        ''' Redo '''
        # -- Toolbar - #
        action = QAction("Redo (Ctrl+Shift+Z)", self)
        action.setIcon(QIcon(os.path.join(resources, 'redo-disabled.png')))
        action.triggered.connect(self.redo)
        action_bar.addAction(action)
        self.redo_action = action

        # Short cut
        self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_Z), self),
                     SIGNAL('activated()'), self.redo)

        action_bar.addSeparator()
        ##############################################
        # ''' Redisplay Button'''
        # # -- Toolbar - #
        # pix_map = QPixmap(os.path.join(resources, 'redisplay-graph.png'))
        # action_bar.addAction(QIcon(pix_map), "Redisplay Graph (F5)", self.redisplay_graph)
        # # Short cut
        # self.connect(QShortcut(QKeySequence(Qt.Key_F5), self),
        #              SIGNAL('activated()'), self.redisplay_graph)

        ''' Select All '''
        # -- Toolbar - #
        pix_map = QPixmap(os.path.join(resources, 'select-all.png'))
        action_bar.addAction(QIcon(pix_map), "Select All (Ctrl+A)", self.select_all)
        # Short cut
        self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_A), self),
                     SIGNAL('activated()'), self.select_all)

        ''' Deselect All '''
        # -- Toolbar - #
        pix_map = QPixmap(os.path.join(resources, 'deselect-all.png'))
        action_bar.addAction(QIcon(pix_map), "Deselect All (Ctrl+D)", self.deselect_all)
        # Short cut
        self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_D), self),
                     SIGNAL('activated()'), self.deselect_all)

        # ''' Show Validations '''
        # # -- Toolbar -- #
        # pix_map = QPixmap(os.path.join(resources, 'show-validations.png'))
        # self.action_show_validations = QAction("Show Validations", self)
        # self.action_show_validations.setIcon(QIcon(pix_map))
        # self.action_show_validations.setIconText("Show Validations")
        # self.action_show_validations.triggered.connect(self.toggle_validations_on_graph)
        # action_bar.addAction(self.action_show_validations)
        # #action_bar.triggered[QAction].connect(self.toggle_validations_on_graph)
        # #action_bar.addAction(QIcon(pix_map), "Show Validations", self.toggle_validations_on_graph)

        ##############################################
        action_bar.addSeparator()
        ##############################################

        ''' Validate Selections '''
        # -- Toolbar - #
        pix_map = QPixmap(os.path.join(resources, 'validate.png'))
        action_bar.addAction(QIcon(pix_map), "Validate Selections", self.validate_selections)

        ''' Invalidate Selections'''
        # -- Toolbar - #
        pix_map = QPixmap(os.path.join(resources, 'invalidate.png'))
        action_bar.addAction(QIcon(pix_map), "Invalidate Selections", self.invalidate_selections)

        ##############################################
        action_bar.addSeparator()
        ##############################################

        ''' Re-Analyze'''
        # -- Toolbar - #
        pix_map = QPixmap(os.path.join(resources, 're-analyze.png'))
        action_bar.addAction(QIcon(pix_map), "Re-Analyze", self.redo_analysis)

        ''' Analysis Settings '''
        # -- Toolbar - #
        pix_map = QPixmap(os.path.join(resources, 'analysis-settings.png'))
        action_bar.addAction(QIcon(pix_map), "Analysis Settings", self.analysis_settings)

        ##############################################
        action_bar.addSeparator()
        ##############################################

        ''' Settings '''
        # -- Toolbar - #
        pix_map = QPixmap(os.path.join(resources, 'settings.png'))
        action_bar.addAction(QIcon(pix_map), "Settings (Ctrl+Alt+S)", self.settings)
        # Short cut
        self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.ALT + Qt.Key_S), self),
                     SIGNAL('activated()'), self.settings)

        ''' Export Write Up'''
        export_cleaned_lines = self.ui.actionCleaned_Lines
        export_cleaned_lines.triggered.connect(self.export_cleaned_lines)

        ''' Export Write Up '''
        writeup = self.ui.actionAnalysis_Summary
        writeup.triggered.connect(self.export_analysis_summary)

        ''' Export Assignment Data '''
        assignment_data = self.ui.actionAssignment_Data
        assignment_data.triggered.connect(self.export_assignment_data)

        ''' Add A Molecule '''
        add_a_molecule = self.ui.actionAdd_a_molecule
        add_a_molecule.triggered.connect(self.add_a_molecule)

        """
        Second Toolbar
        """

        tool_bar = self.ui.left_bar
        tool_bar.setAutoFillBackground(True)
        self.ui.left_bar.setStyleSheet("background-color: #353535")
        tool_bar.setMovable(False)
        ''' Toggle Info Widget '''
        btn = RotatedButton("Info", self, orientation="east")
        # btn.setStyleSheet("background-color:#282828;")
        btn.setFixedWidth(24)
        btn.setFlat(True)
        btn.setIcon(QIcon(images.INFO_ICON))
        btn.clicked.connect(self.toggle_info_widget)
        tool_bar.addWidget(btn)

        ''' Toggle Table View '''
        btn = RotatedButton("Peaks Table", self, orientation="east")
        btn.setFixedWidth(24)
        btn.setFlat(True)
        #btn.setStyleSheet("background-color:#282828;")
        btn.setIcon(QIcon(images.TABLE_ICON))
        btn.clicked.connect(self.toggle_table_widget)
        tool_bar.addWidget(btn)

        ''' Right Toolbar '''
        tool_bar = self.ui.right_bar
        tool_bar.setMovable(False)
        tool_bar.setAutoFillBackground(True)
        tool_bar.setStyleSheet("background-color: #353535")

        ''' Toggle Graph Options '''
        btn = RotatedButton("Graph Options", self)
        btn.setFixedWidth(24)
        btn.setFlat(True)
        btn.setStyleSheet("background-color:#282828;")
        btn.setIcon(QIcon(images.ROUND_GRAPH_ICON_BLUE))
        btn.clicked.connect(self.toggle_graph_options_widget)
        tool_bar.addWidget(btn)

        ''' Toggle Splatalogue Options '''
        btn = RotatedButton("Splatalogue", self)
        btn.setFixedWidth(24)
        btn.setFlat(True)
        btn.setStyleSheet("background-color:#282828;")
        btn.setIcon(QIcon(images.DATABASE_ICON_RED))
        btn.clicked.connect(self.toggle_splatalogue_options_widget)
        tool_bar.addWidget(btn)

    def __setup_graph_toolbar(self):
        """

        :return:
        """
        action_bar = self.ui.graph_action_bar

        ''' Redisplay Button'''
        # -- Toolbar - #
        pix_map = QPixmap(os.path.join(resources, 'redisplay-graph.png'))
        action_bar.addAction(QIcon(pix_map), "Redisplay Graph (F5)", self.redisplay_graph)
        # Short cut
        self.connect(QShortcut(QKeySequence(Qt.Key_F5), self),
                     SIGNAL('activated()'), self.redisplay_graph)


        ''' Show Validations '''
        # -- Toolbar -- #
        pix_map = QPixmap(os.path.join(resources, 'show-validations.png'))
        self.action_show_validations = QAction("Show Validations", self)
        self.action_show_validations.setIcon(QIcon(pix_map))
        self.action_show_validations.setIconText("Show Validations")
        self.action_show_validations.triggered.connect(self.toggle_validations_on_graph)

        action_bar.addAction(self.action_show_validations)

        ''' Plot Full Graph '''
        pix_map = QPixmap(os.path.join(resources, 'plot-spectrum.png'))
        self.action_plot_spectrum = QAction("Plot Spectrum", self)
        self.action_plot_spectrum.setIcon(QIcon(pix_map))
        self.action_plot_spectrum.setIcon(QIcon(images.PLOT_SPECTRUM))
        self.action_plot_spectrum.triggered.connect(self.plot_spectrum)

        action_bar.addAction(self.action_plot_spectrum)

        ''' Color assignments in Experiment '''
        self.action_color_assignments = QAction("Color Experiments", self)
        self.action_color_assignments.setIcon(QIcon(images.COLOR_ASSIGNMENTS))
        self.action_color_assignments.triggered.connect(self.plot_spectrum)

        action_bar.addAction(self.action_color_assignments)

        ''' More '''
        more = QAction("More", self)
        more.setIcon(QIcon(images.MORE_ELLIPSES))
        more.triggered.connect(self.plot_spectrum)

        action_bar.addAction(more)

    ###############################################################################
    # Event Methods
    ###############################################################################

    def toggle_splatalogue_options_widget(self):
        if self.splatalogue_dock_widget.isHidden():
            self.splatalogue_dock_widget.show()
        else:
            self.splatalogue_dock_widget.hide()

    def toggle_graph_options_widget(self):
        if self.graph_toolbox.isHidden():
            self.graph_toolbox.show()
        else:
            self.graph_toolbox.hide()

    def toggle_info_widget(self):
        self.info_toolbox.setHidden(not self.info_toolbox.isHidden())

    def toggle_table_widget(self):
        if self.table_toolbox.isHidden():
            self.table_toolbox.show()
        else:
            self.table_toolbox.hide()

    def closeEvent(self, QCloseEvent):
        sys.exit()

    def update_info(self):
        self.info_widget.update(self.experiment)

    ###############################################################################
    # Stub Methods
    ###############################################################################

    def settings(self):
        print "SETTINGS"

    def analysis_settings(self):
        print "ANALYSIS SETTINGS"

    def redo_analysis(self):
        self.experiment.match_threshold = 0.5
        self.experiment.ratio_threshold = 0.5
        self.experiment.get_assigned_molecules()
        self.organize_matches()
        # self.info_widget.update()

    def remove_from_analysis(self):
        print "Clicked 'remove button'"

    def plot_spectrum(self):
        print "PLOT SPECTRUM!"


class State:
    """
    Represents a single state of the ExperimentView,
    state changes based on user actions.

    Can be used with TimeMachine, to keep a history of
    ExperimentView states.
    """
    def __init__(self, experiment, pending_widget, accepted_widget, rejected_widget):
        self.experiment = deepcopy(experiment)
        self.pending_matches = pending_widget.get_matches()
        self.accepted_matches = accepted_widget.get_matches()
        self.rejected_matches = rejected_widget.get_matches()
