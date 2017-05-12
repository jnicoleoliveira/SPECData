# Author: Jasmine Oliveira
# Date: 5/12/2017

from PyQt4.QtGui import *

from dialog___complete import CompletingWindow
from dialog___wizard_window import WizardWindow


class CreateExecutable(WizardWindow):
    def __init__(self):
        super(CreateExecutable, self).__init__(True)

        self.title.setText("Create Executable")
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
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)

        description = QLabel("Choose the location for your executable:")
        description.setStyleSheet(self.body_font)

        # File Selection
        file_layout = QHBoxLayout()
        file_txt = QLineEdit()
        select_btn = QToolButton()
        select_btn.setText("...")
        file_layout.addWidget(file_txt)
        file_layout.addWidget(select_btn)

        # Import Layout
        import_layout = QVBoxLayout()
        import_layout.addWidget(description)
        import_layout.addLayout(file_layout)
        import_layout.setSpacing(10)

        self.center_layout.addItem(spacer, 0, 0)
        self.center_layout.addLayout(import_layout, 1, 0)
        self.center_layout.addItem(spacer, 2, 0)

    def right_btn_action(self):
        self.close()
        window = CompletingWindow()
        window.show()
        window.exec_()
