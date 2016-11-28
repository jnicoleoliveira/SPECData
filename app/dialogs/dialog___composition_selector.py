# Author: Jasmine Oliveira
# Date: 11/21/2016

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from frames.frame___composition_selector import Ui_Dialog

from widget___periodic_table_scene import PeriodicTableSceneWidget
from frames.frame___element_viewbox_widget import Ui_Form as ViewBox_Ui
from frames.frame___selected_element_box import Ui_Form as SelectedBox_Ui


class CompositionSelector(QDialog):

    def __init__(self):
        super(CompositionSelector, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setLayout(self.ui.gridLayout)
        self.setWindowTitle('Composition Selector')
        self.setMouseTracking(True)
        self.__setup__()

    def __setup__(self):

        left_frame = self.ui.left_frame
        layout = QGridLayout()

        layout.addWidget(PeriodicTableSceneWidget())
        left_frame.setLayout(layout)

        right_frame = self.ui.right_frame

        layout = QVBoxLayout()

        x = QGridLayout()
        x.addWidget(ElementViewBoxWidget())

        box = QFrame()
        box.setLayout(x)
        box.setFrameStyle(QFrame.Plain)
        box.setStyleSheet("color: rgb(255, 255, 255);")
        box.setLineWidth(10)

        selection_box = QHBoxLayout()
        selection_box.addWidget(SelectedElementBox())
        selection_box.addWidget(SelectedElementBox())

        layout.addWidget(box)
        layout.addLayout(selection_box)
        right_frame.setLayout(layout)

class ElementViewBoxWidget(QWidget):
    def __init__(self):
        super(ElementViewBoxWidget, self).__init__()
        self.ui = ViewBox_Ui()
        self.ui.setupUi(self)



class SelectedElementBox(QWidget):

    def __init__(self):
        super(SelectedElementBox, self).__init__()
        self.ui = SelectedBox_Ui()
        self.ui.setupUi(self)
