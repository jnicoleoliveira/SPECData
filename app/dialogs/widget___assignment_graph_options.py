# Author: Jasmine Oliveira
# Date: 09/14/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from frames.frame___assignment_graph_options import Ui_Form
from config import resources
import os


class AssignmentGraphOptionsWidget(QWidget):

    def __init__(self):
        super(AssignmentGraphOptionsWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Set up group boxes for full layout
        self.ui.matches_selections_grpbox.setLayout(self.ui.matches_layout)

        # Options
        self.full_spectrum_chk = self.ui.full_spectrum_chk
        self.color_experiment_chk = self.ui.color_experiment_chk
        self.sharey_chk = self.ui.sharey_chk
        self.y_exp_intensities_chk = self.ui.y_exp_intensities_chk

        # Matches
        self.redisplay_btn = self.ui.redisplay_btn

        self.add_icons()

    def add_icons(self):
        self.redisplay_btn.setIcon(QIcon(QPixmap(os.path.join(resources, 'redisplay-graph.png'))))