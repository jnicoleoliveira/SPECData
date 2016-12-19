# Author: Jasmine Oliveira
# Date: 09/14/2016

import os

from PyQt4.QtGui import *

from app.dialogs.frames.experiment_view.frame___main_graph_options_widget import Ui_Form
from config import resources


class MainGraphOptionsWidget(QWidget):

    def __init__(self):
        super(MainGraphOptionsWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Set up group boxes for full layout
        self.ui.matches_selections_grpbox.setLayout(self.ui.matches_layout)
        self.ui.options_grpbox.setLayout(self.ui.options_layout)
        self.ui.view_grpbox.setLayout(self.ui.view_layout)

        # Options
        self.full_spectrum_chk = self.ui.full_spectrum_chk
        self.color_experiment_chk = self.ui.color_experiment_chk
        self.sharey_chk = self.ui.sharey_chk
        self.y_exp_intensities_chk = self.ui.y_exp_intensities_chk

        # Matches
        self.redisplay_btn = self.ui.redisplay_btn
        self.deselect_all_btn = self.ui.deselect_all_btn
        self.select_all_btn = self.ui.select_all_btn

        # View
        self.show_invalid_btn = self.ui.show_invalid_btn
        self.show_validations_btn = self.ui.show_validations_btn
        self.show_pending_btn = self.ui.show_pending_btn

        self.add_icons()

    def add_icons(self):
        self.redisplay_btn.setIcon(QIcon(QPixmap(os.path.join(resources, 'redisplay-graph.png'))))
        self.deselect_all_btn.setIcon(QIcon(QPixmap(os.path.join(resources, 'deselect-all.png'))))
        self.select_all_btn.setIcon(QIcon(QPixmap(os.path.join(resources, 'select-all.png'))))
        self.show_invalid_btn.setIcon(QIcon(QPixmap(os.path.join(resources, 'show-validations.png'))))
        self.show_validations_btn.setIcon(QIcon(QPixmap(os.path.join(resources, 'show-validations.png'))))
        self.show_pending_btn.setIcon(QIcon(QPixmap(os.path.join(resources, 'show-validations.png'))))
