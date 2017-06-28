# Author: Jasmine N Oliveira
# Date 06/06/2017
# Updated version of AssignmentGraph..

from PyQt4.QtGui import *
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget

from colors import *
from config import conn
from tables.peaks_table import *


class FilterGraphWidget(QWidget):
    def __init__(self, experiment_mid, match):
        super(FilterGraphWidget, self).__init__()
        self.molecule_match = match
        self.experiment_mid = experiment_mid

        self.full_spectrum = False
        self.experiment = False
        self.matches = False
        self.catalog = False
        self.expected = False

        self.catalog_peaks = None
        self.experiment_peaks = None
        self.match_peaks = None
        self.expected_peaks = None

        self.displayed = 0
        self.has_full_spectrum = False

        # Graphing Limits (from experiment max/min)
        self.xmax = None
        self.xmin = None
        self.ymax = None

        # Colors
        self.catalog_color = GREEN
        self.experiment_color = PASTEL_PURPLE
        self.expected_color = BLUE
        self.matches_color = PASTEL_RED

        # Widgets
        self.graph_widget = AssignmentGraphWidget()
        self.filter_widget = FilterWidget()

        # Set Up UI
        self.__setup__()

    def __setup__(self):
        self.__setup_ui__()
        self.xmax = get_max_frequency(conn, self.experiment_mid)
        self.xmin = get_min_frequency(conn, self.experiment_mid)
        self.ymax = get_max_intensity(conn, self.experiment_mid)

    def __setup_ui__(self):
        # Create Layout
        widget_layout = QHBoxLayout()
        filter_layout = QVBoxLayout()
        group_box = QGroupBox()

        # -------- Edit Components -------------- #
        self.graph_widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        # Setup Filter layout
        # filter_layout.addSpacerItem(QSpacerItem(QSpacerItem(30, 69, QSizePolicy.Minimum, QSizePolicy.Minimum)))
        # filter_layout.addWidget(self.filter_widget)
        # filter_layout.addSpacerItem(QSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)))

        # Setup Dock
        l = QVBoxLayout()
        l.addWidget(self.filter_widget)
        l.setMargin(0)
        group_box.setLayout(l)
        # group_box.setStyleSheet("QGroupBox { border:0.5px solid white;}")
        # filter_dock.setWidget(self.filter_widget)

        # Add Components
        widget_layout.addWidget(self.graph_widget)
        widget_layout.addWidget(group_box)
        # widget_layout.addLayout(filter_layout)
        widget_layout.setSpacing(0)
        widget_layout.setMargin(0)

        # Connect Checkboxes
        self.filter_widget.set_filter_connection(self.__event__filter_changed)
        self.setLayout(widget_layout)

        # Determine if
        self.filter_widget.full_spectrum.setDisabled(True)
        self.filter_widget.full_spectrum.setStyleSheet("color:gray")
        self.filter_widget.full_spectrum.setWhatsThis("Full Spectrum is not available.")

        # Additional Settings
        self.setStyleSheet("background:" + FOREGROUND)
    def __event__filter_changed(self):
        full_spectrum = self.filter_widget.full_spectrum.isChecked()
        matches = self.filter_widget.matches.isChecked()
        catalog = self.filter_widget.catalogue.isChecked()
        expected = self.filter_widget.expected.isChecked()
        experiment = self.filter_widget.experiment_peaks.isChecked()

        self.reset_graph()
        self.displayed = 0
        if full_spectrum is True:
            print "should graph"

        if catalog is True:
            self.graph_catalog()

        if experiment is True:
            self.graph_experiment()

        if expected is True:
            self.graph_expected()

        if matches is True:
            self.graph_matches()

            # if matches != self.matches:
            #     if matches == True:
            #         self.reset_graph()
            #         self.graph_matches()
            #     else:
            #         self.matches = False
            #
            # if catalog != self.catalog:
            #     if catalog == True:
            #         self.graph_catalog()
            #     else:
            #         self.catalog = False
            #         self.reset_graph()
            #
            # if expected != self.expected:
            #     if expected == True:
            #         self.graph_expected()
            #     else:
            #         self.expected = False
            #         self.reset_graph()
            #
            # if experiment != self.experiment:
            #     if experiment == True:
            #         self.graph_experiment()
            #     else:
            #         self.experiment = False
            #         self.reset_graph()



            # self.redisplay(full_spectrum, matches, catalogue, expected)

        self.graph_widget.getFigure().tight_layout(pad=0, w_pad=0.5, h_pad=1.0)

    def redisplay(self, full_spectrum, matches, catalogue, expected):
        print "redisplay"

    # ------------------------
    # Graphing
    # ------------------------
    def graph_matches(self):
        self.matches = True
        if self.match_peaks is None:
            self._get_matches_peaks()

        self.displayed += 1
        self.graph_widget.plot_peaks(self.match_peaks[0], self.match_peaks[1], self.matches_color,
                                     xmin=self.xmin, xmax=self.xmax, displayed=self.displayed,
                                     label="Match")
        self.graph_widget.plot_scatter(self.match_peaks[0], self.match_peaks[1], self.matches_color)

    def graph_catalog(self):
        self.catalog = True
        if self.catalog_peaks is None:
            self._get_catalog_peaks()

        self.displayed += 1
        self.graph_widget.plot_peaks(self.catalog_peaks[0], self.catalog_peaks[1], self.catalog_color, mirror=True,
                                     xmax=self.xmax, xmin=self.xmin, displayed=self.displayed,
                                     label="Catalog")

    def graph_experiment(self):
        self.experiment = True
        if self.experiment_peaks is None:
            self._get_experiment_peaks()

        self.displayed += 1
        self.graph_widget.plot_peaks(self.experiment_peaks[0], self.experiment_peaks[1], self.experiment_color,
                                     xmax=self.xmax, xmin=self.xmin, displayed=self.displayed,
                                     label="Experiment")

    def graph_expected(self):
        self.expected = True
        if self.expected_peaks is None:
            self._get_expected_peaks()

        self.displayed += 1
        self.graph_widget.plot_peaks(self.expected_peaks[0], self.expected_peaks[1], self.expected_color,
                                     xmax=self.xmax,
                                     xmin=self.xmin, displayed=self.displayed,
                                     label="Expected")

    # ------------------------
    # Get Data
    # ------------------------
    def _get_matches_peaks(self):
        import tables.peaks_table as get_peaks
        # Get Data
        frequencies = []
        intensities = []
        for p in self.molecule_match.matches:
            frequencies.append(get_peaks.get_frequency(conn, p.exp_pid))
            intensities.append(get_peaks.get_intensity(conn, p.exp_pid))
        self.match_peaks = [frequencies, intensities]

    def _get_experiment_peaks(self):
        # Get Data
        frequencies, intensities = get_frequency_intensity_list(conn, self.experiment_mid)
        self.experiment_peaks = [frequencies, intensities]

    def _get_catalog_peaks(self):
        import tables.peaks_table as get_peaks
        # Get Data
        frequencies, intensities = get_peaks.get_frequency_intensity_list(conn, self.molecule_match.mid)
        normalize = get_peaks.get_max_intensity(conn, self.experiment_mid)
        for i in intensities: i = i / normalize /2
        self.catalog_peaks = [frequencies, intensities]

    def _get_expected_peaks(self):

        import tables.peaks_table as get_peaks

        if self.catalog_peaks is None:
            self._get_catalog_peaks()

        mfrequencies = []
        for p in self.molecule_match.matches:
            mfrequencies.append(get_peaks.get_frequency(conn, p.pid))

        frequencies = []
        intensities = []
        for i in range(0, len(self.catalog_peaks[0])):
            frequency = self.catalog_peaks[0][i]

            if frequency not in mfrequencies:
                intensity = self.catalog_peaks[1][i]
                frequencies.append(frequency)
                intensities.append(intensity)

        self.expected_peaks = [frequencies, intensities]

    def reset_graph(self):
        self.graph_widget.reset()


class FilterWidget(QGroupBox):
    def __init__(self):
        super(FilterWidget, self).__init__()
        self.setMaximumWidth(150)

        # Settings
        self.setTitle("Filter")
        # Create Filter Components
        self.full_spectrum = QCheckBox("Full Spectrum")
        self.experiment_peaks = QCheckBox("Experiment Peaks")
        self.matches = QCheckBox("Matched Peaks")
        self.catalogue = QCheckBox("Catalog Peaks")
        self.expected = QCheckBox("Expected Peaks")

        self.__setup__()

    def __setup__(self):
        # Create Overarching Frame
        frame = QFrame()
        frame_layout = QVBoxLayout()

        # Frame Settings
        frame.setFrameShadow(QFrame.Raised)
        frame.setFrameShape(QFrame.StyledPanel)

        # Create Componenets
        header_1 = QLabel("Data")
        header_1.setMargin(2)
        header_1.setStyleSheet("background :" + ACCENT_LIGHT)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        # line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color:white")
        # Add Components to layout
        frame_layout.addWidget(header_1)
        #frame_layout.addWidget(line)
        frame_layout.addWidget(self.full_spectrum)
        frame_layout.addWidget(self.experiment_peaks)
        frame_layout.addWidget(self.matches)
        frame_layout.addWidget(self.catalogue)
        frame_layout.addWidget(self.expected)
        frame_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Set frame Layout
        frame.setLayout(frame_layout)
        frame_layout.setSpacing(2)

        # Set Widget Layout
        # self.setWidget(frame)
        self.setLayout(frame_layout)
        # ADDITIONAL SETTINGS #
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setStyleSheet("background-color:" + FOREGROUND + "; " +
                           "color:" + "WHITE" + ";")
        self.full_spectrum.setWhatsThis("Full Spectrum of the experiment")
        self.experiment_peaks.setWhatsThis("Peaks of the experiment spectrum.")
        self.matches.setWhatsThis("Peaks of the experiment that are considered matched to the catalog.")
        self.catalogue.setWhatsThis("Peaks of the associated Catalog file.")
        self.expected.setWhatsThis("Catalog lines that are not considered matches.")

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
        self.experiment_peaks.stateChanged.connect(function)


class AssignmentGraphWidget(MatplotlibWidget):
    def __init__(self):
        super(AssignmentGraphWidget, self).__init__()
        self.ax = None

        self.y_axis_on = False

        self.__setup__()

    def __setup__(self):

        figure = self.getFigure()

        # --- Color Scheme -- #
        figure.set_facecolor(FOREGROUND)  # Background
        self.setStyleSheet("QWidget { background-color: " + FOREGROUND + "}")
        # --- Axis Color Scheme --- #
        ax = figure.add_subplot(111, axisbg=FOREGROUND)
        ax.spines['top'].set_color(FOREGROUND)
        ax.spines['right'].set_color(FOREGROUND)
        ax.spines['bottom'].set_color('#F5F5F5')
        # ax.spines['top'].set_color('#F5F5F5')
        # ax.spines['right'].set_color('#F5F5F5')
        #ax.spines['left'].set_color('#F5F5F5')
        ax.tick_params(axis='x', colors='#F5F5F5')
        ax.title.set_color('#F5F5F5')

        # -- Labels Font and Color Scheme -- #
        font = {'style': 'italic', 'size': 10, 'color': '#F5F5F5'}
        ax.set_xlabel('frequency', font)

        if self.y_axis_on is True:
            ax.set_ylabel('intensity', font)
            ax.spines['left'].set_color('#F5F5F5')
            ax.tick_params(axis='y', colors='#F5F5F5')
        else:
            ax.spines['left'].set_color(FOREGROUND)
            ax.tick_params(axis='y', colors=FOREGROUND)

        self.ax = ax
        # --- Spacing and Borders -- #
        self.fig.tight_layout()

        # figure.subplots_adjust(left=0.1, right=0.97, top=0.98, bottom=0.03)
        #figure.set_tight_layout(figure.get_tight_layout())
        # # --- Legend Settings --- #
        # self.ax.legend(loc=0)
        # legend = ax.legend()
        # legend.set_title('Legend', prop={'size':14})
        #     ax.legend(loc=0, ncol=1, bbox_to_anchor=(0, 0, 1, 1),
        #                     prop=font, fancybox=True, shadow=True, title='LEGEND')
        # f
        # ax.setp(legend.get_title(), fontsize='xx-small')
        # -- Sample plotting -- #
        # ax.plot([1,2,3,4,5], [1,2,3,4,5], color=YELLOW)
        # ax.bar([1,2,3,4,5], [1,2,3,4,5], width=0.02, color=BLUE)
        # ax.bar([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], width=0.02, color=GREEN, bottom=-5)

    def plot_peaks(self, frequencies, intensities, color, mirror=False, xmax=None, xmin=None, displayed="",
                   label=""):

        if mirror is False:
            for i in range(0, len(frequencies)):
                if frequencies[i] < xmin or frequencies[i] > xmax:
                    continue
                else:
                    self.ax.bar(frequencies[i], intensities[i], width=0.02, edgecolor=color, color=color)
        else:
            for i in range(0, len(frequencies)):
                if frequencies[i] < xmin or frequencies[i] > xmax:
                    continue
                else:
                    self.ax.bar(frequencies[i], -intensities[i], width=0.02, bottom=0, edgecolor=color,
                                color=color)

        # Add Legend
        self.ax.bar((xmin + xmax) / 2, 0, label=label, color=color)  # invisible bar
        from matplotlib.font_manager import FontProperties
        font = FontProperties()
        font.set_size('small')
        legend = self.ax.legend(loc=0, shadow=True, fancybox=True, title="Legend", prop=font)
        #legend.set_title('Legend',prop={'size':10})
        self.draw()
        self.fig.tight_layout()

    def plot_scatter(self, frequencies, intensities, color):
        self.ax.scatter(frequencies, intensities, c=color)
        self.fig.tight_layout()

    def reset(self):
        self.getFigure().clear()
        self.__setup__()
