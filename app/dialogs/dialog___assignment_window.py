# Author: Jasmine Oliveira
# Date: 08/24/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from frames.frame___assignment_window import Ui_Dialog
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget
from ..experiment_analysis import Graph

class AssignmentWindow(QDialog):

    def __init__(self, match, color, experiment):
        super(AssignmentWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Experiment View")
        self.resize(1000, 1000)
        self.matplot_widget = MatplotlibWidget()
        self.selection_widget = None
        self.list_widget = None
        self.title_label= None
        self.match = match
        self.color = color
        self.experiment = experiment
        self.experiment_graph = None

        self.startup()

    def startup(self):
        # Setup Layou
        self.setup_layout()

        # Set Graph
        self.graph()

    def setup_layout(self):

        layout = QGridLayout()
        self.setLayout(layout)

        # Widgets
        self.matplot_widget = MatplotlibWidget()

        layout.addWidget(self.matplot_widget, 0, 1)

    def graph(self):
        self.experiment_graph = Graph(self.matplot_widget,self.experiment)
        self.experiment_graph.add_subplot_experiment(311)
        self.experiment_graph.add_subplot_selected_assignments(312, [self.match,], [self.color,])
        self.experiment_graph.add_subplot_full_spectrum(313, self.match.mid, self.color)
        self.experiment_graph.draw()