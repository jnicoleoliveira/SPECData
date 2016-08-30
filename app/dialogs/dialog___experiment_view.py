# Author: Jasmine Oliveira
# Date: 08/24/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUi
import pyqtgraph as pg

from frames.frame___experiment import Ui_Dialog
from widget___molecule_selection import MoleculeSelectionWidget
from splash_screens import LoadingProgressScreen
from ..experiment_analysis import ExperimentGraph
from functions import experiment
from config import resources

import time
import numpy as np
import os

#Ui_Experiment = \
#    loadUi(os.path.join(os.path.dirname(__file__), 'frames', 'experiment.ui'))


class ExperimentView(QDialog):

    def __init__(self, experiment_name, mid):
        super(ExperimentView, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Experiment View")
        self.plot_widget = None
        self.selection_widget = None

        self.experiment = None
        self.loading_screen = None

        self.startup(experiment_name, mid)

    def startup(self, experiment_name, mid):
        self.loading_screen = LoadingProgressScreen()
        self.loading_screen.start()     # Start Loading Screen

        ## Do Things ##

        # Create Experiment
        self.loading_screen.set_caption('Creating experiment...')
        self.experiment = self.create_experiment(experiment_name, mid)  # Create experiment obj
        time.sleep(1)
        self.loading_screen.next_value(20)      # Progress ++

        # Analyze Experiment
        self.loading_screen.set_caption('Analyzing...')
        self.do_analysis()                      # Run Analysis
        self.loading_screen.next_value(40)      # Progress ++
        time.sleep(3)

        # Setup Layout
        self.loading_screen.set_caption('Setting up...')
        self.setup_layout()                     # Setup Layout
        self.loading_screen.next_value(60)      # Progress ++
        self.add_selection_assignments()        # Add assignments
        time.sleep(2)
        self.loading_screen.next_value(80)      # Progress ++
        self.graph()
        time.sleep(2)

        self.loading_screen.end()

    def create_experiment(self, experiment_name, mid):
        return experiment.Experiment(experiment_name, mid)

    def start_splash_screen(self):
        from config import resources
        pix_map = QPixmap(os.path.join(resources, 'specdata_logo.png'))
        self.splash_screen = QSplashScreen(pix_map)

        progressBar = QProgressBar(self.splash_screen)
        progressBar.setGeometry(self.splash_screen.width()/10, 7*self.splash_screen.height()/10, 8*self.splash_screen.width()/10, self.splash_screen.height()/10)
        self.splash_screen.show()

        #for i in range (0,100):
        #    progressBar.setValue(i)

            #Analysize
        #self.splash_screen.setPixmap(pix_map, Qt.WindowStaysOnTopHint)
        #self.splash_screen.show()

    def stop_splash_screen(self):
        self.splash_screen.close()

    def do_analysis(self):
        self.experiment.get_assigned_molecules()

    def setup_layout(self):

        # Set a grid layout to manage widgets
        layout = QGridLayout()
        self.setLayout(layout)

        # Widgets
        self.plot_widget = pg.PlotWidget()
        self.selection_widget = MoleculeSelectionWidget()
        #spacer1_widget = QSpacerItem()

        ## Add Widgets to layout
        layout.addWidget(self.selection_widget, 0,0)
        #layout.addWidget(spacer1_widget, 0, 1)
        layout.addWidget(self.plot_widget, 0,2)

    def add_selection_assignments(self):
        # Set
        self.selection_widget.add_all(self.experiment.get_assigned_names(), self.experiment.get_assigned_mids())

    def graph(self):
        experiment_graph = ExperimentGraph(self.experiment, self.selection_widget, [self.plot_widget,0])
        experiment_graph.graph_assignments(0)

    def connect_buttons(self):
        redisplay_btn = self.ui.redisplay_btn

        redisplay_btn.clicked.connect(self.redisplay_graph)

    def redisplay_graph(self):
        return True # do nothing

    #def graph_in_widget(self):
        #graphics_view = self.ui.main_graph
        #self.experiment_graph = ExperimentGraph(self.ui.kplotwidget)
        #self.molecule_grid = self.ui.molecule_grid
        #graphics_view = pg.GraphicsWindow(title='TestingPlot')