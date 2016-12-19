from PyQt4.QtCore import *
from PyQt4.QtGui import *

from dialog___experiment_view import ExperimentView


class OpenExperimentView(QDialog):

    def __init__(self, name, mid):
        super(OpenExperimentView, self).__init__()
        self.resize(0, 0)
        self.new_window = None

        self.show_experiment(name, mid)


    def show_experiment(self, name, mid):
        """Opens the experiment View"""
        self.new_window = ExperimentView(name, mid)
        self.new_window.show()
