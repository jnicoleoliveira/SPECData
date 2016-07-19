from PyQt4.QtCore import *
from PyQt4.QtGui import *

from events import clickable

from frames.frame___import_finished import Ui_importfinished_frame  # Import Frame
from dialog___main_window import MainWindow  # Next Window (Return to Menu)

class ImportFinished(QDialog):
    def __init__(self, log_message):
        super(ImportFinished, self).__init__()
        self.ui= Ui_importfinished_frame()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.log_message = log_message

        self.connect_buttons()  # Connect buttons to appropriate functions
        self.display_log_message()  # Display Log Message to Screen

    def connect_buttons(self):
        # Get buttons/labels
        return_lbl = self.ui.return_lbl

        # Set Buttons
        clickable(return_lbl).connect(self.return_to_main_menu)

    def display_log_message(self):
        """
        Displays Log Message to Screen
        :return:
        """
        log_list = self.ui.log_list
        if self.log_message is not None:
            for line in self.log_message:
                item = QListWidgetItem(line)
                log_list.addItem(item)

    def return_to_main_menu(self):
            """
            Closes current window and returns to MainWindow
            :return:
            """
            self.close()
            window = MainWindow()
            window.show()
