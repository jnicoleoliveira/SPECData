# Author: Jasmine Oliveira
# Date: 04/4/2016
# Cleaner, more effective (refactored) version of AssignmentGraph/MainGraph

from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget

import tables.peaks_table as get_peaks
from config import conn


class ExperimentGraphWidget(MatplotlibWidget):
    FACE_COLOR = "#626262"
    EXPERIMENT_EDGE_COLOR = 'black'

    def __init__(self, experiment):
        super(ExperimentGraphWidget, self).__init__()

        self.experiment = experiment

        # -- Options --#
        self.full_spectrum = False
        self.sharey = False
        self.display_exp_assignments = False
        self.y_to_experiment_intensities = False

    ###############################################################################
    # User Functions
    ###############################################################################
    def graph_assignment_view(self, match, color):

        #####################################
        # Experiment Subplot (#1)
        #####################################
        subplot_1 = self.__add_subplot(311, "", "", "")

        if self.full_spectrum is True:
            x, y = self.get_full_experiment_frequencies_intensities()
            self.__graph_subplot(subplot_1, x, y, 'gray', bar=False)
        x, y = get_peaks.get_frequency_intensity_list(conn, self.experiment.mid)
        self.__graph_subplot(subplot_1, x, y, 'black')

        # Set Max Min
        max_x = max(x)
        min_x = min(x)

        # Share Y Option
        sharey = None
        if self.sharey is True:
            sharey = subplot_1

        #####################################
        # Assignment Subplot (#2)
        #####################################
        subplot_2 = self.__add_subplot(312, "", "", "",
                                       sharex=subplot_1, sharey=sharey,
                                       min=min_x, max=max_x)
        x, y = match.get_matches_frequency_intensity_list()
        self.__graph_subplot(subplot_2, x, y, color)

        #####################################
        # Catalogue Full Subplot (#3)
        #####################################
        subplot_3 = self.__add_subplot(313, "", "", "",
                                       sharex=subplot_1, sharey=sharey,
                                       min=min_x, max=max_x)
        x, y = get_peaks.get_frequency_intensity_list(conn, match.mid, max_x, min_x)
        self.__graph_subplot(subplot_3, x, y, color)

        self.draw()

    def set_options(self, full_spectrum=False, sharey=False,
                    y_to_experiment_intensities=False, color_experiment=False):
        self.full_spectrum = full_spectrum
        self.sharey = sharey
        self.display_exp_assignments = color_experiment
        self.y_to_experiment_intensities = y_to_experiment_intensities

    def clear(self):
        self.getFigure().clear()

    ###############################################################################
    # Private Functions
    ###############################################################################
    def __add_subplot(self, pos, title, xlabel, ylabel, sharex=None, sharey=None, min=None, max=None):

        figure = self.getFigure()
        figure.set_facecolor(ExperimentGraphWidget.FACE_COLOR)

        subplot = figure.add_subplot(pos,
                                     axisbg='white',
                                     xlabel=xlabel,
                                     ylabel=ylabel,
                                     sharex=sharex,
                                     sharey=sharey,
                                     title=title,
                                     xlim=(min, max))

        return subplot

    def __graph_subplot(self, subplot_obj, x, y, color, width=0.02, bar=True):

        if bar is True:
            subplot_obj.bar(x, y, width=width, color=color)
        else:
            subplot_obj.plot(x, y, color=color)

    def full_spectrum_exists(self):
        import os
        from config import db_dir
        file_path = os.path.join(db_dir, "experiments", (str(self.experiment.mid) + ".sp"))
        return os.path.exists(file_path)

    def get_full_experiment_frequencies_intensities(self):
        if self.full_spectrum_exists is True:
            import os
            from config import db_dir
            file_path = os.path.join(db_dir, "experiments", (str(self.experiment.mid) + ".sp"))
            full_spectrum_intensities = []
            full_spectrum_frequencies = []
            with open(file_path) as f:
                for line in f:
                    point = str.split(line.strip())
                    full_spectrum_frequencies.append(float(point[0]))
                    full_spectrum_intensities.append(float(point[1]))

            return full_spectrum_frequencies, full_spectrum_intensities

        return [], []
