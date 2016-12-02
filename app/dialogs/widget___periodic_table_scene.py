# Author: Jasmine Oliveira
# Date: 11/21/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from frames.frame___periodic_table_scene import Ui_Form


class PeriodicTableSceneWidget(QWidget):

    def __init__(self):
        super(PeriodicTableSceneWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setMouseTracking(True)
        self.delete_widgets = []

        self.transfer_labels_to_buttons(self.ui.periodic_grid_1)
        self.transfer_labels_to_buttons(self.ui.periodic_grid_2)

    def transfer_labels_to_buttons(self, grid):
        count = grid.count()

        items = (grid.itemAt(i) for i in range(count))


        i = 0
        none_count = 0
        none_count = 0
        for w in items:
            if w.widget() is not None and not isinstance(w.widget(), QSpacerItem):
                print w.widget().objectName()
                print w.widget().text()
                r, c, cs, rs = grid.getItemPosition(i)
                self.set_next(grid, w.widget(), r, c)
                i += 1
                print i
                print "\n"
                #print count
            else:
                none_count += 1

        print none_count
        self.clear_remove_later(grid)

    def set_next(self, grid, button, x, y):


        # Get Button Attributes
        #x = button.x()
        #y = button.y()
        print str(x) + " " + str(y)
        #print button.text()
        text = button.text()
        stylesheet = button.styleSheet() + " border: 1px solid white; "
        size_policy = button.sizePolicy()

        # Create New Button
        new_button = HoverButton()
        new_button.setText(text)
        new_button.setSizePolicy(size_policy)
        new_button.setStyleSheet(stylesheet)
        #print stylesheet
        new_button.setMinimumSize(40, 40)
        new_button.setMaximumSize(40, 40)
        new_button.setAutoRaise(True)

        self.delete_widgets.append(button)
        grid.addWidget(new_button, x, y)

    def clear_remove_later(self, grid):
        for r in self.delete_widgets:
            grid.removeWidget(r)
            r.deleteLater()
            r.close()
            del r

        self.delete_widgets = []

def hoverable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()

        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.HoverMove:
                    if obj.rect().contains(event.pos()):
                        print "HOVER"
                        return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked

class HoverLabel(QLabel):
    def __init__(self, parent=None):
        super(HoverLabel, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        print("Enter")
        self.setStyleSheet("background-color:#45b545;")

    def leaveEvent(self,event):
        self.setStyleSheet("background-color:yellow;")
        print("Leave")

class HoverButton(QToolButton):

    def __init__(self, parent=None):
        super(HoverButton, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        print("Enter")
        self.setStyleSheet("background-color:#45b545;")

    def leaveEvent(self,event):
        self.setStyleSheet("background-color:yellow;")
        print("Leave")