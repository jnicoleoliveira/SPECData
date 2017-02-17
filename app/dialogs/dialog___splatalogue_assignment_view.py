# Author: Jasmine Oliveira
# Date: 02/17/2017

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget  # Matplotlib Widget


class SplatalogueAssignmentWindow(QDialog):
    def __init__(self, experiment, chemical):
        super(SplatalogueAssignmentWindow, self).__init__()

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Splatalogue Assignment Window")
        self.resize(1500, 750)

        # Data
        self.experiment = experiment
        self.chemical = chemical

        # Widgets
        self.info_widget = SplatalogueInfoWidget(chemical)
        self.table_widget = QTableWidget()
        self.matplot_widget = MatplotlibWidget()

        self.__setup__()

    def __setup__(self):
        self.__setup_layout()
        self.__populate_graph()
        self.__populate_table()

    def __setup_layout(self):
        layout = QGridLayout()

        layout.addWidget(self.info_widget, 0, 0)
        layout.addWidget(self.table_widget, 0, 1)
        layout.addWidget(self.matplot_widget, 1, 0)

        self.setLayout(layout)

    def __populate_graph(self):
        print "populate graph "

    def __populate_table(self):
        """

        :return:
        """
        print "populate table"


class SplatalogueInfoWidget(QWidget):
    def __init__(self, chemical):
        super(SplatalogueInfoWidget, self).__init__()

        self.chemical = chemical
        self.__setup__()

    def __setup__(self):
        layout = QFormLayout()

        name_lbl = QLabel("Chemical Name")
        matches_lbl = QLabel("Matches")

        layout.addRow(name_lbl, QLabel(str(self.chemical.name)))
        layout.addRow(matches_lbl, QLabel(str(self.chemical.N)))

        self.setLayout(layout)
