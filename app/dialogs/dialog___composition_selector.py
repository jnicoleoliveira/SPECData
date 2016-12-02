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
        self.periodic_table_widget = None
        self.__setup__()

    def __setup__(self):

        left_frame = self.ui.left_frame
        layout = QGridLayout()

        ''' Create Widgets '''
        self.element_view_box_widget = ElementViewBoxWidget()
        self.periodic_table_widget = PeriodicTableSceneWidget(self.element_view_box_widget)

        ''' Add Widgets to Layout '''
        layout.addWidget(self.periodic_table_widget)
        left_frame.setLayout(layout)

        right_frame = self.ui.right_frame

        layout = QVBoxLayout()

        x = QGridLayout()

        x.addWidget(self.element_view_box_widget)

        box = QFrame()
        box.setLayout(x)
        box.setFrameStyle(QFrame.Plain)
        box.setStyleSheet("color: rgb(255, 255, 255);")
        box.setLineWidth(10)

        selection_box = QGridLayout()
        selection_box.addWidget(SelectedElementBox(), 0, 0)
        selection_box.addWidget(SelectedElementBox(), 0, 1)
        selection_box.addWidget(SelectedElementBox(), 0, 2)
        selection_box.addWidget(SelectedElementBox(), 1, 0)
        selection_box.addWidget(SelectedElementBox(), 1, 1)
        selection_box.addWidget(SelectedElementBox(), 1, 2)


        layout.addWidget(box)
        layout.addSpacerItem(QSpacerItem(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        layout.addLayout(selection_box)
        right_frame.setLayout(layout)


        ''' Connect Element Buttons '''
        element_buttons = self.periodic_table_widget.element_buttons


class ElementViewBoxWidget(QWidget):
    def __init__(self):
        super(ElementViewBoxWidget, self).__init__()
        self.ui = ViewBox_Ui()
        self.ui.setupUi(self)

    def setLabelText(self, symbol, name, mass, atomic_number, boiling):
        self.ui.symbol_lbl.setText(str(symbol))
        self.ui.name_lbl.setText(str(name))
        self.ui.atomic_mass_lbl.setText(str(mass))
        self.ui.atomic_number_lbl.setText(str(atomic_number))
        self.ui.boiling_lbl.setText(str(boiling))

class SelectedElementBox(QWidget):

    def __init__(self):
        super(SelectedElementBox, self).__init__()
        self.ui = SelectedBox_Ui()
        self.ui.setupUi(self)
