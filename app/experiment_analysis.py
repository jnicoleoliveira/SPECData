# Author: Jasmine Oliveira
# Date: 08/24/2016

from config import conn
from tables.get import get_peaks
#from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTK

class MainGraph:

    def __init__(self, plot_widget, options_widget, experiment):
        self.plot_widget = plot_widget
        self.options_widget = options_widget

        self.experiment = experiment
        self.figure = self.plot_widget.getFigure()
        self.subplot_1 = None
        self.subplot_2 = None

        # Set Options to default
        self.full_spectrum = False
        self.sharey = False
        self.display_exp_assignments = False
        self.y_to_experiment_intensities = False
        self.show_validations = True

        self.home_xlim = None
        self.home_ylim = None

        self.last_xlim = None
        self.last_ylim = None
        self.full_spectrum_intensities = None
        self.full_spectrum_frequencies = None

        # -- Event Handling --#
        self.xlims = None
        self.on_bar = False
        self.x_bar = None
        self.hover_color_bar = None
        self.cid_hover = self.figure.canvas.mpl_connect('motion_notify_event', self.on_plot_hover)

    def set_experiment(self, experiment):
        self.experiment = experiment

    def set_plot_widget(self, plot_widget):
        self.plot_widget = plot_widget

    def get_experiment_frequencies_intensities(self):
        """
        Returns the appropriate frequencies and intensities list of the experiment to graph
        based on the state of the options.
        :return: list of frequencies, list of intensities
        """
        # if show validations, get all experiment peaks
        if self.show_validations:
            return self.experiment.get_experiment_frequencies_intensities_list()

        # otherwise show only unvalidated
        return self.experiment.get_unvalidated_experiment_intensities_list()

    def add_subplot_experiment(self, pos, color):

        # Get experiment frequency and intensities to graph
        frequencies, intensities = self.get_experiment_frequencies_intensities()

        figure = self.plot_widget.getFigure()
        figure.set_facecolor("#626262")

        self.subplot_1 = figure.add_subplot(pos, \
                                     axisbg='white', \
                                     xlabel="Frequency", \
                                     ylabel="Intensity", \
                                     title = 'Experiment: ' + self.experiment.name +' Peaks')

        self.subplot_1.bar(frequencies, intensities, width=0.02, edgecolor=color, picker=3)

        self.remove_hover_status()
        self.xlims = frequencies


    def add_subplot_all_assignments(self, pos):
        colors = ['green', 'blue', 'yellow', '#ff6500', 'cyan', 'magenta', '#008B8B', '#8B0000', '#FA8072', '#FF69B4',
                  '#BDB76B', '#663399', '#7cfc00', ]
        color_index = 0

        figure = self.plot_widget.getFigure()
        subplot = figure.add_subplot(pos, \
                                     axisbg='white', \
                                     xlabel="Frequency", \
                                     ylabel="Intensity",\
                                     sharex=self.subplot_1, \
                                     title='Assignments')
        for key, value in self.experiment.molecule_matches.iteritems():
            frequencies = []
            intensities = []
            for match in value.matches:
                frequencies.append(get_peaks.get_frequency(conn, match.pid))
                intensities.append(get_peaks.get_intensity(conn, match.pid))

            subplot.bar(frequencies, intensities, width=0.02, edgecolor=colors[color_index])
            print value.name + "\t" + colors[color_index]  # Print KEY
            color_index += 1

    def add_subplot_selected_assignments(self, pos, matches, colors):

        if len(matches) != len(colors):
            return

        figure = self.plot_widget.getFigure()
        figure.set_facecolor("#626262")

        # Create Subplot
        if self.sharey is True:
            # Subplot with sharey of subplot_!
            subplot_2 = figure.add_subplot(pos, \
                                        axisbg='white', \
                                        xlabel="Frequency", \
                                        ylabel="Intensity", \
                                        sharex=self.subplot_1,\
                                        sharey=self.subplot_1, \
                                        title='Selected Assignments')
        else:
            # No sharey
            subplot_2 = figure.add_subplot(pos, \
                                           axisbg='white', \
                                           xlabel="Frequency", \
                                           ylabel="Intensity", \
                                           sharex=self.subplot_1, \
                                           title='Selected Assignment')
        self.subplot_2 = subplot_2

        color_index = 0
        if self.y_to_experiment_intensities is False:
            for match in matches:
                frequencies = []
                intensities = []
                for p in match.matches:
                    frequencies.append(get_peaks.get_frequency(conn, p.pid))
                    intensities.append(get_peaks.get_intensity(conn, p.pid))

                subplot_2.bar(frequencies, intensities, width=0.02, edgecolor=colors[color_index])
                print match.name + "\t" + colors[color_index]  # Print KEY
                color_index += 1
        else:
            for match in matches:
                frequencies = []
                intensities = []
                for p in match.matches:
                    frequencies.append(get_peaks.get_frequency(conn, p.pid))
                    intensities.append(get_peaks.get_intensity(conn, p.exp_pid))

                subplot_2.bar(frequencies, intensities, width=0.02, edgecolor=colors[color_index])
                print match.name + "\t" + colors[color_index]  # Print KEY
                color_index += 1

    def add_full_experiment_spectrum(self, pos, color):

        if self.full_spectrum_frequencies is None:
            import os
            from config import db_dir
            file_path = os.path.join(db_dir, "experiments", (str(self.experiment.mid) + ".sp"))
            self.full_spectrum_intensities = []
            self.full_spectrum_frequencies = []
            with open(file_path) as f:
                for line in f:
                    point = str.split(line.strip())
                    self.full_spectrum_frequencies.append(float(point[0]))
                    self.full_spectrum_intensities.append(float(point[1]))

        self.subplot_1.plot(self.full_spectrum_frequencies, self.full_spectrum_intensities, color=color)

    def draw(self):
        self.plot_widget.draw()

    def clear(self):
        """
        Stores last zoom coordinates, clears subplot
        :return:
        """
        # -- Store last zoom coordinates -- #
        self.last_xlim, self.last_ylim = self.get_zoom_coordinates()

        # -- Clear Plot -- #
        self.subplot_1.clear()
        self.plot_widget.getFigure().clear()

    def full_spectrum_exists(self):
        import os
        from config import db_dir
        file_path = os.path.join(db_dir, "experiments", (str(self.experiment.mid) + ".sp"))
        return os.path.exists(file_path)

    def set_options(self, full_spectrum=False, sharey=False, y_to_experiment_intensities=False, color_experiment=False, show_validations=True):
        self.full_spectrum = full_spectrum
        self.sharey = sharey
        self.display_exp_assignments = color_experiment
        self.y_to_experiment_intensities = y_to_experiment_intensities
        self.show_validations = show_validations

    def graph(self, matches, colors):
        if self.full_spectrum is True:
            self.add_subplot_experiment(211, 'black')
            self.add_full_experiment_spectrum(211, 'gray')
        else:
            self.add_subplot_experiment(211, 'black')

        self.add_subplot_selected_assignments(212, matches, colors)
        self.plot_widget.getFigure().subplots_adjust(top=0.95,
                                                     bottom = 0.07,
                                                     left = 0.05,
                                                     right = 0.97,
                                                     hspace=0.35,)

        if self.last_xlim is not None or self.last_ylim is not None:
            self.subplot_1.set_xlim(self.last_xlim)
            self.subplot_1.set_ylim(self.last_ylim)
            self.subplot_2.set_xlim(self.last_xlim)
            self.subplot_2.set_ylim(self.last_ylim)
        #else:
        #    NavigationToolbar2GTK.push_current()

    def get_zoom_coordinates(self):
        """
        Determines the current zoom coordinates
        :return: xlim, ylim
        """
        #from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget
        #self.plot_widget = MatplotlibWidget()

        figure = self.plot_widget.getFigure()
        xlim = self.subplot_1.axes.get_xlim()
        ylim = self.subplot_1.axes.get_ylim()

        return xlim, ylim

    def remove_hover_status(self):

        if self.hover_color_bar is not None:
            try:
                self.hover_color_bar.remove()
            except ValueError:
                print "not removing"
            self.hover_color_bar = None
        self.on_bar = False
        self.x_bar = None

    def on_plot_hover(self, event):
        xdata = event.xdata

        if xdata is None:
        #    if self.on_bar is True:
        #        self.remove_hover_status()
            return

        #if self.on_bar is True:
        #    if not (0 >= (self.x_bar - xdata) <= 0.5):
        #        self.remove_hover_status()
        #    return

        for curve in self.xlims:
            if curve - xdata <= 1 and curve - xdata >= 0:

                if(curve is not self.x_bar):

                    if self.hover_color_bar is not None:
                        self.remove_hover_status()

                    self.x_bar = curve
                    self.on_bar = True
                    self.hover_color_bar = self.subplot_1.bar(curve, 1,\
                                                              edgecolor='red',\
                                                              facecolor ='black',
                                                              width=0.5,
                                                              picker=True)
                    self.draw()
                    return


class Graph:

    def __init__(self, plot_widget, experiment):
        self.plot_widget = plot_widget
        self.experiment = experiment
        self.subplot_1 = None
        self.subplot_2 = None
        self.x = []
        self.y = []

    def set_x_list(self, x):
        self.x = x

    def set_y_list(self, y):
        self.y = y

    def add_subplot_experiment(self, pos):
        frequencies, intensities = self.experiment.get_experiment_frequencies_intensities_list()

        figure = self.plot_widget.getFigure()
        figure.set_facecolor("#626262")

        self.subplot_1 = figure.add_subplot(pos, \
                                     axisbg='white', \
                                     xlabel="Frequency", \
                                     ylabel="Intensity", \
                                     title = 'Experiment: ' + self.experiment.name +' Peaks')

        self.subplot_1.bar(frequencies, intensities, width=0.02, edgecolor='black')

    def draw(self):
        self.plot_widget.draw()

    def add_subplot_all_assignments(self, pos):
        colors = ['green', 'blue', 'yellow', '#ff6500', 'cyan', 'magenta', '#008B8B', '#8B0000', '#FA8072', '#FF69B4',
                  '#BDB76B', '#663399', '#7cfc00', ]
        color_index = 0

        figure = self.plot_widget.getFigure()
        subplot = figure.add_subplot(pos, \
                                     axisbg='white', \
                                     xlabel="Frequency", \
                                     ylabel="Intensity",\
                                     sharex=self.subplot_1, \
                                     title='Assignments')
        for key, value in self.experiment.molecule_matches.iteritems():
            frequencies = []
            intensities = []
            for match in value.matches:
                frequencies.append(get_peaks.get_frequency(conn, match.pid))
                intensities.append(get_peaks.get_intensity(conn, match.pid))

            subplot.bar(frequencies, intensities, width=0.02, edgecolor=colors[color_index])
            print value.name + "\t" + colors[color_index]  # Print KEY
            color_index += 1

    def add_subplot_selected_assignments(self, pos, matches, colors, sharey=None):

        if len(matches) != len(colors):
            return

        figure = self.plot_widget.getFigure()
        figure.set_facecolor("#626262")

        subplot_2 = figure.add_subplot(pos, \
                                    axisbg='white', \
                                    xlabel="Frequency", \
                                    ylabel="Intensity", \
                                    sharex=self.subplot_1,\
                                    sharey=sharey, \
                                    title='Selected Assignments')
        color_index = 0
        for match in matches:
            frequencies = []
            intensities = []
            for p in match.matches:
                frequencies.append(get_peaks.get_frequency(conn, p.pid))
                intensities.append(get_peaks.get_intensity(conn, p.pid))

            subplot_2.bar(frequencies, intensities, width=0.02, edgecolor=colors[color_index])
            print match.name + "\t" + colors[color_index]  # Print KEY
            color_index += 1

    def add_subplot_full_spectrum(self, pos, mid, color, sharey=None):
        frequencies, intensities = get_peaks.get_frequency_intensity_list(conn, mid)

        figure = self.plot_widget.getFigure()
        figure.set_facecolor("#626262")

        subplot = figure.add_subplot(pos, \
                                     axisbg='white', \
                                     xlabel="Frequency", \
                                     ylabel="Intensity", \
                                     sharex=self.subplot_1, \
                                     sharey=sharey,  \
                                     title='Full Spectrum')

        subplot.bar(frequencies, intensities, width=0.02, edgecolor=color)

    def clear(self):
        self.subplot_1.clear()
        self.plot_widget.getFigure().clear()