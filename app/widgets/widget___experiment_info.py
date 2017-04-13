# Author: Jasmine Oliveira
# Date: 10/03/2016
#
# * Form widget that displays the experiment info for Experiment View
#

from PyQt4.QtGui import *

import tables.experimentinfo_table as info_table
import tables.peaks_table as peaks_table
from app.dialogs.frames.experiment_view.frame___experiment_info_widget import Ui_Form
from config import conn


class ExperimentInfoWidget(QWidget):

    def __init__(self, experiment):
        super(ExperimentInfoWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.__setup__(experiment)
        #self.show()

    def __setup__(self, experiment):
        """

        :param experiment:
        :return:
        """
        mid = experiment.mid
        name = experiment.name
        composition = info_table.get_composition(conn, mid)
        notes = info_table.get_notes(conn, mid)
        units = info_table.get_units(conn, mid)
        type = info_table.get_type(conn, mid)

        total_peaks = peaks_table.get_peak_count(conn, mid)
        assigned = experiment.get_assigned_peaks_count()

        invalid_mol, invalid_peaks = experiment.get_invalidated_peaks_count()
        valid_mol, valid_peaks = experiment.get_validated_count()

        pending_peaks = assigned - valid_peaks - invalid_peaks
        pending_mol = len(experiment.molecule_matches) - invalid_mol - valid_mol

        unnassigned = total_peaks - valid_peaks

        # Set labels to data #
        self.ui.experiment_name_lbl.setText(name)
        self.ui.composition_val.setText(composition)
        self.ui.notes_val.setText(notes)
        self.ui.units_val.setText(units)
        self.ui.type_val.setText(type)

        self.ui.total_peaks_val.setText(str(total_peaks))

        self.ui.invalid_mol_num.display(invalid_mol)
        self.ui.invalid_peaks_num.display(invalid_peaks)
        self.ui.valid_mol_num.display(valid_mol)
        self.ui.valid_peaks_num.display(valid_peaks)
        self.ui.pending_mol_num.display(pending_mol)
        self.ui.pending_peaks_num.display(pending_peaks)
        self.ui.unnassigned_peaks_num.display(unnassigned)

        # Formatting
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        #
        # lcds  = [self.ui.pending_mol_num, self.ui.pending_peaks_num,
        #          self.ui.invalid_peaks_num, self.ui.invalid_mol_num,
        #          self.ui.valid_mol_num, self.ui.valid_peaks_num,
        #          self.ui.unnassigned_peaks_num]
        #
        # for n in lcds:
        #     n.setNumDigits(10)

    def update(self, experiment):
        self.__setup__(experiment)

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


