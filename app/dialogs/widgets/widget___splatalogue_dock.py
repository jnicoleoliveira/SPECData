# Author: Jasmine Oliveira
# Date: 02/16/2017

from PyQt4.QtGui import *

import images
from  analysis.splatalogue_analysis import SplatalogueAnalysis
from app.dialogs.dialog___splatalogue_assignment_view import SplatalogueAssignmentWindow
from app.dialogs.frames.experiment_view.frame___splatalogue_dock import Ui_DockWidget

class SplatalogueDockWidget(QDockWidget):
    def __init__(self, experiment):
        super(SplatalogueDockWidget, self).__init__()
        self.ui = Ui_DockWidget()
        self.ui.setupUi(self)
        # self.setWindowTitle("Splatalogue")

        self.most_likely_list_widget = QListWidget()
        self.likely_list_widget = QListWidget()
        self.least_likely_list_widget = QListWidget()

        self.toolbox = QToolBox()

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

        ''' Functions '''
        self.most_likely_list_widget.doubleClicked.connect(self.open_assignment_view)
        self.likely_list_widget.doubleClicked.connect(self.open_assignment_view)
        self.least_likely_list_widget.doubleClicked.connect(self.open_assignment_view)

        ''' Layout '''
        self.ui.frame.setLayout(self.ui.gridLayout_2)

        toolbox = QToolBox()
        toolbox.addItem(self.most_likely_list_widget, "Most Likely")
        toolbox.addItem(self.likely_list_widget, "Likely")
        toolbox.addItem(self.least_likely_list_widget, "Least Likely")
        self.toolbox = toolbox
        self.ui.scrollArea.setWidget(toolbox)
        self.most_likely_list_widget.setStyleSheet("background-color:rgb(63, 63, 63);")
        self.ui.frame.setLayout(self.ui.gridLayout_2)

        self.populate_lists_with_matches()

    def populate_lists_with_matches(self):
        """

        """
        self.splat_analysis.find_matches()
        most_likely, likely, least_likely = self.splat_analysis.get_likelihood_chemical_lists()

        self.update_list_widget_title(0, "Most Likely", len(most_likely))
        self.update_list_widget_title(1, "Likely", len(likely))
        self.update_list_widget_title(2, "Least likely", len(least_likely))

        self.populate_list_widget(most_likely, self.most_likely_list_widget)
        self.populate_list_widget(likely, self.likely_list_widget)
        self.populate_list_widget(least_likely, self.least_likely_list_widget)

    def populate_list_widget(self, list, list_widget):
        """

        :param list:
        :param list_widget:
        :return:
        """
        for c in list:
            N = str(c.N)
            name = str(c.name)
            if len(N) == 2:
                delim = " "
            else:
                delim = "   "
            item = QListWidgetItem(N + delim + name)
            list_widget.addItem(item)

    def update_list_widget_title(self, index, string, count):
        """

        :param index:
        :param string:
        :param count:
        :return:
        """
        s = string + " (" + str(count) + ")"
        self.toolbox.setItemText(index, s)

    def open_assignment_view(self):
        index = self.toolbox.currentIndex()

        if index == 0:
            list_widget = self.most_likely_list_widget
        elif index == 1:
            list_widget = self.likely_list_widget
        else:
            list_widget = self.least_likely_list_widget

        item = list_widget.selectedItems()[0]
        text = str(item.text()).split()

        chemical = self.splat_analysis.chemicals[text[1]]

        window = SplatalogueAssignmentWindow(self.splat_analysis.experiment, chemical)
        window.exec_()
