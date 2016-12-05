# Author: Jasmine Oliveira
# Date: 08/24/2016

import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget
from .frames.frame___experiment_view import Ui_MainWindow

from analysis import experiment
from .splash_screens import LoadingProgressScreen
from .widget___main_graph_options import MainGraphOptionsWidget
from .widget___molecule_selection import MoleculeSelectionWidget
from .widget___experiment_info import ExperimentInfoWidget
from ..experiment_analysis import MainGraph

from config import resources
from ..events import display_error_message
import os


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
        self.setWindowTitle("Experiment View")
        self.resize(1800, 900)

        ''' Widgets '''
        # -- Graph  -- #
        self.matplot_widget = None
        # -- Graph Options -- #
        self.graph_options_widget = None
        # -- Experiment Info Widget -- #
        self.info_widget = None
        # -- Molecule Selection Widget -- #
        self.selection_widget = None
        # -- Validated Selection Widget --#
        self.validated_selection_widget = None
        # -- Invalidated Selection Widget --#
        self.invalidated_selection_widget = None
        # -- Table Widget -- #
        self.table_widget = None
        # -- Buttons -- #
        self.redisplay_btn = None       # Redisplay (Redisplay graph with current selections)
        self.select_all_btn = None      # Select all (for molecule selection)
        self.deselect_all_btn = None    # Deselect all (for molecule selection)
        self.main_menu_btn = None       # Main Menu (exits, returns to main menu)
        self.delete_btn = None          # Delete Button, removes associated lines from analysis

        ''' Menu Bar '''
        self.action_show_validations = None
        self.show_validations_on_graph = True

        ''' Data '''
        self.experiment = None          # Experiment Object
        self.experiment_graph = None    # ExperimentGraph Object
        self.loading_screen = None      # LoadingProgressScreen Object

        '''Start Up'''
        self.startup(experiment_name, mid)
        self.show()
        self.cid_pick = self.matplot_widget.getFigure().canvas.mpl_connect('pick_event', self.on_pick)

    def add_selection_assignments(self):
        self.selection_widget.add_all(self.experiment.get_sorted_molecule_matches())

    def deselect_all(self):
        """
        Select all button function.
        Checks all selections in selection widget
        """
        self.selection_widget.deselect_all()

    def do_analysis(self):
        self.experiment.get_assigned_molecules()

    def get_options(self):

        # -- Get Values for Options -- #
        full_spectrum = self.graph_options_widget.full_spectrum_chk.isChecked()
        sharey = self.graph_options_widget.sharey_chk.isChecked()
        color_experiment = self.graph_options_widget.color_experiment_chk.isChecked()
        y_to_experiment_intensities = self.graph_options_widget.y_exp_intensities_chk.isChecked()
        show_validations = self.show_validations_on_graph

        # Set Options in graph #
        self.experiment_graph.set_options(full_spectrum=full_spectrum, sharey=sharey,
                                          y_to_experiment_intensities=y_to_experiment_intensities,
                                          color_experiment=color_experiment, show_validations=show_validations)

    def go_to_main_menu(self):
        #from dialog___main_menu import MainMenu
        #window = MainMenu()
        #self.close()
        self.hide()
        #window.exec_()
        #self.close()

    def graph(self):
        # Get Info for Experiment graph
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

    def invalidate_selections(self):
        # Remove selected rows, and get those selections #
        matches, colors = self.selection_widget.remove_selections()

        for i in range(0, len(matches)):
            self.invalidated_selection_widget.add_row(matches[i], colors[i])

    def redisplay_graph(self):
        """
        Redisplay button function.
        Clears current experiment graph, and redisplays graph from checkbox selections.
        """

        xlim, ylim = self.experiment_graph.get_zoom_coordinates()
        print str(xlim) + " " + str(ylim)

        # Clear Graph
        self.experiment_graph.clear()

        # Get options
        self.get_options()

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
        self.cid_pick = self.matplot_widget.getFigure().canvas.mpl_connect('pick_event', self.on_pick)

    def select_all(self):
        """
        Select all button function.
        Checks all selections in selection widget
        """
        self.selection_widget.select_all()

    def highlight_table_row(self, frequency):
        """
        Highlights corresponding rows with the parameter pid
        :param pid:
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
        Populate table_widget with the following graph data:
            Experiment PID, Frequency, Intensity with its associative
            match's PID, frequency, and intensity
        """
        import tables.peaks_table as peaks_table
        from config import conn
        matches = self.experiment.get_all_matches_list()

        row_count = len(matches) # Number of values
        column_count = 5         # Columns

        # Format Table
        self.table_widget.setRowCount(row_count)
        self.table_widget.setColumnCount(column_count)
        self.table_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.table_widget.setSortingEnabled(True)

        # Set Header Label
        self.table_widget.setHorizontalHeaderLabels(["Exp PID", "Frequency", "Intensity", \
                                                     "Match", "Status"])

        for i in range(0, row_count):

            # Get Row Data
            exp_pid = matches[i].exp_pid
            exp_frequency, exp_intensity = peaks_table.get_frequency_intensity(conn, exp_pid)
            name = matches[i].name
            mid = matches[i].mid
            status = "pending"

            # Determine if status is valid
            if self.experiment.is_validated_molecule(mid):
                status = "valid"

            # Convert Data to QTableWidgetItem
            exp_pid_item = QTableWidgetItem(str(exp_pid))
            exp_frequency_item = QTableWidgetItem(str(exp_frequency))
            exp_intensity_item = QTableWidgetItem(str(exp_intensity))
            name_item = QTableWidgetItem(name)
            status_item = QTableWidgetItem(status)

            color = QColor("black")
            # Get status color
            if status is "invalid":
                color = QColor(self.COLOR_INVALID)
            elif status is "valid":
                color = QColor(self.COLOR_VALID)

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

        # width = self.table_widget.horizontalHeader().width()
        # self.table_widget.setFixedWidth(width)

    def show_validations(self):
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

        print "Show Validations: " + str(self.show_validations_on_graph)

    def setup_layout(self):
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

        '''
        Create Inner Layouts / Containers
        '''

        # ------------------------------------------------------------------ #
        # Create Docked Tool Box Widget
        # ------------------------------------------------------------------ #
        # --- 1st Tab: Graph options
        # --- 2nd Tab : Peak List

        # Create Tool Box
        tool_box = QToolBox()
        text = QString("Graph Options")
        tool_box.addItem(self.graph_options_widget, text)
        tool_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        text = QString("Peak List")
        tool_box.addItem(self.table_widget, text)

        # Dock the tool box
        dock_tools = QDockWidget(self.window())
        self.window().addDockWidget(Qt.RightDockWidgetArea, dock_tools)
        dock_tools.setWidget(tool_box)
        dock_tools.setFeatures(QDockWidget.DockWidgetClosable |
                               QDockWidget.DockWidgetMovable |
                               QDockWidget.DockWidgetFloatable |
                               QDockWidget.DockWidgetVerticalTitleBar)

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

        '''
        Add widgets to Layout
        '''

        hlayout = QHBoxLayout()
        v1 = QVBoxLayout()
        v1.addWidget(self.info_widget)
        v1.addWidget(selection_tab_widget)
        v2 = QVBoxLayout()
        v2.addWidget(self.matplot_widget)
        hlayout.addLayout(v1)
        hlayout.addLayout(v2)
        outer_layout.addLayout(hlayout, 0, 0)

        '''
        Toolbar and ShortCuts
        '''
        self.setup_toolbar_and_shortcuts()

        ''' Button Connections '''
        self.graph_options_widget.deselect_all_btn.clicked.connect(self.deselect_all)
        self.graph_options_widget.redisplay_btn.clicked.connect(self.redisplay_graph)
        self.graph_options_widget.select_all_btn.clicked.connect(self.select_all)
        self.graph_options_widget.show_validations_btn.clicked.connect(self.show_validations)

    def setup_toolbar_and_shortcuts(self):

        action_bar = self.ui.action_bar

        ''' Home Button '''
        pix_map = QPixmap(os.path.join(resources, 'home.png'))
        action_bar.addAction(QIcon(pix_map), "Main Menu", self.go_to_main_menu)

        ''' Save Button'''
        # -- Toolbar - #
        pix_map = QPixmap(os.path.join(resources, 'save-button.png'))
        action_bar.addAction(QIcon(pix_map), "Save Analysis (Ctrl+S)", self.save_analysis)
        # Short cut
        self.connect(QShortcut(QKeySequence(Qt.CTRL, Qt.Key_S), self),
                     SIGNAL('activated()'), self.save_analysis)

        action_bar.addSeparator()
        ##############################################
        ''' Undo '''
        # -- Toolbar - #
        pix_map = QPixmap(os.path.join(resources, 'undo-disabled.png'))
        action_bar.addAction(QIcon(pix_map), "Undo (Ctrl+Alt+Z)", self.undo)

        ''' Redo '''
        # -- Toolbar - #
        pix_map = QPixmap(os.path.join(resources, 'redo.png'))
        action_bar.addAction(QIcon(pix_map), "Redo (Ctrl+Alt+Y)", self.redo)

        action_bar.addSeparator()
        ##############################################
        ''' Redisplay Button'''
        # -- Toolbar - #
        pix_map = QPixmap(os.path.join(resources, 'redisplay-graph.png'))
        action_bar.addAction(QIcon(pix_map), "Redisplay Graph (F5)", self.redisplay_graph)
        # Short cut
        self.connect(QShortcut(QKeySequence(Qt.Key_F5), self),
                     SIGNAL('activated()'), self.redisplay_graph)

        ''' Select All '''
        # -- Toolbar - #
        pix_map = QPixmap(os.path.join(resources, 'select-all.png'))
        action_bar.addAction(QIcon(pix_map), "Select All (Ctrl+A)", self.select_all)
        # Short cut
        self.connect(QShortcut(QKeySequence(Qt.CTRL, Qt.Key_A), self),
                     SIGNAL('activated()'), self.select_all)

        ''' Deselect All '''
        # -- Toolbar - #
        pix_map = QPixmap(os.path.join(resources, 'deselect-all.png'))
        action_bar.addAction(QIcon(pix_map), "Deselect All (Ctrl+D)", self.deselect_all)
        # Short cut
        self.connect(QShortcut(QKeySequence(Qt.CTRL, Qt.Key_D), self),
                     SIGNAL('activated()'), self.deselect_all)

        ''' Show Validations '''
        # -- Toolbar -- #
        pix_map = QPixmap(os.path.join(resources, 'show-validations.png'))
        self.action_show_validations = QAction("Show Validations", self)
        self.action_show_validations.setIcon(QIcon(pix_map))
        self.action_show_validations.setIconText("Show Validations")
        self.action_show_validations.triggered.connect(self.show_validations)
        action_bar.addAction(self.action_show_validations)
        #action_bar.triggered[QAction].connect(self.show_validations)
        #action_bar.addAction(QIcon(pix_map), "Show Validations", self.show_validations)

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
        self.connect(QShortcut(QKeySequence(Qt.CTRL, Qt.ALT, Qt.Key_S), self),
                     SIGNAL('activated()'), self.settings)

        ''' Export Write Up'''
        export_cleaned_lines = self.ui.actionExport_cleaned_lines
        export_cleaned_lines.triggered.connect(self.export_cleaned_lines)

    def startup(self, experiment_name, mid):
        """
        Start-up script, does the following behind a loading progress screen:
        (1) Creates experiment from mid and experiment_name
        (2) Does Experiment analysis
        (3) Sets up layout with respective analysis data
        (4) Draws graph
        :param experiment_name: Experiment name
        :param mid: Experiment molecule ID
        """

        '''Start Loading Screen'''
        self.loading_screen = LoadingProgressScreen()
        self.loading_screen.start()     # Start Loading Screen

        ## Do Things ##

        ''' Create Experiment '''
        self.loading_screen.set_caption('Creating experiment...')
        self.experiment = experiment.Experiment(experiment_name, mid)  # Create experiment obj
        time.sleep(1)
        self.loading_screen.next_value(20)

        '''Analyze Experiment'''
        self.loading_screen.set_caption('Analyzing...')
        self.do_analysis()                      # Run Analysis
        self.loading_screen.next_value(40)
        time.sleep(1)

        '''Setup Layout'''
        self.loading_screen.set_caption('Setting up...')
        self.setup_layout()                     # Setup Layout
        self.loading_screen.next_value(60)

        '''Add Assignments to Selection Widget'''
        self.add_selection_assignments()        # Add assignments
        time.sleep(1)
        self.loading_screen.next_value(80)

        '''Graph Main Graph'''
        self.graph()                            # Graph
        self.loading_screen.next_value(90)
        time.sleep(2)

        '''End Loading Screen'''
        self.loading_screen.end()

    def validate_selections(self):
        print "VALIDATE SELECTIONS"

        # -- Get Selected Mids -- #
        selected_mids = self.selection_widget.get_selected_mids()

        # -- Validate Selections in Experiment -- #
        for mid in selected_mids:
            self.experiment.validate_a_match(mid)

        # Remove selected rows, and get those selections #
        matches, colors = self.selection_widget.remove_selections()

        for i in range(0, len(matches)):
            self.validated_selection_widget.add_row(matches[i], colors[i])

        # Repopulate table widget to show updated validations
        self.populate_table_widget()

    def on_pick(self, event):
        """
        When picking a line on the graph, highlights associated
        row in the table-widget.
        :param event:
        """
        # print str(event.xdata)
        rect = event.artist
        x,y = rect.xy
        self.highlight_table_row(x)

        #print (rect.xy)
        print "picked x" + str(x)

    # ----- STUB METHODS ---- #

    def settings(self):
        print "SETTINGS"

    def analysis_settings(self):
        print "ANALYSIS SETTINGS"

    def redo_analysis(self):
        self.highlight_table_row(30761)
        print "RE-ANALYZE"

    def undo(self):
        print "UNDO"

    def redo(self):
        print "REDO"

    def remove_from_analysis(self):
        print "Clicked 'remove button'"

    def save_analysis(self):
        print "SAVE BUTTON CLICKED"

    def export_cleaned_lines(self):
        from dialog___export_cleaned_lines import ExportCleanedLines
        window = ExportCleanedLines(self.experiment)
        window.exec_()






