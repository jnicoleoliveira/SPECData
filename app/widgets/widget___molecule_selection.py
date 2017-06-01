# Author: Jasmine Oliveira
# Date 08/30/2016

import os, operator

from PyQt4.QtGui import *

from app.dialogs.dialog___assignment_window import AssignmentWindow
from app.dialogs.frames.experiment_view.frame___molecule_selection_widget import Ui_ScrollArea
from config import resources


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

        # Color Wheel
        self.colorWheel = GraphColorWheel()
        self.colorWheel.import_color_wheel(os.path.join(resources, 'graphing_colors'))

    def add_row(self, match, color=None):
        """
        Adds a Molecule Row to MoleculeSelection Widget, and list of elements.
        Row consists of the following widgets:
            color_lbl (color associated with molecule match)
            checkbox  (checkbox associated with selecting a molecule match for graphing)
            more_btn  (button associated with opening AssignmentWindow(mid)
            probability_lcd (QLCDNumber with probability of match)
        :param match: MoleculeMatch object
        :param color : If none, will automatically assign a color.
        :return:
        """

        # Create Widgets
        color_lbl = QLabel()
        checkbox = QCheckBox()
        more_btn = QToolButton()
        probability_lcd = QLCDNumber()

        # Color Label Settings
        if color is None:
            color = self.colorWheel.next_color()

        color_lbl.setText((' ') * 15)
        color_lbl.setFrameShape(QFrame.Panel)
        color_lbl.setFrameShadow(QFrame.Raised)
        color_lbl.setStyleSheet("border-color: rgb(255, 255, 255); "
                                + "background-color: " + color + ";")
        color_lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Check Box Settings
        if 10 < len(match.name) < 20:
            size = 18
        elif len(match.name) > 20:
            size = 10
        else:
            size = 20

        font = QFont()
        font.setPixelSize(size)
        checkbox.setFont(font)
        checkbox.setText(match.name)
        checkbox.click()

        # Probability LCD Number
        probability_lcd = QLabel()
        probability_lcd.setText(" " + str(match.p * 1000)[:4] + "  ")  # substring (of length 4)
        probability_lcd.setFont(QFont("monospace"))
        # probability_lcd.setDecMode()
        # probability_lcd.setDigitCount(4)
        # probability_lcd.display((match.p * 1000))
        # probability_lcd.setSegmentStyle(QLCDNumber.Flat)
        # probability_lcd.setFrameShape(QFrame.NoFrame)
        # #probability_lcd.setFrameShadow(QFrame.Raised)
        probability_lcd.setStyleSheet("background-color: none; \
                                        border-color: none;\
                                        color: rgb(255, 255, 255);")
        probability_lcd.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # More Button (...) Settings
        more_btn.setText('...')
        more_btn.clicked.connect(lambda: self.more_info(match, color))

        # Add Widgets to Layout
        widget = QHBoxLayout()
        widget.setSpacing(3)
        widget.addWidget(probability_lcd)
        widget.addWidget(color_lbl)
        widget.addWidget(checkbox)
        widget.addWidget(more_btn)
        self.ui.gridLayout.addLayout(widget, self.size, 0)

        # Add Data to elements array
        selection_row = SelectionRow(match, color, checkbox, more_btn, widget)
        self.elements[match.mid] = selection_row

        self.size += 1          # increase size of elements array
        #self.selected.append(1) # increase # of selected elements

    def add_all(self, match_list):
        for match in match_list:
            self.add_row(match)

    def remove_row(self, match):
        print "remove_row"

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QWidgetItem):
                # print "widget" + str(item)
                item.widget().close()
                # or
                # item.widget().setParent(None)
            elif isinstance(item, QSpacerItem):
                # no need to do extra stuff
                pass
            else:
                #print "layout " + str(item)
                self.clearLayout(item.layout())

            # remove the item from layout
            layout.removeItem(item)

    def remove_selections(self):

        matches = []
        colors = []
        mids = []
        elements_copy = self.elements.copy()

        for key, value in elements_copy.iteritems():
            match = value.match
            color = value.color
            checkbox = value.checkbox
            widget = value.widget

            if checkbox.isChecked():
                mids.append(match.mid)
                matches.append(match)
                colors.append(color)
                self.clear_layout(self.elements[key].widget)
                del self.elements[key]

        # print str(self.elements)

        return matches, colors

    def more_info(self, match, color):
        window = AssignmentWindow(match, color, self.experiment)
        window.exec_()
        #window.show()

    def get_selected_mids(self):
        mids = []

        for key, value in self.elements.iteritems():
            checkbox = value.checkbox
            if checkbox.isChecked():
                mids.append(key)

        return mids

    def get_selections(self):
        matches = []
        colors = []

        for key, value in self.elements.iteritems():
            match = value.match
            color = value.color
            checkbox = value.checkbox

            if checkbox.isChecked():
                matches.append(match)
                colors.append(color)

        return matches, colors

    def select_all(self):
        """
        'Clicks' all checkboxes that are not checked
        :return:
        """
        for key, value in self.elements.iteritems():
            checkbox = value.checkbox
            if checkbox.isChecked() is False:
                checkbox.click()

    def deselect_all(self):
        """
        'Clicks' all checkboxes that are checked
        :return:
        """
        for key, value in self.elements.iteritems():
            checkbox = value.checkbox
            if checkbox.isChecked() is True:
                checkbox.click()

    def add_rows(self, matches, colors):
        for i in range(0, len(matches)):
            self.add_row(matches[i], colors[i])

    def get_matches(self):
        """
        Return matches (sorted by match.p)
        """
        matches = []
        colors = []

        sorted = self.elements.values()
        sorted.sort(key=operator.attrgetter('match.p'), reverse=True)
        for value in sorted:
            matches.append(value.match)
            colors.append(value.color)
        return [matches, colors]

    def set_matches(self, matches, colors):
        self.select_all()
        self.remove_selections()
        self.add_rows(matches, colors)

    def get_elements(self):
        return self.elements

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


class SelectionRow:
    def __init__(self, match, color, checkbox, more_btn, widget):
        self.match = match
        self.color = color
        self.checkbox = checkbox
        self.more_btn = more_btn
        self.widget = widget

