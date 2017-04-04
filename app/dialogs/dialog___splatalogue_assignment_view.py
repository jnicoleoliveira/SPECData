# Author: Jasmine Oliveira
# Date: 02/17/2017

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget  # Matplotlib Widget

import images
from config import conn
from tables.peaks_table import get_frequency


class SplatalogueAssignmentWindow(QDialog):
    FACE_COLOR = "#626262"
    EXPERIMENT_EDGE_COLOR = 'black'

    def __init__(self, experiment, chemical, selection_widget):
        super(SplatalogueAssignmentWindow, self).__init__()

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Splatalogue Assignment Window")
        self.resize(1500, 750)

        ''' Data '''
        self.experiment = experiment
        self.chemical = chemical

        ''' Widgets '''
        self.info_widget = SplatalogueInfoWidget(chemical)
        self.table_widget = QTableWidget()
        self.matplot_widget = MatplotlibWidget()
        self.selection_widget = selection_widget

        '''Colors'''
        self.color___experiment_edge = SplatalogueAssignmentWindow.EXPERIMENT_EDGE_COLOR
        self.color___face_color = SplatalogueAssignmentWindow.FACE_COLOR

        self.__setup__()

    def validate(self):
        # Validate all lines for now
        for line in self.chemical.lines:
            line.validated = True
        match = self.chemical.validate_chemical(self.experiment)
        self.selection_widget.add_row(match)

        self.close()
        self.setResult(1)

    def __setup__(self):
        self.setStyleSheet(
            "background-color: rgb(48, 48, 48);\ngridline-color: rgb(195, 195, 195);\ncolor: rgb(255, 255, 255);\n")
        self.matplot_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__setup_layout()
        self.__populate_graph()
        self.__populate_table()

    def __setup_layout(self):
        outer_layout = QVBoxLayout()

        ''' Inner Grid Layout '''
        layout = QGridLayout()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.info_widget)
        left_layout.addWidget(self.table_widget)
        layout.addLayout(left_layout, 0, 0)
        layout.addWidget(self.matplot_widget, 0, 1)

        ''' Bottom Frame '''
        bottom_frame = QFrame()
        frame_layout = QHBoxLayout()
        # --- Widgets --- #
        validate_btn = QPushButton(QIcon(images.VALIDATE_ICON), "Validate")
        cancel_btn = QPushButton("Cancel")
        # -- Settings -- #
        bottom_frame.setFrameShadow(QFrame.Raised)
        bottom_frame.setFrameShape(QFrame.StyledPanel)
        # -- Add Widgets -- #
        frame_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        frame_layout.addWidget(validate_btn)
        frame_layout.addWidget(cancel_btn)
        bottom_frame.setLayout(frame_layout)
        # -- Button Connections -- #
        validate_btn.clicked.connect(self.validate)
        cancel_btn.clicked.connect(self.close)

        ''' Add '''
        outer_layout.addLayout(layout)
        outer_layout.addWidget(bottom_frame)

        self.setLayout(outer_layout)

    def __populate_graph(self):
        """

        :return:
        """

        figure = self.matplot_widget.getFigure()
        figure.set_facecolor(self.color___face_color)

        ''' Experiment Subplot '''
        frequencies, intensities = self.experiment.get_experiment_frequencies_intensities_list()
        max_freq = max(frequencies)
        min_freq = min(frequencies)

        self.subplot_1 = figure.add_subplot(311,
                                            axisbg='white',
                                            title='Experiment: ' + self.experiment.name + ' Peaks')

        self.subplot_1.bar(frequencies, intensities, width=0.02, edgecolor=self.color___experiment_edge)

        ''' Matches Subplot '''
        self.subplot_2 = figure.add_subplot(312,
                                            axisbg='white',
                                            sharex=self.subplot_1)

        for l in self.chemical.lines:
            # if l.intensity <= 0:
            self.subplot_2.bar(l.frequency, 1, width=0.02, edgecolor='blue')
            # else:
            #     self.subplot_2.bar(l.frequency, l.intensity, width=0.02, edgecolor='blue')

        ''' Chemical Subplot '''
        self.subplot_3 = figure.add_subplot(313,
                                            axisbg='white',
                                            sharex=self.subplot_1)

        lines = self.chemical.get_all_lines(min_freq, max_freq)
        for l in lines:
            if l.intensity is None:  # or l.intensity <= 1:
                self.subplot_3.bar(l.frequency, 1, width=0.02, edgecolor='black')
            else:
                self.subplot_3.bar(l.frequency, l.intensity, width=0.02, edgecolor='blue')

        ''' Adjustments '''
        # self.matplot_widget.getFigure().subplots_adjust(top=0.95,
        #                                              bottom = 0.07,
        #                                              left = 0.05,
        #                                              right = 0.97,
        #                                              hspace=0.35,)
        self.matplot_widget.draw()

    def __populate_table(self):
        """

        :return:
        """

        row_count = self.chemical.N
        column_count = 5

        # Format Table
        self.table_widget.setRowCount(row_count)
        self.table_widget.setColumnCount(column_count)
        self.table_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.table_widget.setSortingEnabled(True)

        # Set Header Label
        self.table_widget.setHorizontalHeaderLabels(["EXP-Frequency", "Frequency", "Intensity", \
                                                     "Units", "Linelist", ])

        for i in range(0, row_count):
            # Get Row Data
            # exp_freq = self.chemical.matched_lines[i]
            exp_freq = get_frequency(conn, self.chemical.matched_lines[i])
            frequency = self.chemical.lines[i].frequency
            intensity = self.chemical.lines[i].intensity
            line_list = self.chemical.lines[i].line_list
            units = self.chemical.lines[i].units

            # Convert Data to QTableWidgetItem
            exp_freq_item = QTableWidgetItem(str(exp_freq))
            frequency_item = QTableWidgetItem(str(frequency))
            intensity_item = QTableWidgetItem(str(intensity))
            line_list_item = QTableWidgetItem(str(line_list))
            units_item = QTableWidgetItem(str(units))

            self.table_widget.setItem(i, 0, exp_freq_item)
            self.table_widget.setItem(i, 1, frequency_item)
            self.table_widget.setItem(i, 2, intensity_item)
            self.table_widget.setItem(i, 3, units_item)
            self.table_widget.setItem(i, 4, line_list_item)

        # --- Set Size Policy --- #
        self.table_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.table_widget.setMaximumWidth(600)
        self.table_widget.setFixedWidth(500)
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

        # -- Additional Options -- #
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # disallow in-table editing


class SplatalogueInfoWidget(QWidget):
    def __init__(self, chemical):
        super(SplatalogueInfoWidget, self).__init__()

        self.chemical = chemical
        self.__setup__()

    def __setup__(self):
        layout = QFormLayout()

        name_lbl = QLabel("Chemical: ")
        layout.addRow(name_lbl, QLabel(str(self.chemical.name)))

        fullname_lbl = QLabel("Name: ")
        layout.addRow(fullname_lbl, QLabel(str(self.chemical.full_name)))

        matches_lbl = QLabel("Matches: ")
        layout.addRow(matches_lbl, QLabel(str(self.chemical.N)))

        self.setLayout(layout)
