# Author: Jasmine Oliveira
# Date: 02/16/2017

from PyQt4.QtGui import *

import images
from app.dialogs.frames.experiment_view.frame___splatalogue_dock import Ui_DockWidget


class SplatalogueDockWidget(QDockWidget):
    def __init__(self, experiment):
        super(SplatalogueDockWidget, self).__init__()
        self.ui = Ui_DockWidget()
        self.ui.setupUi(self)
        # self.setWindowTitle("Splatalogue")

        self.list_widget = QListWidget()

        self.experiment = experiment
        self.__setup__()

    def __setup__(self):
        self.ui.add_btn.setIcon(QIcon(images.ADD_ICON))
        self.ui.wizard_btn.setIcon(QIcon(images.MAGIC_WAND_ICON))

        self.ui.frame.setLayout(self.ui.gridLayout_2)

        pixmap = QPixmap(images.SPLATALOGUE_LOGO_ICON)
        self.ui.logo_lbl.setPixmap(pixmap)
        self.ui.scrollArea.setWidget(self.list_widget)
        self.list_widget.setStyleSheet("background-color:rgb(63, 63, 63);")
        self.list_widget.show()
