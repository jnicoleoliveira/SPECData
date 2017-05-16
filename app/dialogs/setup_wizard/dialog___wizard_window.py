# Author: Jasmine Oliveira
# Date: 4/28/2017

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from images import LOGO_ICON, WELCOME_RECT


class WizardWindow(QDialog):
    def __init__(self, header=True):
        super(WizardWindow, self).__init__()
        self.resize(600, 500)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.show()
        self.setWindowTitle("SPECdata Setup")

        ''' Widgets '''
        self.rightbtn = QPushButton()
        self.leftbtn = QPushButton()
        self.title = QLabel()
        self.center_layout = QGridLayout()

        ''' Font'''
        self.body_font = "font: serif;"
        self.header_font = "font:22px, bold;"
        self.title_font = "font:15px, bold"

        self.__setup_ui__(header)

    def __setup_ui__(self, header=True):
        main_layout = QVBoxLayout()
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Fixed)

        ''' Create Header'''
        if header is True:
            # Create Header Frame
            frame = QFrame()
            frame.setFrameStyle(QFrame.StyledPanel)
            frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            # Setup Content Widgets
            flayout = QHBoxLayout()
            self.title.setStyleSheet(self.header_font)
            icon = QLabel()
            icon.setPixmap(QPixmap(LOGO_ICON).scaledToWidth(50))

            # Setup layout
            flayout.addWidget(self.title)
            flayout.addSpacerItem(spacer)
            flayout.addWidget(icon)

            # Set frame and add to main layout
            frame.setLayout(flayout)
            main_layout.addWidget(frame)
            side_photo = QLabel()
            side_photo.hide()
        else:

            side_photo = QLabel()
            side_photo.setPixmap(QPixmap(WELCOME_RECT).scaled(250,500))
            side_photo.setStyleSheet("background:#008080")
            side_photo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            side_photo.setFrameStyle(QFrame.StyledPanel)

            side_photo.setFixedWidth(200)
            side_photo.setMaximumSize(250, 500)

        main_frame = QFrame()
        main_frame.setFrameStyle(QFrame.StyledPanel)
        main_frame.setLayout(self.center_layout)

        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        flayout = QHBoxLayout()
        flayout.addSpacerItem(spacer)
        flayout.addWidget(self.leftbtn)
        flayout.addWidget(self.rightbtn)
        frame.setLayout(flayout)

        # right_layout = QVBoxLayout()
        # right_layout.addWidget(main_frame)
        # right_layout.addWidget(frame)

        core_layout = QHBoxLayout()
        core_layout.addWidget(side_photo)
        core_layout.addWidget(main_frame)

        main_layout.addLayout(core_layout)
        main_layout.addWidget(frame)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
