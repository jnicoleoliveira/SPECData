# Author: Jasmine Oliveira
# Date: 08/24/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from frames.frame___assignment_window import Ui_Dialog              # Dialog Window
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget     # Matplotlib Widget
from widget___assignment_window_info import AssignmentInfoWidget    # Assignment Info Widget

from ..experiment_analysis import Graph
from config import conn


class AssignmentWindow(QDialog):

    def __init__(self, match, color, experiment):
        super(AssignmentWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Assignment View")
        self.resize(1500, 750)

        # Widgets
        self.matplot_widget = None
        self.info_widget = None
        self.table_widget = None

        # Data
        self.match = match
        self.color = color
        self.experiment = experiment
        self.experiment_graph = None

        self.startup()

    def startup(self):
        # Setup Layout
        self.setup_layout()

        # Set Graph
        self.graph()

    def setup_layout(self):

        layout = QGridLayout()
        self.setLayout(layout)

        # Widgets
        self.matplot_widget = MatplotlibWidget()
        self.info_widget = AssignmentInfoWidget(self.match)
        self.table_widget = QTableWidget()

        # Add Data
        self.populate_table_widget()

        # Containers
        left_container = QVBoxLayout()
        left_container.addWidget(self.info_widget)
        left_container.addWidget(self.table_widget)



        # Add Widgets to Layout
        layout.addLayout(left_container, 0, 0)
        #layout.addWidget(self.info_widget, 0,0)
        #layout.addWidget(QLabel(), 0, 1)
        #layout.addWidget(self.table_widget, 1, 0)
        layout.addWidget(self.matplot_widget, 0, 1)

    def populate_table_widget(self):
        """
        Populate table_widget with the following graph data:
            Experiment PID, Frequency, Intensity with its associative
            match's PID, frequency, and intensity
        :return:
        """
        matches = self.match.matches
        import tables.get.get_peaks as peaks

        row_count = len(matches) # Number of values
        column_count = 6         # Columns
        self.table_widget = QTableWidget()

        # Format Table
        self.table_widget.setRowCount(row_count)
        self.table_widget.setColumnCount(column_count)
        self.table_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.table_widget.setSortingEnabled(True)

        # Set Header Label
        self.table_widget.setHorizontalHeaderLabels(["Experiment PID", "Frequency", "Intensity", \
                                                     "Match PID", "Frequency", "Intensity"])

        print "ROW COUNT:" + str(row_count)
        # Populate Table Widget with data
        #   Exp_pid, Exp_frequency, Exp_intensity
        #   Match_Pid, Match_frequency, Match_intensity
        for i in range(0, row_count):

            # Get Row Data
            pid = matches[i].pid
            exp_pid = matches[i].exp_pid
            match_frequency, match_intensity = peaks.get_frequency_intensity(conn, pid)
            exp_frequency, exp_intensity = peaks.get_frequency_intensity(conn, exp_pid)
            # Convert Data to QTableWidgetItem
            exp_pid_item = QTableWidgetItem(str(exp_pid))
            exp_frequency_item = QTableWidgetItem(str(exp_frequency))
            exp_intensity_item = QTableWidgetItem(str(exp_intensity))
            pid_item = QTableWidgetItem(str(pid))
            match_frequency_item = QTableWidgetItem(str(match_frequency))
            match_intensity_item = QTableWidgetItem(str(match_intensity))

            color = QColor("2E2726")
            pid_item.setBackgroundColor(color)
            match_frequency_item.setBackgroundColor(color)
            match_intensity_item.setBackgroundColor(color)

            # Add Widget Items to Table
            self.table_widget.setItem(i, 0, exp_pid_item)
            self.table_widget.setItem(i, 1, exp_frequency_item)
            self.table_widget.setItem(i, 2, exp_intensity_item)
            self.table_widget.setItem(i, 3, pid_item)
            self.table_widget.setItem(i, 4, match_frequency_item)
            self.table_widget.setItem(i, 5, match_intensity_item)

        #self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        width = self.table_widget.horizontalHeader().width()
        self.table_widget.setFixedWidth(width)

    def graph(self):
        """
        Graphs three subplots.
        (1) The original experiment
        (2) The Selected assignment (this match)
        (3) Full Original Spectrum of this assignment
        :return:
        """
        self.experiment_graph = Graph(self.matplot_widget,self.experiment)
        self.experiment_graph.add_subplot_experiment(311)
        self.experiment_graph.add_subplot_selected_assignments(312, [self.match,], [self.color,])
        self.experiment_graph.add_subplot_full_spectrum(313, self.match.mid, self.color)
        self.experiment_graph.draw()