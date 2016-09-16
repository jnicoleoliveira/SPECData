# Author: Jasmine Oliveira
# Date: 08/24/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import matplotlib.backends.backend_qt4agg

#import matplotlib
#matplotlib.use("Agg")
from .frames.frame___experiment import Ui_Dialog
from .widget___molecule_selection import MoleculeSelectionWidget
from .widget___main_graph_options import MainGraphOptionsWidget
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget
from .splash_screens import LoadingProgressScreen

from ..experiment_analysis import MainGraph
from functions import experiment
import pyqtgraph as pg

import time
import os


class ExperimentView(QDialog):

    def __init__(self, experiment_name, mid):
        super(ExperimentView, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Experiment View")

        # Widgets
        self.plot_widget = None
        self.graph_options_widget = None
        self.matplot_widget = MatplotlibWidget()
        self.selection_widget = None
        self.redisplay_btn = QPushButton()
        self.select_all_btn = QPushButton()
        self.deselect_all_btn = QPushButton()

        # Data
        self.experiment = None          # Experiment Object
        self.experiment_graph = None    # ExperimentGraph Object
        self.loading_screen = None      # LoadingProgressScreen Object

        self.startup(experiment_name, mid)

    def add_selection_assignments(self):
        self.selection_widget.add_all(self.experiment.molecule_matches.values())

    def connect_buttons(self):
        redisplay_btn = self.ui.redisplay_btn
        redisplay_btn.clicked.connect(self.redisplay_graph)

    def deselect_all(self):
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
        :return:
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

    def select_all(self):
        self.selection_widget.select_all()

    def setup_layout(self):

        # Set a grid layout to manage widgets
        layout = QGridLayout()
        self.setLayout(layout)

        # Widgets
        self.matplot_widget = MatplotlibWidget()
        self.graph_options_widget = MainGraphOptionsWidget()
        self.selection_widget = MoleculeSelectionWidget(self.experiment)
        self.redisplay_btn = QPushButton()
        self.select_all_btn = QPushButton()
        self.deselect_all_btn = QPushButton()

        # Containers  / Inner Layouts
        select_btns_layout = QHBoxLayout()
        select_btns_layout.addWidget(self.select_all_btn)
        select_btns_layout.addWidget(self.deselect_all_btn)

        scroll_selection_container = QScrollArea()
        scroll_selection_container.setWidget(self.selection_widget)
        scroll_selection_container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        left_layout = QVBoxLayout()
        left_layout.addWidget(scroll_selection_container)
        left_layout.addWidget(self.graph_options_widget)
        left_layout.addLayout(select_btns_layout)
        left_layout.addWidget(self.redisplay_btn)

        # Set Data
        self.redisplay_btn.setText("Redisplay")
        self.redisplay_btn.clicked.connect(self.redisplay_graph)

        self.select_all_btn.setText("Select All")
        self.select_all_btn.clicked.connect(self.select_all)

        self.deselect_all_btn.setText("Deselect All")
        self.deselect_all_btn.clicked.connect(self.deselect_all)

        #self.plot_widget = pg.PlotWidget(title="Experiment Peaks")
        #spacer1_widget = QSpacerItem()

        ## Add Widgets to layout
        #layout.addWidget(scroll_selection_container, 0, 0)
        layout.addLayout(left_layout, 0 , 0)
        layout.addWidget(self.matplot_widget, 0, 1)
        #layout.addWidget(self.graph_options_widget, 3, 0)
        #layout.addLayout(select_btns_layout, 1, 0)

        #layout.addWidget(self.redisplay_btn, 2,0)
        #layout.addWidget(QLabel(), 1, 2)
        #layout.addWidget(self.plot_widget, 0,1)

    def startup(self, experiment_name, mid):
        self.loading_screen = LoadingProgressScreen()
        self.loading_screen.start()     # Start Loading Screen

        ## Do Things ##

        # Create Experiment
        self.loading_screen.set_caption('Creating experiment...')
        self.experiment = experiment.Experiment(experiment_name, mid)  # Create experiment obj
        time.sleep(1)
        self.loading_screen.next_value(20)

        # Analyze Experiment
        self.loading_screen.set_caption('Analyzing...')
        self.do_analysis()                      # Run Analysis
        self.loading_screen.next_value(40)
        time.sleep(1)

        # Setup Layout
        self.loading_screen.set_caption('Setting up...')
        self.setup_layout()                     # Setup Layout
        self.loading_screen.next_value(60)

        # Add Assignments to Selection Widget
        self.add_selection_assignments()        # Add assignments
        time.sleep(1)
        self.loading_screen.next_value(80)

        # Graph Main Graph
        self.graph()                            # Graph
        self.loading_screen.next_value(90)
        time.sleep(2)

        # End Loading Screen
        self.loading_screen.end()




