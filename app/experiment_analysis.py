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

class Graph():

    def __init__(self, plot_widget, experiment):
        self.plot_widget = plot_widget
        self.experiment = experiment
        self.subplot = None
        self.x = []
        self.y = []

    def set_x_list(self, x):
        self.x = x

    def set_y_list(self, y):
        self.y = y

    def add_subplot_experiment(self, pos):
        frequencies, intensities = self.experiment.get_experiment_frequencies_intensities_list()

        figure = self.plot_widget.getFigure()
        self.subplot = figure.add_subplot(pos, \
                                     axisbg='white', \
                                     xlabel="Frequency", \
                                     ylabel="Intensity", \
                                     title = 'Experiment Peaks')

        self.subplot.bar(frequencies, intensities, width=0.02, edgecolor='black')

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
                                     sharex=self.subplot, \
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
        subplot = figure.add_subplot(pos, \
                                     axisbg='white', \
                                     xlabel="Frequency", \
                                     ylabel="Intensity", \
                                     sharex=self.subplot, \
                                     title='Selected Assignments')
        color_index = 0
        for key, value in matches.iteritems():
            frequencies = []
            intensities = []
            for match in value.matches:
                frequencies.append(get_peaks.get_frequency(conn, match.pid))
                intensities.append(get_peaks.get_intensity(conn, match.pid))

            subplot.bar(frequencies, intensities, width=0.02, edgecolor=colors[color_index])
            print value.name + "\t" + colors[color_index]  # Print KEY
            color_index += 1



