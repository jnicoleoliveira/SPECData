# Author: Jasmine Oliveira
# Date: 5/12/2017

from PyQt4.QtGui import *

from dialog___setup_database import SetupDatabase
from dialog___wizard_window import WizardWindow


class CheckRequirements(WizardWindow):
    def __init__(self):
        super(CheckRequirements, self).__init__(True)

        self.text_browser = QTextBrowser()

        self.title.setText("Create Executable")
        self.__setup_center_layout()
        self.__setup_buttons()
        self.show()
        self.check_requirements()

    def __setup_buttons(self):
        self.rightbtn.setText("Cancel")
        self.leftbtn.setText("Next")
        self.leftbtn.clicked.connect(self.right_btn_action)
        self.rightbtn.clicked.connect(self.close)

    def __setup_center_layout(self):

        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)

        description = QLabel("Checking requirements...")
        description.setStyleSheet(self.body_font)

        # View
        text_browser = self.text_browser
        text_browser.setStyleSheet("font:monospace;")
        text_browser.setWordWrapMode(QTextOption.NoWrap)
        text_browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add Components to Center Layout
        self.center_layout.addItem(spacer, 0, 0)
        self.center_layout.addWidget(description, 1, 0)
        self.center_layout.addWidget(text_browser, 2, 0)
        self.center_layout.addItem(spacer, 3, 0)

    def check_requirements(self):
        missing_imports = []
        import os
        import config
        path = os.path.join(config.PROGRAM_DIR, "init", "bin", "import_list.txt")
        imports = open(path).readlines()
        buff = len(max(imports, key=len))
        print buff
        for name in imports:
            name = name.strip()
            try:
                exec ("import " + name)
                line = name + ("." * (buff - len(name))) + " [OK]"
                print line
            except ImportError:
                missing_imports.append(name)
                line = name + "[Failed]"

            self.text_browser.append(line)

        success = len(imports) - len(missing_imports)
        failed = len(missing_imports)
        self.text_browser.append("Passed: " + str(success) + " Failed: " + str(failed))

    def right_btn_action(self):
        self.close()
        window = SetupDatabase()
        window.show()
        window.exec_()
