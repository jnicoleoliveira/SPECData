# Author: Jasmine Oliveira
# Date: 09/07/2016

from PyQt4.QtGui import *

import tables.peaks_table as peaks_table
from app.dialogs.frames.assignment_view.frame___assignment_info_widget import Ui_Form
from config import conn
from tables.knowninfo_table import get_notes


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
        self.ui.total_peaks_val.setText(str(peaks_table.get_peak_count(conn, self.match.mid)))
        self.ui.presence_val_lbl.setText(str(self.match.p * 100))
        self.set_info_text()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    def set_info_text(self):
        mid = self.match.mid

        try:
            self.ui.info_val_lbl.setText(get_notes(conn, mid))
        except TypeError:
            self.ui.info_val_lbl.setText("(Splatalogue Entry)")

    def set_name(self, text):
        self.ui.experiment_name_lbl.setText(text)
