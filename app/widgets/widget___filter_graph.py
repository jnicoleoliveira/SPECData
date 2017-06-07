# Author: Jasmine N Oliveira
# Date 06/06/2017
# Updated version of AssignmentGraph..

from PyQt4.QtGui import *

from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget


class FilterGraphWidget(QWidget):
    def __init__(self):
        super(FilterGraphWidget, self).__init__()
        self.full_spectrum = False
        self.matches = False
        self.catalogue = False
        self.expected = False

        # Widgets
        self.graph_widget = MatplotlibWidget()
        self.filter_widget = FilterWidget()

        # Set Up UI
        self.__setup__()

    def __setup__(self):
        # Create Layout
        widget_layout = QHBoxLayout()
        filter_layout = QVBoxLayout()

        # Edit Components
        self.graph_widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        # Setup Filter layout
        filter_layout.addSpacerItem(QSpacerItem(QSpacerItem(30, 30, QSizePolicy.Minimum, QSizePolicy.Minimum)))
        filter_layout.addWidget(self.filter_widget)
        filter_layout.addSpacerItem(QSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)))

        # Add Components
        widget_layout.addWidget(self.graph_widget)
        widget_layout.addLayout(filter_layout)

        # Connect Checkboxes
        self.filter_widget.set_filter_connection(self.__event__filter_changed)

        self.setLayout(widget_layout)

    def __event__filter_changed(self):
        full_spectrum = self.filter_widget.full_spectrum.isChecked()
        matches = self.filter_widget.matches.isChecked()
        catalogue = self.filter_widget.catalogue.isChecked()
        expected = self.filter_widget.catalogue.isChecked()

        self.redisplay(full_spectrum, matches, catalogue, expected)

    def redisplay(self, full_spectrum, matches, catalogue, expected):
        print "redisplay"


class FilterWidget(QDockWidget):
    def __init__(self):
        super(FilterWidget, self).__init__()
        self.setMaximumWidth(200)
        # Create Filter Components
        self.full_spectrum = QCheckBox("Full Experiment Spectrum")
        self.matches = QCheckBox("Matched Lines")
        self.catalogue = QCheckBox("Catalogue")
        self.expected = QCheckBox("Expected")

        self.__setup__()

    def __setup__(self):
        # Create Overarching Frame
        frame = QFrame()
        frame_layout = QVBoxLayout()

        # Frame Settings
        frame.setFrameShadow(QFrame.Raised)
        frame.setFrameShape(QFrame.StyledPanel)

        # Add Components to layout
        frame_layout.addWidget(self.full_spectrum)
        frame_layout.addWidget(self.matches)
        frame_layout.addWidget(self.catalogue)
        frame_layout.addWidget(self.expected)
        frame_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                                   )
        # Set frame Layout
        frame.setLayout(frame_layout)
        frame_layout.setSpacing(2)

        # Set Widget Layout
        self.setWidget(frame)

        # ADDITIONAL SETTINGS #
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    def set_filter_connection(self, function):
        """
        Setts the stateChanges for checkboxes to function
        :param function: function pointer
        :return:
        """
        self.full_spectrum.stateChanged.connect(function)
        self.matches.stateChanged.connect(function)
        self.catalogue.stateChanged.connect(function)
        self.expected.stateChanged.connect(function)
