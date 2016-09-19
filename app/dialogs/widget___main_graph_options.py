# Author: Jasmine Oliveira
# Date: 09/14/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from frames.frame___main_graph_options_widget import Ui_Form


class MainGraphOptionsWidget(QWidget):

    def __init__(self):
        super(MainGraphOptionsWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.full_spectrum_chk = self.ui.full_spectrum_chk
        self.color_experiment_chk = self.ui.color_experiment_chk
        self.sharey_chk = self.ui.sharey_chk
        self.y_exp_intensities_chk = self.ui.y_exp_intensities_chk
