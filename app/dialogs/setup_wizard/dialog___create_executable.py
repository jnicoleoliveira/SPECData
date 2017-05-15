# Author: Jasmine Oliveira
# Date: 5/12/2017

from PyQt4.QtGui import *

import config
import os
import sys
from app.error import path_exists
from app.events import save_as_file, display_error_message
from dialog___complete import CompletingWindow
from dialog___wizard_window import WizardWindow
from images import LOGO_ICON


class CreateExecutable(WizardWindow):
    def __init__(self):
        super(CreateExecutable, self).__init__(True)
        self.select_btn = QToolButton()
        self.file_txt = QLineEdit()
        self.file_path = None

        self.title.setText("Create Executable")
        self.__setup_center_layout()
        self.__setup_buttons()
        self.show()

    def __setup_buttons(self):
        self.rightbtn.setText("Cancel")
        self.leftbtn.setText("Next")
        self.leftbtn.clicked.connect(self.next_btn_clicked)
        self.rightbtn.clicked.connect(self.close)
        self.select_btn.clicked.connect((lambda x: save_as_file(self.file_txt, ".txt")))

    def __setup_center_layout(self):
        # Radio Buttons
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)

        description = QLabel("Choose the location for your executable:")
        description.setStyleSheet(self.body_font)
        description.setContentsMargins(0, 15, 0, 0)

        # File Selection
        file_layout = QHBoxLayout()
        file_txt = QLineEdit()
        self.select_btn.setText("...")
        file_layout.addWidget(file_txt)
        file_layout.addWidget(self.select_btn)

        # Import Layout
        import_layout = QVBoxLayout()
        import_layout.addWidget(description)
        import_layout.addLayout(file_layout)
        import_layout.setSpacing(10)

        # self.center_layout.addItem(spacer, 0, 0)
        self.center_layout.addLayout(import_layout, 1, 0)
        self.center_layout.addItem(spacer, 2, 0)

    def open_next_window(self):
        self.close()
        window = CompletingWindow()
        window.show()
        window.exec_()

    def next_btn_clicked(self):
        self.file_path = self.file_txt.text()

        if path_exists(self.file_path):
            self.create_linux_executable()
            self.open_next_window()
        else:
            display_error_message("Invalid Path!", "The path location you chose is invalid.",
                                  "Please choose an existing path")

    def create_linux_executable(self, dest):
        """

        :param dest:
        :return:
        """

        string = ""

        app_path = os.path.join(config.PROGRAM_DIR, "app.py")
        interpreter_path = str(sys.executable)
        work_path = config.PROGRAM_DIR
        icon_path = LOGO_ICON
        startupnotify = "true"
        version = "1.0"

        string += "[Desktop Entry]" \
                  "Version={version}" \
                  "Name=SPECdata" \
                  "Exec={interpreter_path} {app_path}" \
                  "Type=Application" \
                  "Path={work_path}" \
                  "Icon={icon_path}" \
                  "Categories=Utility;Application;" \
                  "StartupNotify=true" \
            .format(version=version, interpreter_path=interpreter_path,
                    app_path=app_path, icon_path=icon_path,
                    work_path=work_path)

        file = open(dest, 'w')
        file.write(string)
        file.close()

        return dest
