# Author: Jasmine Oliveira
# Date: 10/03/2016
#
# * Form widget that displays the experiment info for Experiment View
#

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from frames.frame___experiment_info_widget import Ui_Form
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget

from config import conn
#from tables.get import get_peaks
import tables.peaks_table as peaks_table

class ExperimentInfoWidget(QWidget):

    def __init__(self, experiment):
        super(ExperimentInfoWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.setup(experiment)
        #self.show()

    def setup(self, experiment):
        # Get Data
        mid = experiment.mid
        name = experiment.name
        total_peaks = peaks_table.get_peak_count(conn, mid)
        peaks_assigned = experiment.get_assigned_peaks_count()
        peaks_unassigned = total_peaks - peaks_assigned
        molecules_found = len(experiment.molecule_matches)

        # Set labels to data
        self.ui.experiment_name_lbl.setText(name)
        self.ui.composition_val.setText('C2H2 + CS2')
        self.ui.total_peaks_val.setText(str(total_peaks))
        self.ui.peaks_assigned_val.setText(str(peaks_assigned))
        self.ui.peaks_unassigned_val.setText(str(peaks_unassigned))
        self.ui.molecules_found_val.setText(str(molecules_found))
        self.ui.info_val_lbl.setText("Discharge")
        # Formatting
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        layout = self.ui.gridLayout

        # Elipsis Widget
        #set_angle = 0
        #angle = 90
        #ellipse = QGraphicsEllipseItem()
        #brush = QBrush()
        #color = QColor()
        #color.setNamedColor("green")
        #brush.setColor(color)
        #ellipse.setStartAngle(set_angle)
        #ellipse.setSpanAngle(angle)
        #ellipse.setBrush(brush)

        #color.setNamedColor("red")
        #brush.setColor(color)
        #ellipse.setStartAngle(angle)
        #ellipse.setSpanAngle(0)
        #ellipse.setBrush(brush)
        #layout.addWidget(ellipse, 3, 3)
        #plot_widget = MatplotlibWidget()
        #info_graph = InfoGraph(plot_widget)
        #layout.addWidget(plot_widget, 3, 3)
        #info_graph.plot(peaks_assigned, peaks_unassigned)


class InfoGraph():

    def __init__(self, plot_widget):
        self.plot_widget = plot_widget

    def plot(self, peaks_assigned, peaks_unassigned):
        labels = ['Assigned', 'Unassigned']
        sizes = [peaks_assigned, peaks_unassigned]
        colors = ['yellowgreen', 'lightcoral']
        explode = (0.05, 0)

        #figure = self.plot_widget.getFigure()
        figure = self.plot_widget.getFigure()
        subplot = figure.add_subplot(111)
        subplot.pie(sizes, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', shadow=True, startangle=90)

        subplot.axis('equal')

        ax = figure.gca().set_aspect('1')

        #ax.set_xticks([0, 1])
        #ax.set_aspect('equal')

        self.plot_widget.draw()


