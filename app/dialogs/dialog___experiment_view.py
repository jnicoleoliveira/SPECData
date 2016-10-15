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
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Experiment View")

        ''' Widgets '''
        # -- Graph  -- #
        self.matplot_widget = None
        # -- Graph Options -- #
        self.graph_options_widget = None
        # -- Experiment Info Widget -- #
        self.info_widget = None
        # -- Molecule Selection Widget -- #
        self.selection_widget = None
        # -- Table Widget -- #
        self.table_widget = None
        # -- Buttons -- #
        self.redisplay_btn = None       # Redisplay (Redisplay graph with current selections)
        self.select_all_btn = None      # Select all (for molecule selection)
        self.deselect_all_btn = None    # Deselect all (for molecule selection)
        self.main_menu_btn = None       # Main Menu (exits, returns to main menu)
        self.delete_btn = None          # Delete Button, removes associated lines from analysis

        ''' Data '''
        self.experiment = None          # Experiment Object
        self.experiment_graph = None    # ExperimentGraph Object
        self.loading_screen = None      # LoadingProgressScreen Object

        '''Start Up'''
        self.startup(experiment_name, mid)
        self.show()

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

    def get_options(self):
        full_spectrum = self.graph_options_widget.full_spectrum_chk.isChecked()
        sharey = self.graph_options_widget.sharey_chk.isChecked()
        color_experiment = self.graph_options_widget.color_experiment_chk.isChecked()
        y_to_experiment_intensities = self.graph_options_widget.y_exp_intensities_chk.isChecked()

        self.experiment_graph.set_options(full_spectrum=full_spectrum, sharey=sharey,
                                          y_to_experiment_intensities=y_to_experiment_intensities,
                                          color_experiment=color_experiment)

    def redisplay_graph(self):
        """
        Redisplay button function.
        Clears current experiment graph, and redisplays graph from checkbox selections.
        """
        # Clear Graph
        self.experiment_graph.clear()

        # Get options
        self.get_options()

        # Determine graphing selections
        matches, colors = self.selection_widget.get_selections()

        # Graph
        self.experiment_graph.graph(matches, colors)

        # Draw
        self.experiment_graph.draw()

    def remove_from_analysis(self):
        print "Clicked 'remove button'"

    def select_all(self):
        """
        Select all button function.
        Checks all selections in selection widget
        """
        self.selection_widget.select_all()

    def go_to_main_menu(self):
        #from dialog___main_menu import MainMenu
        #window = MainMenu()
        #self.close()
        self.hide()
        #window.exec_()
        #self.close()

    def populate_table_widget(self):
        """
        Populate table_widget with the following graph data:
            Experiment PID, Frequency, Intensity with its associative
            match's PID, frequency, and intensity
        :return:
        """
        import tables.get.get_peaks as peaks
        from config import conn
        matches = self.experiment.get_all_matches_list()

        row_count = len(matches) # Number of values
        column_count = 5         # Columns
        self.table_widget = QTableWidget()

        # Format Table
        self.table_widget.setRowCount(row_count)
        self.table_widget.setColumnCount(column_count)
        self.table_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.table_widget.setSortingEnabled(True)

        # Set Header Label
        self.table_widget.setHorizontalHeaderLabels(["Experiment PID", "Frequency", "Intensity", \
                                                     "Molecule Matched", "Status"])

        for i in range(0, row_count):

            # Get Row Data
            exp_pid = matches[i].exp_pid
            exp_frequency, exp_intensity = peaks.get_frequency_intensity(conn, exp_pid)
            name = matches[i].name
            status = "invalid"

            # Convert Data to QTableWidgetItem
            exp_pid_item = QTableWidgetItem(str(exp_pid))
            exp_frequency_item = QTableWidgetItem(str(exp_frequency))
            exp_intensity_item = QTableWidgetItem(str(exp_intensity))
            name_item = QTableWidgetItem(name)
            status_item = QTableWidgetItem(status)

            color = QColor("2E2726")
            # Get status color
            if status is "pending":
                color = QColor(self.COLOR_PENDING)
            elif status is "invalid":
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

        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        #width = self.table_widget.horizontalHeader().width()
        #self.table_widget.setFixedWidth(width)

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
        # BUTTONS LAYOUT #
        #buttons_layout = QVBoxLayout()
        #select_btns_layout = QHBoxLayout()
        #select_btns_layout.addWidget(self.select_all_btn)
        #select_btns_layout.addWidget(self.deselect_all_btn)
        #select_btns_layout.addWidget(self.delete_btn)
        #buttons_layout.addLayout(select_btns_layout)
        #buttons_layout.addWidget(self.redisplay_btn)


        # TOOL BOX WIDGET
        tool_box = QToolBox()
        text = QString("Graph Options")
        tool_box.addItem(self.graph_options_widget, text)
        tool_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        text = QString("Peak List")
        tool_box.addItem(self.table_widget, text)



        # DOCK TOOLS
        dock_tools = QDockWidget(self.window())
        self.window().addDockWidget(Qt.BottomDockWidgetArea, dock_tools)
        dock_tools.setWidget(tool_box)
        #dock_tools.setFloating(True)
        dock_tools.setFeatures(QDockWidget.DockWidgetClosable |
                               QDockWidget.DockWidgetMovable |
                               QDockWidget.DockWidgetFloatable |
                               QDockWidget.DockWidgetVerticalTitleBar)

        # SCROLL SELECTION #
        scroll_selection_container = QScrollArea()
        scroll_selection_container.setWidget(self.selection_widget)
        scroll_selection_container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_selection_container.setFrameShadow(QFrame.Raised)

        # LEFT LAYOUT #
        left_layout = QVBoxLayout()
        #left_layout.addWidget(scroll_selection_container)
        left_layout.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding))
        #left_layout.addWidget(self.graph_options_widget)
        #left_layout.addLayout(select_btns_layout)
        #left_layout.addWidget(self.redisplay_btn)

        '''
        Connect Buttons
        '''

        # -- CONNECT BUTTONS -- #
        #self.redisplay_btn.setText("Redisplay (F5)")
        #self.redisplay_btn.clicked.connect(self.redisplay_graph)

        #self.select_all_btn.setText("Select All")
        #self.select_all_btn.clicked.connect(self.select_all)

        #self.deselect_all_btn.setText("Deselect All")
        #self.deselect_all_btn.clicked.connect(self.deselect_all)

        #self.main_menu_btn.setText("Main Menu")
        #self.main_menu_btn.clicked.connect(self.go_to_main_menu)

        #delete_icon = QIcon(QPixmap(os.path.join(resources, 'trash_icon.png')))
        #self.delete_btn.setIcon(delete_icon)
        #self.delete_btn.clicked.connect(self.remove_from_analysis)

        '''
        Add widgets to Layout
        '''

        hlayout = QHBoxLayout()
        v1 = QVBoxLayout()
        v1.addWidget(self.info_widget)
        v1.addWidget(scroll_selection_container)
        v2 = QVBoxLayout()
        v2.addWidget(self.matplot_widget)
        hlayout.addLayout(v1)
        hlayout.addLayout(v2)
        outer_layout.addLayout(hlayout, 0, 0)

        '''
        Toolbar and ShortCuts
        '''
        self.setup_toolbar_and_shortcuts()

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

    def settings(self):
        print "SETTINGS"

    def analysis_settings(self):
        print "ANALYSIS SETTINGS"

    def redo_analysis(self):
        print "RE-ANALYZE"

    def undo(self):
        print "UNDO"

    def redo(self):
        print "REDO"

    def invalidate_selections(self):
        print "INVALIDATE SELECTIONS CLICKED"

    def validate_selections(self):
        print "VALIDATE SELECTIONS CLICKED"
        self.selection_widget.validate_selections()

    def save_analysis(self):
        print "SAVE BUTTON CLICKED"





