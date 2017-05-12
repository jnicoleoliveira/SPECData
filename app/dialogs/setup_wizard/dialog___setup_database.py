# Author: Jasmine Oliveira
# Date: 5/12/2017

from PyQt4.QtGui import *

from dialog___create_executable import CreateExecutable
from dialog___wizard_window import WizardWindow


class SetupDatabase(WizardWindow):
    def __init__(self):
        super(SetupDatabase, self).__init__(True)

        self.title.setText("Setup Database")
        self.__setup_center_layout()
        self.__setup_buttons()
        self.show()

    def __setup_buttons(self):
        self.rightbtn.setText("Cancel")
        self.leftbtn.setText("Next")
        self.leftbtn.clicked.connect(self.right_btn_action)
        self.rightbtn.clicked.connect(self.close)

    def __setup_center_layout(self):
        # Radio Buttons
        create_database_btn = QRadioButton()
        create_database_btn.setText("Create New Database")
        create_database_btn.setStyleSheet(self.body_font)
        import_database_btn = QRadioButton()
        import_database_btn.setText("Import a Database..")
        import_database_btn.setStyleSheet(self.body_font)

        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)

        # File Selection
        file_layout = QHBoxLayout()
        file_txt = QLineEdit()
        select_btn = QToolButton()
        select_btn.setText("...")
        file_layout.addSpacerItem(QSpacerItem(20, 20))
        file_layout.addWidget(file_txt)
        file_layout.addWidget(select_btn)

        # Import Layout
        import_layout = QVBoxLayout()
        import_layout.addWidget(import_database_btn)
        import_layout.addLayout(file_layout)
        import_layout.setSpacing(0)

        # Radio Button Full Layout
        layout = QVBoxLayout()
        layout.setSpacing(6)
        layout.addWidget(create_database_btn)
        layout.addLayout(import_layout)

        # Add Buttons to Cetner
        self.center_layout.addItem(spacer, 0, 0)
        self.center_layout.addLayout(layout, 1, 0)
        self.center_layout.addItem(spacer, 2, 0)

    def right_btn_action(self):
        self.close()
        window = CreateExecutable()
        window.show()
        window.exec_()


class SetupComplete(WizardWindow):
    def __init__(self):
        super(SetupComplete, self).__init__()

    def __setup_buttons(self):
        self.rightbtn.setText("Cancel")
        self.leftbtn.setText("Next")
        self.rightbtn.clicked.connect()
        self.leftbtn.clicked.connect()

        # def __setup_center_layout(self):
        #     layout =
        #
        # def right_btn_action(self):
