# Author: Jasmine Oliveira
# Date: 11/21/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from frames.frame___periodic_table_scene import Ui_Form
from periodic import element

class PeriodicTableSceneWidget(QWidget):

    def __init__(self, view_box):
        super(PeriodicTableSceneWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setMouseTracking(True)
        self.delete_widgets = []
        self.element_buttons = []
        self.view_box = view_box

        self.transfer_labels_to_buttons(self.ui.periodic_grid_1)
        self.transfer_labels_to_buttons(self.ui.periodic_grid_2)

    def transfer_labels_to_buttons(self, grid):
        count = grid.count()
        items = (grid.itemAt(i) for i in range(count))

        i = 0
        for w in items:
            if w.widget() is not None and not isinstance(w.widget(), QSpacerItem):
                r, c, cs, rs = grid.getItemPosition(i)
                self.set_next(grid, w.widget(), r, c)
                i += 1

        self.clear_remove_later(grid)

    def set_next(self, grid, button, x, y):

        # Get Button Attributes
        text = button.text()
        stylesheet = button.styleSheet()
        size_policy = button.sizePolicy()

        # Create New Button
        new_button = HoverButton(self.view_box, stylesheet)
        new_button.setText(text)
        new_button.setSizePolicy(size_policy)
        new_button.setStyleSheet(stylesheet + " border: 1px solid white; ")
        new_button.setMinimumSize(40, 40)
        new_button.setMaximumSize(40, 40)
        new_button.setAutoRaise(True)
        new_button.get_colors()
        new_button.get_data()

        # add old widget do delete later widgets
        self.delete_widgets.append(button)

        # add new widget in its place
        grid.addWidget(new_button, x, y)
        self.element_buttons.append(new_button)

    def clear_remove_later(self, grid):
        for r in self.delete_widgets:
            grid.removeWidget(r)
            r.deleteLater()
            r.close()
            del r

        self.delete_widgets = []


class HoverButton(QToolButton):

    def __init__(self, view_box, original_stylesheet, parent=None):
        super(HoverButton, self).__init__(parent)
        self.setMouseTracking(True)

        ''' Output Information '''
        self.view_box = view_box

        ''' Style Sheet Information '''
        self.og_color = None
        self.original_style_sheet = original_stylesheet + " border: 1px solid white; "
        self.darker_style_sheet = None
        self.setStyleSheet(self.original_style_sheet)

        ''' Element Information '''
        self.mass = ""
        self.boiling = ""
        self.name = ""
        self.symbol = ""
        self.name = ""
        self.atomic_number = ""

    def get_colors(self):
        og_color = self.palette().color(QPalette.Background)
        og_color = og_color.name()
        self.og_color = og_color
        darker = QColor(og_color + "").darker()
        self.darker_style_sheet = "background-color: " + darker.name() + "; border: 1px solid white; "

    def get_data(self):
        self.symbol = str(self.text())
        e = element(self.symbol)

        if e is None:
            n = {"Cn":112, "Uut": 113, "Fl" : 114, "Uup": 115, "Lv":116, "Uus":117, "Uuo":118 }

            if self.symbol in n:
                e = element(n[self.symbol])

            if e is None:
                print "Not Found: " + self.symbol
                return

        self.mass = e.mass
        self.name = e.name
        self.atomic_number = e.atomic



    def enterEvent(self,event):
        self.setStyleSheet(self.darker_style_sheet)
        print self.symbol
        self.view_box.setLabelText(self.symbol, self.name, self.mass, self.atomic_number, self.boiling)
        self.view_box.setStyleSheet("background-color: " + str(self.og_color) + ";")

    def leaveEvent(self,event):
        self.setStyleSheet(self.original_style_sheet)
