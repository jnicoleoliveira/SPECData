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
        #QObject.connect(self.ui.Li, SIGNAL('hovered()'), self.label_EnterEvent)
        #self.ui.Li.setMouseTracking(True)
        #hoverable(self.ui.Li)
        self.ui.pushButton.setMouseTracking(True)
        self.ui.pushButton = HoverButton()
    def label_EnterEvent(self):
        print("Enter")
        self.setStyleSheet("background-color:#45b545;")


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

class HoverButton(QPushButton):
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        print 'Mouse moved!'