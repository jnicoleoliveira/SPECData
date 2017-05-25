# Author: Jasmine Oliveira
# Date: 5/12/2017

import os
import sys

from PyQt4.QtGui import *

import config
from app.events import save_as_file, display_error_message, display_informative_message
from dialog___complete import CompletingWindow
from dialog___wizard_window import WizardWindow
from images import LOGO_ICON, LOGO_ICON_WIN


class CreateExecutable(WizardWindow):
    def __init__(self):
        super(CreateExecutable, self).__init__(True)
        self.select_btn = QToolButton()
        self.file_txt = QLineEdit()
        self.file_path = None
        self.executable_ext = None  # ".lnk" #".desktop"
        self.system = None

        self.title.setText("Create Executable")
        self.__setup_center_layout()
        self.__setup_os()
        self.__setup_buttons()
        self.show()

    def __setup_os(self):
        import platform
        self.system = platform.system()
        import os

        if self.system == "Windows":
            self.executable_ext = ".lnk"
        elif self.system == "Linux":
            self.executable_ext = ".desktop"
            home = os.path.expanduser("~")
            # print home
            self.file_txt.setText(home + "/.local/share/applications/specdata.desktop")
        elif self.system == "Mac OS X" or self.system == "Darwin":
            self.executable_ext = ".command"
            self.file_txt.setText("/Applications/specdata.command")
        else:
            display_informative_message("The OS you are using: \n  "
                                        + str(self.system) +
                                        "\nis not currently supported for this feature. \n\n"
                                        "For questions, or to request to add this feature, "
                                        "please report this in the Issues Page on Github: \n"
                                        "  https://github.com/jnicoleoliveira/SPECData/issues")
            self.open_next_window()

    def __setup_buttons(self):
        self.rightbtn.setText("Cancel")
        self.leftbtn.setText("Next")
        self.leftbtn.clicked.connect(self.next_btn_clicked)
        self.rightbtn.clicked.connect(self.close)
        self.select_btn.clicked.connect((lambda x: save_as_file(self.file_txt, self.executable_ext)))

    def __setup_center_layout(self):
        # Radio Buttons
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)

        description = QLabel("Choose the location for your executable:")
        description.setStyleSheet(self.body_font)
        description.setContentsMargins(0, 15, 0, 0)

        # File Selection
        file_layout = QHBoxLayout()
        self.select_btn.setText("...")
        file_layout.addWidget(self.file_txt)
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
        """

        :return:
        """
        self.file_path = self.file_txt.text()

        if self.file_path == None or self.file_path == "":
            display_error_message("No path was chosen!", "No file path was chosen.",
                                  "Please choose an existing path!")
            return

        print "OS=" + str(self.system)

        try:
            self.create_executable()
        except IOError:
            # Test for spaces...
            self.file_path = self.file_path.replace(" ", "\\ ")

            try:
                self.create_executable()
            except IOError:
                display_error_message("Invalid Path!", "The path location you chose is invalid.",
                                      "Please choose an existing path")

    def create_executable(self):
        try:
            if self.system == "Windows":
                self.create_windows_executable(str(self.file_path))
            elif self.system == "Linux":
                self.create_linux_executable(str(self.file_path))
            elif self.system == "Mac OS X" or self.system == "Darwin":
                self.create_osx_executable(str(self.file_path))
            else:
                display_informative_message("The OS you are using: \n     "
                                            + str(self.system) + "  " + str(self.system.platform.release()) +
                                            "\n is not currently supported for this feature. \n\n "
                                            "For questions, or to request to add this feature, "
                                            "please report this in the Issues Page on Github: \n"
                                            "\t https://github.com/jnicoleoliveira/SPECData/issues")

            self.open_next_window()
        except IOError:
            print "IO ERROR"
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

        # Replace spaces
        app_path = app_path.replace(" ", "\\ ")
        interpreter_path = interpreter_path.replace(" ", "\\ ")

        work_path = config.PROGRAM_DIR
        icon_path = LOGO_ICON
        startupnotify = "true"
        version = "1.0"

        string += "[Desktop Entry]\n" \
                  "Version={version}\n" \
                  "Name=SPECdata\n" \
                  "Exec={interpreter_path} {app_path}\n" \
                  "Type=Application\n" \
                  "Path={work_path}\n" \
                  "Icon={icon_path}\n" \
                  "Categories=Utility;Application;\n" \
                  "StartupNotify=true" \
            .format(version=version, interpreter_path=interpreter_path,
                    app_path=app_path, icon_path=icon_path,
                    work_path=work_path)

        file = open(dest, 'w')
        file.write(string)
        file.close()

        ### Add Executable permissions
        import stat
        st = os.stat(dest)
        os.chmod(dest, st.st_mode | stat.S_IEXEC)

        return dest

    def create_windows_executable(self, dest):
        from win32com.client import Dispatch

        dest = str(dest)
        app_path = os.path.join(config.PROGRAM_DIR, "app.py")
        interpreter_path = str(sys.executable)
        work_path = config.PROGRAM_DIR
        target = interpreter_path + " " + app_path
        icon_path = LOGO_ICON_WIN

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(dest)
        shortcut.TargetPath = interpreter_path
        shortcut.Arguments = ' ' + app_path
        shortcut.WorkingDirectory = work_path
        shortcut.IconLocation = icon_path
        shortcut.Save()

        return dest

    def create_osx_executable(self, dest):

        # Create File
        os.system("touch " + dest)
        os.system("chmod +x " + dest)

        # Get Paths
        app_path = os.path.join(config.PROGRAM_DIR, "app.py")
        interpreter_path = str(sys.executable)

        # Replace spaces
        app_path = app_path.replace(" ", "\\ ")
        interpreter_path = interpreter_path.replace(" ", "\\ ")

        # Write text of executable
        string = "#!/bin/bash \n#SPECdata Launch\n" + \
                 interpreter_path + " " + app_path
        file = open(dest, 'w')
        file.write(string)

        return dest
