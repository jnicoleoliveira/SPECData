# Author: Jasmine Oliveira
# Date 08/30/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from frames.frame___molecule_selection_widget import Ui_ScrollArea

from dialog___assignment_window import AssignmentWindow
from config import resources
import os


class MoleculeSelectionWidget(QWidget):

    def __init__(self, experiment):
        super(MoleculeSelectionWidget, self).__init__()
        self.ui = Ui_ScrollArea()
        self.ui.setupUi(self)
        self.setLayout(self.ui.gridLayout)
        self.setWindowTitle('Matches')

        self.experiment = experiment
        self.elements = {}
        self.size = 0
        self.selected = []
        self.show()

        # Initialize Color Wheel
        self.colorWheel = GraphColorWheel()
        self.colorWheel.import_color_wheel(os.path.join(resources, 'graphing_colors'))

    def add_row(self, match):
        """
        Adds a Molecule Row to MoleculeSelection Widget, and list of elements.
        Row consists of the following widgets:
            color_lbl (color associated with molecule match)
            checkbox  (checkbox associated with selecting a molecule match for graphing)
            more_btn  (button associated with opening AssignmentWindow(mid)
            probability_lcd (QLCDNumber with probability of match)
        :param match: MoleculeMatch object
        :return:
        """
        # Create Widgets
        color_lbl = QLabel()
        checkbox = QCheckBox()
        more_btn = QToolButton()
        probability_lcd = QLCDNumber()

        # Color Label Settings
        color = self.colorWheel.next_color()
        color_lbl.setText('             ')
        color_lbl.setFrameShape(QFrame.Panel)
        color_lbl.setFrameShadow(QFrame.Raised)
        color_lbl.setStyleSheet("border-color: rgb(255, 255, 255); "
                                + "background-color: " + color + ";")

        # Check Box Settings
        font = QFont()
        font.setPixelSize(20)
        checkbox.setFont(font)
        checkbox.setText(match.name)
        checkbox.click()

        # Probability LCD Number
        #probability_lcd.setDigitCount(match.p)
        probability_lcd.setNumDigits(8)
        probability_lcd.display((match.p * 1000))
        probability_lcd.setSegmentStyle(QLCDNumber.Flat)
        probability_lcd.setFrameShape(QFrame.NoFrame)
        #probability_lcd.setFrameShadow(QFrame.Raised)
        probability_lcd.setStyleSheet("background-color: none; \
                                        border-color: none;\
                                        color: rgb(255, 255, 255);")
        # More Button (...) Settings
        more_btn.setText('...')
        more_btn.clicked.connect(lambda: self.more_info(match, color))


        # Add Widgets to Layout
        self.ui.gridLayout.addWidget(probability_lcd, self.size, 0)
        self.ui.gridLayout.addWidget(color_lbl, self.size, 1)
        self.ui.gridLayout.addWidget(checkbox, self.size, 2)
        self.ui.gridLayout.addWidget(more_btn, self.size, 3)
        self.ui.gridLayout.addWidget(more_btn, self.size, 4)

        # Add Data to elements array
        self.elements[(self.size, 0)] = match
        self.elements[(self.size, 1)] = color
        self.elements[(self.size, 2)] = checkbox
        self.elements[(self.size, 3)] = more_btn

        self.size += 1          # increase size of elements array
        self.selected.append(1) # increase # of selected elements

    def add_all(self, match_list):
        for match in match_list:
            self.add_row(match)

    def more_info(self, match, color):
        window = AssignmentWindow(match, color, self.experiment)
        window.exec_()
        #window.show()

    def get_selected_mids(self):
        mids = []

        for i in range(0, self.size):
            match = self.elements[i, 0]
            checkbox = self.elements[i, 2]
            mid = match.mid

            if checkbox.isChecked():
                mids.append(mid)

        return mids

    def get_selections(self):
        matches = []
        colors = []
        for i in range(0, self.size):
            match = self.elements[i, 0]
            color = self.elements[i, 1]
            checkbox = self.elements[i, 2]

            if checkbox.isChecked():
                matches.append(match)
                colors.append(color)

        return matches, colors

    def select_all(self):
        for i in range(0, self.size):
            checkbox = self.elements[i, 2]

            if checkbox.isChecked() is False:
                checkbox.click()

    def deselect_all(self):
        for i in range(0, self.size):
            checkbox = self.elements[i, 2]

            if checkbox.isChecked() is True:
                checkbox.click()

    def validate_selections(self):
        """
        Validates the Selected Molecules in experiment
        """
        selected_mids = self.get_selected_mids()

        for mid in selected_mids:
            self.experiment.validate_a_match(mid)


class GraphColorWheel:

    def __init__(self):
        self.color_wheel = None
        self.index = 0

    def import_color_wheel(self, file_path):

        with open(file_path) as f:
            self.color_wheel = f.read().splitlines()

    def next_color(self):
        self.index += 1
        return self.color_wheel[self.index-1]
