# Author: Jasmine Oliveira
# Date: 11/4/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from frames.frame___export_cleaned_lines import Ui_Dialog
from config import resources
import os


class ExportCleanedLines(QDialog):

    def __init__(self):
        super(ExportCleanedLines, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Export Cleaned Lines")
        self.resize(500, 750)

        # Variables to hold form input
        self.clean_mids_list = []
        self.save_path = None

        self.connect_buttons()

    def connect_buttons(self):

        # Get Buttons
        select_file_btn = self.ui.select_file_btn
        select_all_btn = self.ui.select_all_btn
        deselect_all_btn = self.ui.deselect_all_btn
        ok_btn = self.ui.ok_btn
        cancel_btn = self.ui.cancel_btn

        select_file_btn.clicked.connect(self.select_file)
        select_all_btn.clicked.connect(self.select_all)
        deselect_all_btn.clicked.connect(self.deselect_all)
        ok_btn.clicked.connect(self.ok)
        cancel_btn.clicked.connect(self.cancel)

    def cancel(self):
        self.close()

    def select_file(self):
        w = QWidget()
        w.resize(320, 240)
        w.setWindowTitle("Open File")
        self.save_path = QFileDialog.getOpenFileName(w, 'Open File', os.path.curdir)
        self.ui.select_file_txt.setText(self.file_path)

    def deselect_all_btn(self):
        print "DESELECT ALL"

    def select_all(self):
        print "stub"

    def ok(self):
        print "stub"
