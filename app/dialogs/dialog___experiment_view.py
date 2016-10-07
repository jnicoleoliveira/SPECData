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

        # Start Up Script
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
        from dialog___main_menu import MainMenu
        window = MainMenu()
        self.close()
        window.exec_()

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
        self.redisplay_btn = QPushButton()      # Redisplay (Redisplay graph with current selections)
        self.select_all_btn = QPushButton()     # Select all (for molecule selection)
        self.deselect_all_btn = QPushButton()   # Deselect all (for molecule selection)
        self.main_menu_btn = QPushButton()      # Main Menu (exits, returns to main menu)
        self.delete_btn = QPushButton()
        self.table = QTableWidget()

        '''
        Create Inner Layouts / Containers
        '''
        # BUTTONS LAYOUT #
        buttons_layout = QVBoxLayout()
        select_btns_layout = QHBoxLayout()
        select_btns_layout.addWidget(self.select_all_btn)
        select_btns_layout.addWidget(self.deselect_all_btn)
        select_btns_layout.addWidget(self.delete_btn)
        buttons_layout.addLayout(select_btns_layout)
        buttons_layout.addWidget(self.redisplay_btn)

        # TAB LAYOUT #

        # TOOL BOX
        tool_box = QToolBox()
        text = QString("Graph Options")
        tool_box.addItem(self.graph_options_widget, text)
        tool_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        text = QString("Peak List")
        tool_box.addItem(self.table, text)

        # DOCK WIDGET
        dock_tools = QDockWidget(self.window())
        self.window().addDockWidget(Qt.BottomDockWidgetArea, dock_tools)
        dock_tools.setWidget(tool_box)
        #dock_tools.setFloating(True)
        dock_tools.setFeatures(QDockWidget.DockWidgetClosable |
                               QDockWidget.DockWidgetMovable |
                               QDockWidget.DockWidgetFloatable |
                               QDockWidget.DockWidgetVerticalTitleBar)
        #dock_tools.setFeatures(QDockWidget.DockWidgetMovable)
        #dock_tools.setFeatures(QDockWidget.DockWidgetFloatable)
        #dock_tools.setFeatures(QDockWidget.DockWidgetVerticalTitleBar)

        #dock_tools.setAllowedAreas(QDockWidget.LeftDockWidgetArea)
        #dock_tools.setAllowedAreas(QDockWidget.RightDockWidgetArea)
        #dock_tools.setAllowedAreas(QDockWidget.TopDockWidgetArea)
        #dock_tools.setAllowedAreas(QDockWidget.BottomDockWidgetArea)

        # SCROLL SELECTION #
        scroll_selection_container = QScrollArea()
        scroll_selection_container.setWidget(self.selection_widget)
        scroll_selection_container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
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
        self.redisplay_btn.setText("Redisplay")
        self.redisplay_btn.clicked.connect(self.redisplay_graph)

        self.select_all_btn.setText("Select All")
        self.select_all_btn.clicked.connect(self.select_all)

        self.deselect_all_btn.setText("Deselect All")
        self.deselect_all_btn.clicked.connect(self.deselect_all)

        self.main_menu_btn.setText("Main Menu")
        self.main_menu_btn.clicked.connect(self.go_to_main_menu)

        delete_icon = QIcon(QPixmap(os.path.join(resources, 'trash_icon.png')))
        self.delete_btn.setIcon(delete_icon)
        self.delete_btn.clicked.connect(self.remove_from_analysis)

        '''
        Add widgets to Layout
        '''
        layout.addWidget(scroll_selection_container, 1, 0)
        layout.addLayout(buttons_layout, 2, 0)
        #layout.addWidget(self.redisplay_btn, 3, 0)
        #layout.addLayout(left_layout, 1, 1)
        layout.addWidget(self.matplot_widget, 1, 1)
        #layout.addWidget(dock_tools, 3, 2)
        #layout.addWidget(QLabel(), 4, 1)
        #layout.addWidget(tool_box, 4, 2)
        #layout.addWidget(self.main_menu_btn, 2, 2)
        outer_layout.addWidget(self.info_widget, 0, 0)
        outer_layout.addLayout(layout, 1, 0)

        #outer_layout.addWidget(dock_tools, 1, 0)

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




