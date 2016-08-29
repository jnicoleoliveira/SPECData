# Author: Jasmine Oliveira
# Date: 08/24/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUi
from frames.frame___experiment import Ui_Dialog

#from frames.frame___experiment_view import Ui_ExperimentDialog  # Import frame
#from ..experiment_analysis import ExperimentGraph
from widget___molecule_selection import MoleculeSelectionWidget

import pyqtgraph as pg
import numpy as np
import os
from functions import experiment
#Ui_Experiment = \
#    loadUi(os.path.join(os.path.dirname(__file__), 'frames', 'experiment.ui'))


class ExperimentView(QDialog):

    def __init__(self, experiment_name, mid):
        super(ExperimentView, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Experiment View")

        self.experiment = experiment.Experiment(experiment_name, mid)

        # Functions
        self.do_analysis()
        self.setup_layout()

        self.show()

    def do_analysis(self):
        self.experiment.get_assigned_molecules()

    def setup_layout(self):

        # Set a grid layout to manage widgets
        layout = QGridLayout()
        self.setLayout(layout)

        # Widgets
        plot_widget = pg.PlotWidget()
        selection_widget = MoleculeSelectionWidget()
        #spacer1_widget = QSpacerItem()

        # Set
        selection_widget.add_all(self.experiment.get_assigned_names(), self.experiment.get_assigned_mids())
        print "added!"
        ## Add Widgets to layout
        layout.addWidget(selection_widget, 0,0)
        #layout.addWidget(spacer1_widget, 0, 1)
        layout.addWidget(plot_widget, 0,2)

        
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