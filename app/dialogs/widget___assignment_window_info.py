# Author: Jasmine Oliveira
# Date: 09/07/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from frames.frame___assignment_info_widget import Ui_Form
from config import conn
from tables.get import get_peaks

class AssignmentInfoWidget(QWidget):

    def __init__(self, match):
        super(AssignmentInfoWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle(match.name)

        self.match = match

        self.setup()
        self.show()

    def setup(self):
        self.ui.experiment_name_lbl.setText(self.match.name)
        self.ui.peaks_assigned_val.setText(str(len(self.match.matches)))
        self.ui.total_peaks_val.setText(str(get_peaks.get_peak_count(conn, self.match.mid)))
        self.ui.presence_val_lbl.setText(str(self.match.p * 100))
        self.ui.info_val_lbl.setText("[stub]")
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
