# Author: Jasmine Oliveira
# Date: 08/24/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from frames.frame___assignment_window import Ui_Dialog              # Dialog Window
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget     # Matplotlib Widget
from widget___assignment_window_info import AssignmentInfoWidget    # Assignment Info Widget
from widget___assignment_graph_options import AssignmentGraphOptionsWidget # Graph Options Widget
from ..experiment_analysis import AssignmentGraph
from config import conn
from config import resources
import os

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
        self.graph_options_widget = None
        self.validate_btn = None
        self.invalidate_btn = None

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

        ''' Widgets '''
        self.matplot_widget = MatplotlibWidget()
        self.info_widget = AssignmentInfoWidget(self.match)
        self.table_widget = QTableWidget()
        self.graph_options_widget = AssignmentGraphOptionsWidget()
        self.validate_btn = QPushButton()
        self.invalidate_btn = QPushButton()
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)

        ''' Add Data '''
        self.populate_table_widget()
        self.experiment_graph = AssignmentGraph(self.matplot_widget, self.experiment)

        ''' Setup Buttons '''
        size = QSize(32, 32)
        #path = os.path.join(resources, 'validate-128.png')
        #self.validate_btn.setStyleSheet("QPushButton{ background-image: url(" + path + "); }")
        self.validate_btn.setIcon(QIcon(QPixmap(os.path.join(resources, 'validate-64x.png'))))
        self.invalidate_btn.setIcon(QIcon(QPixmap(os.path.join(resources, 'invalidate-32.png'))))
        #self.validate_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.invalidate_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.validate_btn.setIconSize(size)
        self.invalidate_btn.setIconSize(size)

        self.graph_options_widget.ui.redisplay_btn.clicked.connect(self.redisplay_graph)

        ''' Create Containers '''
        # Button Layout
        button_container = QVBoxLayout()
        button_container.addWidget(self.validate_btn)
        button_container.addWidget(self.invalidate_btn)

        # Right Container
        right_container = QVBoxLayout()
        #right_container.addWidget(self.graph_options_widget)
        #right_container.addLayout(button_container)
        #right_container.addSpacerItem(spacer_item)

        # Left Container
        left_container = QVBoxLayout()
        left_container.addWidget(self.info_widget)
        left_container.addWidget(self.graph_options_widget)
        #left_container.addLayout(button_container)
        left_container.addWidget(self.table_widget)
        #left_container.addSpacerItem(spacer_item)

        ''' Add Widgets to Layout '''
        layout.addLayout(left_container, 0, 0)
        layout.addWidget(self.matplot_widget, 0, 1)
        #layout.addLayout(right_container, 0, 2)
        #layout.addLayout(right_container, 0, 2)

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

        # --- Set Size Policy --- #
        self.table_widget.resizeRowsToContents()
        width = self.table_widget.horizontalHeader().width()
        self.table_widget.setFixedWidth(width)

        # -- Additional Options -- #
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # disallow in-table editing

    def set_graph_options(self):
        """
        Sets graph options of the Graph data object
        to the associated states of the checkboxes in the graph_options_widget
        Options:
            (1) Show Experiment's Full Spectrum
            (2) Share y axis
            (3) Color the experiment to matches
            (4) Set the matches' intensities to the matching
                experiment intensities.
        """

        # -- Get Values for Options -- #
        full_spectrum = self.graph_options_widget.full_spectrum_chk.isChecked()
        sharey = self.graph_options_widget.sharey_chk.isChecked()
        color_experiment = self.graph_options_widget.color_experiment_chk.isChecked()
        y_to_experiment_intensities = self.graph_options_widget.y_exp_intensities_chk.isChecked()

        # Set Options in graph #
        self.experiment_graph.set_options(full_spectrum=full_spectrum, sharey=sharey,
                                          y_to_experiment_intensities=y_to_experiment_intensities,
                                          color_experiment=color_experiment)

    def graph(self):
        """
        Graphs three subplots.
        (1) The original experiment
        (2) The Selected assignment (this match)
        (3) Full Original Spectrum of this assignment
        :return:
        """

        self.experiment_graph.graph(self.match, self.color)
        self.experiment_graph.draw()

    def redisplay_graph(self):
        self.set_graph_options()
        self.experiment_graph.clear()
        self.graph()
