# Author: Jasmine N Oliveira
# Date 06/06/2017
# Updated version of AssignmentGraph..

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget

import tables.peaks_table as get_peaks
from config import conn

class FilterGraph(QWidget):

    def __init__(self, match, color, experiment):
        super(FilterGraph, self).__init__()
        self.full_spectrum = False
        self.matches = False
        self.catalogue = False
        self.expected = False
        # Widgets
        self.graph_widget = MatplotlibWidget()

    class Filter(QDockWidget):

        def __init__(self):
            super(FilterGraph, self).__init__()

            self.__setup__()

        def __setup__(self):

            # Create Filter Components
            full_spectrum = QCheckBox("Full Experiment Spectrum")
            matches = QCheckBox("Matched Lines")
            catalogue = QCheckBox("Catalogue")
            expected = QCheckBox("Expected")

            self.layout = QVBoxLayout()

            self.layout.addWidget(full_spectrum)
            self.layout.addWidget(matches)
            self.layout.addWidget(catalogue)
            self.layout.addWidget(expected)

            connect()






