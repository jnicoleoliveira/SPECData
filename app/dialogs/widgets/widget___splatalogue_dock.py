# Author: Jasmine Oliveira
# Date: 02/16/2017

from PyQt4.QtGui import *

import images
from  analysis.splatalogue_analysis import SplatalogueAnalysis
from app.dialogs.frames.experiment_view.frame___splatalogue_dock import Ui_DockWidget


class SplatalogueDockWidget(QDockWidget):
    def __init__(self, experiment):
        super(SplatalogueDockWidget, self).__init__()
        self.ui = Ui_DockWidget()
        self.ui.setupUi(self)
        # self.setWindowTitle("Splatalogue")

        self.list_widget = QListWidget()

        self.splat_analysis = SplatalogueAnalysis(experiment)
        self.__setup__()


    def __setup__(self):
        """
        Setup the layout, and connect buttons
        """

        ''' Widgets '''
        add_btn = self.ui.add_btn
        wizard_btn = self.ui.wizard_btn

        ''' Set Images '''
        add_btn.setIcon(QIcon(images.ADD_ICON))
        wizard_btn.setIcon(QIcon(images.MAGIC_WAND_ICON))
        self.ui.logo_lbl.setPixmap(QPixmap(images.SPLATALOGUE_LOGO_ICON))

        ''' Layout '''
        self.ui.frame.setLayout(self.ui.gridLayout_2)
        self.ui.scrollArea.setWidget(self.list_widget)
        self.list_widget.setStyleSheet("background-color:rgb(63, 63, 63);")
        self.ui.frame.setLayout(self.ui.gridLayout_2)

        self.populate_list_widget()

    def populate_list_widget(self):
        self.splat_analysis.find_matches()
        for key, value in self.splat_analysis.chemicals.iteritems():
            item = QListWidgetItem(str(key) + "\t" + str(len(value.lines)))
            self.list_widget.addItem(item)
