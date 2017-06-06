# Author: Jasmine Oliveira
# Date: 5/12/2017

from PyQt4.QtGui import *

from dialog___setup_database import SetupDatabase
from dialog___wizard_window import WizardWindow
from app.events import display_question_message

class CheckRequirements(WizardWindow):
    def __init__(self):
        super(CheckRequirements, self).__init__(True)

        self.text_browser = QTextBrowser()

        self.title.setText("Checking Requirements")
        self.__setup_center_layout()
        self.__setup_buttons()
        self.show()

        self.missing = self.check_requirements()

    def run(self):

        missing = self.check_requirements()

        if len(missing) == 0:
            return  # All Requirments met

        # Otherwise... throw warning.
        display_question_message("Your environment does not satisfy the necessary"
                                 " requirements. It is recrommended that these requirementss are"
                                 " resolved before continuing. Are you sure you want to continue?",
                                 "Requirements Unfulfilled")

    def __setup_buttons(self):
        self.rightbtn.setText("Cancel")
        self.leftbtn.setText("Next")
        self.leftbtn.clicked.connect(self.left_btn_action)
        self.rightbtn.clicked.connect(self.close)

    def __setup_center_layout(self):

        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)

        description = QLabel("Checking requirements...")
        description.setStyleSheet(self.body_font)

        # View
        text_browser = self.text_browser
        text_browser.setStyleSheet("font-family:monospace;")
        text_browser.setWordWrapMode(QTextOption.NoWrap)
        text_browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add Components to Center Layout
        self.center_layout.addItem(spacer, 0, 0)
        self.center_layout.addWidget(description, 1, 0)
        self.center_layout.addWidget(text_browser, 2, 0)
        self.center_layout.addItem(spacer, 3, 0)

    def check_requirements(self):
        """
        Tests Importing all required imports in import_list.txt and prints results to text_browser
        Returns list of strings of missing imports names
        """
        missing_imports = []
        import os
        import config
        path = os.path.join(config.PROGRAM_DIR, "init", "bin", "import_list.txt")
        imports = open(path).readlines()
        buff = len(max(imports, key=len))

        self.text_browser.append("Checking installed packages: ")
        for name in imports:
            name = name.strip()
            try:
                exec ("import " + name)
                line = " " + name + (" " * (buff - len(name))) + " [OK]"
            except ImportError:
                missing_imports.append(name)
                line = " " + name + (" " * (buff - len(name))) + "[Failed]"

            self.text_browser.append(line)

        success = len(imports) - len(missing_imports)
        failed = len(missing_imports)
        self.text_browser.append("\nPassed: " + str(success) + " Failed: " + str(failed))

        return missing_imports

    def right_btn_action(self):
        self.close()
        window = SetupDatabase()
        window.show()
        window.exec_()

    def left_btn_action(self):
        if len(self.missing) == 0:
            self.open_next()

        # Otherwise... throw warning.
        answer = display_question_message("Your environment does not satisfy the necessary"
                                 " requirements! It is recrommended that these requirements are"
                                 " resolved before continuing.\nAre you sure you want to continue?",
                                 "Requirements Unfulfilled")

        if answer is True:
            self.open_next()
        else:
            self.close()

    def open_next(self):
        self.close()
        window = SetupDatabase()
        window.show()
        window.exec_()
