# Author: Jasmine Oliveira
# Date 08/30/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from frames.frame___molecule_selection_widget import Ui_ScrollArea


class MoleculeSelectionWidget(QWidget):
    def __init__(self):
        super(MoleculeSelectionWidget, self).__init__()
        self.ui = Ui_ScrollArea()
        self.ui.setupUi(self)
        self.setLayout(self.ui.gridLayout)
        self.setWindowTitle('Matches')

        self.elements = {}
        self.size = 0
        self.selected = []

        self.show()
        self.colorWheel = GraphColorWheel()
        self.colorWheel.import_color_wheel('/home/joli/PycharmProjects/SPECData/app/dialogs/graphing_colors')

    def add_row(self, match):

        # Create Widgets
        color_lbl = QLabel()
        checkbox = QCheckBox()
        more_btn = QToolButton()

        color = self.colorWheel.next_color()
        color_lbl.setText('     ')
        color_lbl.setFrameShadow(QFrame.Sunken)
        color_lbl.setStyleSheet("border-color: rgb(255, 255, 255); "
                                + "background-color: " + color + ";")

        font = QFont()
        font.setPixelSize(20)
        checkbox.setFont(font)
        checkbox.setText(match.name)
        checkbox.click()
        #checkbox.setEnabled(True)
        checkbox.setSizeIncrement(2,2)
        more_btn.setText('...')
        more_btn.clicked.connect(lambda: self.more_info(match.mid))

        # Add Widgets to Layout
        self.ui.gridLayout.addWidget(color_lbl, self.size, 0)
        self.ui.gridLayout.addWidget(checkbox, self.size, 1)
        self.ui.gridLayout.addWidget(more_btn, self.size, 2)
        self.ui.gridLayout.addWidget(more_btn, self.size, 2)

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

    def more_info(self, mid):
        from ..events import display_error_message
        display_error_message("Window: " + mid, "Test","Test")
        print 'open window' + str(mid)

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

class GraphColorWheel():

    def __init__(self):
        self.color_wheel = None
        self.index = 0

    def import_color_wheel(self, file_path):

        with open(file_path) as f:
            self.color_wheel = f.read().splitlines()

    def next_color(self):
        self.index += 1
        return self.color_wheel[self.index-1]
