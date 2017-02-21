# Author: Jasmine Oliveira
# Date: 02/17/2017

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget  # Matplotlib Widget

import images


class SplatalogueAssignmentWindow(QDialog):
    def __init__(self, experiment, chemical):
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

        self.__setup__()

    def __setup__(self):
        self.setStyleSheet(
            "background-color: rgb(48, 48, 48);\ngridline-color: rgb(195, 195, 195);\ncolor: rgb(255, 255, 255);\n")
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
        validate_btn = QPushButton(QIcon(images.VALIDATE_ICON), "")
        invalidate_btn = QPushButton(QIcon(images.INVALIDATE_ICON), "")
        cancel_btn = QPushButton("Cancel")
        # -- Settings -- #
        bottom_frame.setFrameShadow(QFrame.Raised)
        bottom_frame.setFrameShape(QFrame.StyledPanel)
        # -- Add Widgets -- #
        frame_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        frame_layout.addWidget(validate_btn)
        frame_layout.addWidget(invalidate_btn)
        frame_layout.addWidget(cancel_btn)
        bottom_frame.setLayout(frame_layout)

        ''' Add '''
        outer_layout.addLayout(layout)
        outer_layout.addWidget(bottom_frame)

        self.setLayout(outer_layout)

    def __populate_graph(self):
        print "populate graph "

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
        self.table_widget.setHorizontalHeaderLabels(["Experiment Frequency", "Frequency", "Intensity", \
                                                     "Units", "Linelist", ])

        for i in range(0, row_count):
            # Get Row Data
            exp_freq = self.chemical.matched_lines[i]
            frequency = self.chemical.lines[i].frequency
            intensity = self.chemical.lines[i].intensity
            line_list = self.chemical.lines[i].linelist
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
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
