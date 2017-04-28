# Author: Jasmine Oliveira
# Date: 5/28/2017

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from images import LOGO_ICON


class WizardWindow(QDialog):
    def __init__(self):
        super(WizardWindow, self).__init__()
        self.resize(250, 250)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.show()
        self.setWindowTitle("SPECdata Setup")

        self.rightbtn = QPushButton()
        self.leftbtn = QPushButton()
        self.title = QLabel()
        self.center_layout = QGridLayout()

        self.__setup_ui__()
        self.show()

    def __setup_ui__(self, header=True):
        main_layout = QHBoxLayout()

        if header is True:
            # Create Header
            frame = QFrame()
            flayout = QVBoxLayout()
            flayout.addWidget(self.title)
            flayout.addSpacerItem(QSpacerItem(1, 1))
            icon = QLabel()
            icon.setPixmap(QPixmap(LOGO_ICON))
            flayout.addWidget(icon)
            frame.setLayout(flayout)
            main_layout.addWidget(frame)

        main_layout.addSpacerItem(QSpacerItem(1, 1))
        main_layout.addLayout(self.center_layout)
        main_layout.addSpacerItem(QSpacerItem(1, 1))

        frame = QFrame()
        flayout = QVBoxLayout()
        flayout.addSpacerItem(QSpacerItem(1, 1))
        flayout.addWidget(self.leftbtn)
        flayout.addWidget(self.rightbtn)
        frame.setLayout(flayout)

        main_layout.addWidget(frame)
        self.setLayout(main_layout)
