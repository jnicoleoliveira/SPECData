# Author: Jasmine Oliveira
# Date: 01/11/2017

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from app.dialogs.frames.experiment_view.frame___graph_toolbox_dock_widget import Ui_GraphingOptions


class GraphToolBoxDock(QDockWidget):

    def __init__(self):
        super(GraphToolBoxDock, self).__init__()
        self.ui = Ui_GraphingOptions()
        self.ui.setupUi(self)
        self.setWindowTitle("Graphing Options")

        #self.ui.full_spectrum_slider.setMaximum(1)
        #self.ui.full_spectrum_slider.setMinimum(0)
        #self.ui.full_spectrum_slider.setTickInterval(0)

        self.show()
        l1 = self.ui.gridLayout
        l2 = self.ui.gridLayout_4

        self.full_spectrum_slider = ToggleSlider()
        self.show_validations_slider = ToggleSlider()
        self.share_yaxis_slider = ToggleSlider()
        self.share_intensities_slider = ToggleSlider()

        l1.addWidget(self.full_spectrum_slider, 1, 1)
        l1.addWidget(self.show_validations_slider, 2, 1)

        l2.addWidget(self.share_yaxis_slider, 0, 1)
        l2.addWidget(self.share_intensities_slider, 1 , 1)

    def reset(self):
        self.full_spectrum_slider.toggle_off()
        self.show_validations_slider.toggle_off()
        self.share_yaxis_slider.toggle_off()
        self.share_intensities_slider.toggle_off()


class ToggleSlider(QSlider):

    def __init__(self, parent=None):
        super(ToggleSlider, self).__init__(parent)
        self.setMaximum(1)
        self.setMinimum(0)
        self.setTickInterval(0)
        self.setOrientation(Qt.Horizontal)

    def mousePressEvent(self, event):

        if self.value() == 0:
            self.setValue(1)
            self.setStyleSheet("background-color: #91dc5a;")
        else:
            self.setValue(0)
            self.setStyleSheet("")

    def is_toggled_on(self):
        return True if self.value() == 1 else False

    def toggle_off(self):
        self.setValue(0)
        self.setStyleSheet("")
