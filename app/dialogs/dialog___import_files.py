# Author: Jasmine Oliveira
# Date: 09/15/2016

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from app.dialogs.frames.manage_database.frame___import_files import Ui_Dialog


class ImportFiles(QDialog):
    """
        Select multiple files to be imported.
        Loads file paths into a list.
            UI:          import_files.ui
            Dialog:      frame___import_files.py
            Next Dialog: dialog___import_files_verification.py
            Back Dialog: dialog___main_menu.py
    """
    def __init__(self):
        super(ImportFiles, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Import Files")
        self.resize(1025, 750)

        self.file_paths = None

        # Start
        self.__start_up__()

    def __start_up__(self):
        self.open_file_dialog()                 # First Open File Dialog
        self.populate_list_with_file_paths()    # Populate listwidget with paths
        self.connect_buttons()                  # Connect Buttons to functions

    def add(self):
        self.open_file_dialog()
        self.populate_list_with_file_paths()

    def cancel(self):
        """
        Close current window, and return to main menu
        """
        self.close()
        from dialog___main_menu import MainMenu
        window = MainMenu()
        window.exec_()

    def connect_buttons(self):
        """
        Connect dialog buttons to associated function
        """
        # Get Buttons
        add_btn = self.ui.add_btn
        remove_btn = self.ui.remove_btn
        accept_btn = self.ui.accept_btn
        cancel_btn = self.ui.cancel_btn

        # Connect to functions
        add_btn.clicked.connect(self.add)
        remove_btn.clicked.connect(self.remove)
        cancel_btn.clicked.connect(self.cancel)
        accept_btn.clicked.connect(self.verify_import_list)

    def verify_import_list(self):
        """
        Iterates through the file paths, and opens
        an associated ImportFileVerification Dialog to
        verify info, and accept user input for entry data
         """
        from dialog___import_file_verification import ImportFileVerification

        not_accepted = []
        i = 0
        total = len(self.file_paths)
        for f in self.file_paths:
            window = ImportFileVerification(f, i, total)
            window.exec_()
            if not window.accepted:
                not_accepted.append(f)
            i += 1

        # Clear list widget
        self.ui.listWidget.clear()

        # Populate with leftover
        for path in not_accepted:
            path_item = QListWidgetItem(str(path))
            self.ui.listWidget.addItem(QListWidgetItem(path_item))

    def open_file_dialog(self):
        """
        Opens File dialog in parent of parent directory.
        Appends file_paths selected by user, to self.file_paths
        """
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        w = QWidget()
        w.resize(320, 240)
        w.setWindowTitle("Select Files")

        if self.file_paths is not None:
            ## Get the union of this set and the previous set
            self.file_paths = list(set(self.file_paths) |
                               set(QFileDialog.getOpenFileNames(w, 'Open File', parent_dir)))
        else:
            self.file_paths = (QFileDialog.getOpenFileNames(w, 'Open File', parent_dir))

    def populate_list_with_file_paths(self):
        """
        Populates list widget with file path strings in self.file_paths
        """
        self.ui.listWidget.clear()

        for path in self.file_paths:
            path_item = QListWidgetItem(str(path))
            self.ui.listWidget.addItem(QListWidgetItem(path_item))

    def remove(self):
        """
        Removes selected items in the list widget
        """
        items = self.ui.listWidget.selectedItems()
        for item in items:
            self.ui.listWidget.takeItem(self.ui.listWidget.row(item))
            self.file_paths.remove(item.text())
