# Author: Jasmine Oliveira
# Date: 1/19/2017

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from app.dialogs.frames.experiment_view.frame___add_a_molecule import Ui_Dialog

from tables.molecules_table import get_mids_where_category_in, get_name
from config import conn


class AddAMolecule(QDialog):

    def __init__(self, selection_widget, experiment):
        super(AddAMolecule, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Add A Molecule")
        self.resize(500, 750)
        self.show()

        self.selection_widget = selection_widget
        self.experiment = experiment
        self.mids = []
        self.check_boxes = []

        self.__setup__()

    ###############################################################################
    # Setup Functions
    ###############################################################################
    def __setup__(self):

        self.ui.scrollArea.setWidgetResizable(True)
        self.ui.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.__setup_checkboxes()

        ## Setup Buttons ##
        self.ui.ok_btn.clicked.connect(self.ok)
        self.ui.cancel_btn.clicked.connect(self.cancel)
        self.ui.select_all_btn.clicked.connect(self.select_all)
        self.ui.deselect_all_btn.clicked.connect(self.deselect_all)
        self.ui.invert_btn.clicked.connect(self.invert)

    def __setup_checkboxes(self):

        self.mids = self.diff(get_mids_where_category_in(conn, ['known']),
                              self.experiment.get_assigned_mids())

        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)
        self.ui.scrollArea.setWidget(container)

        for m in self.mids:
            name = get_name(conn, m)
            check_box = QCheckBox(name)
            self.check_boxes.append(check_box)
            layout.addWidget(check_box)

    ###############################################################################
    # Button Functions
    ###############################################################################
    def ok(self):
        selected_mids = []
        for i in range(0, len(self.check_boxes)):
            if self.check_boxes[i].isChecked():
                selected_mids.append(self.mids[i])

        for m in selected_mids:
            match = self.experiment.add_a_molecule(m)
            print "added " + str(m)

            self.selection_widget.add_row(match)

    def cancel(self):
        """
        Cancel Function, closes the current dialog window.
        """
        self.close()

    def select_all(self):
        """
        'Clicks' all checkboxes that are not checked
        :return:
        """
        for c in self.check_boxes:
            if c.isChecked() is False:
                c.click()

    def deselect_all(self):
        """
        'Clicks' all checkboxes that are checked
        :return:
        """
        for c in self.check_boxes:
            if c.isChecked() is True:
                c.click()

    def invert(self):
        """
        'Clicks' all checkboxes to invert the selections
        :return:
        """

        for c in self.check_boxes:
            c.click()

    @staticmethod
    def diff(A, B):
        B = set(B)
        return [i for i in A if i not in B]

