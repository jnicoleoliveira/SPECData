# Author: Jasmine Oliveira
# Date: 11/21/2016

from PyQt4.QtGui import *

from app.dialogs.frames.composition_selector.frame___composition_selector import Ui_Dialog
from app.dialogs.frames.composition_selector.frame___element_viewbox_widget import Ui_Form as ViewBox_Ui
from app.dialogs.frames.composition_selector.frame___selected_element_box import Ui_Form as SelectedBox_Ui
from app.widgets.widget___periodic_table_scene import PeriodicTableSceneWidget
from ..events import display_error_message


class CompositionSelector(QDialog):

    def __init__(self, composition_lbl):
        super(CompositionSelector, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setLayout(self.ui.gridLayout)
        self.setWindowTitle('Composition Selector')
        self.setMouseTracking(True)
        self.composition_lbl = composition_lbl

        ''' Widgets '''
        self.element_view_box_widget = ElementViewBoxWidget()
        self.periodic_table_widget = PeriodicTableSceneWidget(self.element_view_box_widget)
        self.selected_elements_grid = QGridLayout()
        self.selected_elements = []
        self.grid_row = 0
        self.grid_column = 0
        self.__setup__()

    def __setup__(self):
        """
        Sets up the layout of the dialog
        """

        ''' Get Frames '''
        left_frame = self.ui.left_frame
        right_frame = self.ui.right_frame
        view_box_frame = self.ui.view_box_frame

        ''' Setup Left Frame '''
        layout = QGridLayout()
        layout.addWidget(self.periodic_table_widget)
        left_frame.setLayout(layout)

        ''' Set View Box Frame '''
        layout = QGridLayout()
        layout.addWidget(self.element_view_box_widget)
        view_box_frame.setLayout(layout)

        ''' Setup Right Frame '''
        right_frame.setLayout(self.selected_elements_grid)

        ''' Connect Element Buttons '''
        element_buttons = self.periodic_table_widget.element_buttons
        self.connect_element_buttons(element_buttons)

        ''' Connect Other Buttons '''
        self.ui.accept_btn.clicked.connect(self.accept_selections)
        self.ui.cancel_btn.clicked.connect(self.close_self)

    def connect_element_buttons(self, buttons):

        for b in buttons:
            sctuple = (b.symbol, b.og_color)
            b.clicked.connect(lambda state, x=sctuple: self.add_selected_element(x))

    def add_selected_element(self, sctuple):

        symbol = sctuple[0]
        color = sctuple[1]
        e = self.get_selected_element(symbol)

        if e is not None:
            e.increase_counter()
        else:

            # Create new selected element object
            widget = SelectedElementBox(symbol, color, \
                                        lambda state, x=symbol: self.remove_selected_element(x))
            widget.increase_counter()
            # Add to selected elements list #
            self.selected_elements.append(widget)

            if self.grid_row == 3:
                self.grid_row = 0
                self.grid_column += 1

            self.selected_elements_grid.addWidget(widget, self.grid_column, self.grid_row)

            self.grid_row += 1

    def get_selected_element(self, symbol):
        for e in self.selected_elements:
            if e.symbol == symbol:
                return e

        return None

    def remove_selected_element(self, symbol):

        for e in self.selected_elements:
            if e.symbol == symbol:
                self.selected_elements_grid.removeWidget(e)
                e.deleteLater()
                e.close()
                self.selected_elements.remove(e)
                del e
                return

    def close_self(self):
        """
        Close current window.
        """
        self.close()

    def accept_selections(self):
        """
        Action when a user decides to accept their element selections
            -- Displays error message and returns if no elements selected
            -- (--deprecated)Prompts user to confirm selections
        """
        # Throw error message if none are selected
        if len(self.selected_elements) is 0:
            display_error_message("No elements have been selected.",\
                                  "Please add at least (1) element to continue.",\
                                  "To add an element, click an element on the periodic"
                                  " table. To add more than one, simply click again.")
            return

        # Prompt for selection confirmation
        composition_string = self.get_selected_string()
        # display_string = "You've selected the following elements:\n\n"\
        #                  + composition_string + "\n\n Do you accept?"
        # reply = display_question_message(display_string, "Confirm")
        #
        # if reply is False:
        #     return

        self.composition_lbl.setText(composition_string)
        self.close_self()

    def get_selected_string(self):

        string = ""
        for e in self.selected_elements:
            string += e.symbol + "(" + str(e.get_counter_value()) + ") "

        return string


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

    def __init__(self, symbol, color, function_connection):
        super(SelectedElementBox, self).__init__()
        self.ui = SelectedBox_Ui()
        self.ui.setupUi(self)
        self.symbol = symbol
        self.ui.blank_lbl.setStyleSheet("background-color: " + color + ";")
        self.ui.symbol_lbl.setText(symbol)
        self.ui.close_btn.setStyleSheet("background-color: " + color + ";")
        self.ui.symbol_lbl.setStyleSheet("background-color: " + color + ";")
        self.ui.close_btn.clicked.connect(function_connection)

    def increase_counter(self):
        counter = self.ui.spinBox
        value = counter.value()
        counter.setValue(value + 1)

    def get_counter_value(self):
        return self.ui.spinBox.value()
