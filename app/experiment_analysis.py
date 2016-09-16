# Author: Jasmine Oliveira
# Date: 08/24/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUi
import pyqtgraph as pg
import matplotlib.pyplot as pyplot
import numpy as np
from functions.experiment import Experiment
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget

from tables.get import get_peaks
from config import conn

class MainGraph():
    def __init__(self, plot_widget, options_widget, experiment):
        self.plot_widget = plot_widget
        self.options_widget = options_widget
        self.experiment = experiment
        self.subplot_1 = None
        self.subplot_2 = None

        # Set Options to default
        self.full_spectrum = False
        self.sharey = False
        self.display_exp_assignments = False
        self.y_to_experiment_intensities = False

        self.full_spectrum_intensities = None
        self.full_spectrum_frequencies = None

    def set_experiment(self, experiment):
        self.experiment = experiment

    def set_plot_widget(self, plot_widget):
        self.plot_widget = plot_widget

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
        self.subplot_1.clear()
        self.plot_widget.getFigure().clear()

    def set_options(self, full_spectrum=False, sharey=False, y_to_experiment_intensities=False, color_experiment=False):
        self.full_spectrum = full_spectrum
        self.sharey = sharey
        self.display_exp_assignments = color_experiment
        self.y_to_experiment_intensities = y_to_experiment_intensities

    def graph(self, matches, colors):
        self.add_subplot_experiment(211)
        self.add_subplot_selected_assignments(212, matches, colors)

        self.plot_widget.getFigure().subplots_adjust(top=0.95,
                                                     bottom = 0.07,
                                                     left = 0.05,
                                                     right = 0.97,
                                                     hspace=0.35,)
        if self.full_spectrum is True:
            self.add_full_experiment_spectrum(211, 'grey')


class Graph():

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
        import tables.get.get_peaks
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