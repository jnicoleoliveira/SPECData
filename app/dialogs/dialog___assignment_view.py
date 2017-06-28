# Author: Jasmine Oliveira
# Date: 06/06/2017
# Description:
#   Updated AssignmentView from previous AssignmentWindow (8/24/2016)

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from app.widgets.widget___assignments_table import AssignmentTableWidget
from app.widgets.widget___filter_graph import FilterGraphWidget
from colors import *
from config import conn
from images import *


class AssignmentWindow(QDialog):

    def __init__(self, match, color, experiment):
        super(AssignmentWindow, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowIcon(QIcon(QPixmap(LOGO_ICON)))
        self.setWindowTitle("Assignment View")
        self.resize(1500, 750)
        self.setStyleSheet("background-color:" + BACKGROUND)

        # Data
        self.match = match
        self.color = color
        self.experiment = experiment

        # Widgets
        self.fgraph_widget = None
        self.info_table_widget = None
        self.assignment_table_widget = None

        self.__setup__()
        self.show()

    def __setup__(self):
        self.__setup_ui__()
        self.__setup_graph__()

    def __setup_ui__(self):
        # Constants
        margin = 5

        # Create Layouts
        layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        tool_bar_layout = QHBoxLayout()

        # ------------ Create Components -------------- #
        # Name Label
        name_lbl = QLabel(self.match.name)
        name_lbl.setStyleSheet("font: 30px; background:" + ACCENT_LIGHT + ";")
        name_lbl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        name_lbl.setMaximumHeight(50)
        name_lbl.setMargin(10)
        # Molecule Label
        molecule_lbl = QLabel()
        molecule_lbl.setStyleSheet("background:" + ACCENT_LIGHT + ";")
        molecule_lbl.setPixmap(QPixmap(MOLECULE_ICON).scaledToHeight(30))
        molecule_lbl.setMargin(5)

        # molecule_lbl.setMaximumHeight(30)
        molecule_lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        # Graphing Widget
        self.fgraph_widget = FilterGraphWidget(self.experiment.mid, self.match)
        # Info Table Widget
        self.info_table_widget = InfoTableWidget(self.match.mid)
        self.info_table_widget.setMinimumHeight((self.info_table_widget.rowCount()
                                                 * self.info_table_widget.rowHeight(0)) + 5)
        # self.info_table_widget.setMaximumWidth(404)
        stylesheet = "QHeaderView::section{Background-color:" + ACCENT + \
                     ";border - radius:14px;}"
        self.info_table_widget.setStyleSheet(stylesheet)
        # Table Widget
        self.assignment_table_widget = AssignmentTableWidget(self.experiment.mid, self.match)
        self.assignment_table_widget.setMaximumWidth(404)
        self.assignment_table_widget.setStyleSheet(stylesheet)

        # Tool Bar
        tool_frame = QFrame()
        tool_frame.setStyleSheet("background:" + FOREGROUND)
        tool_frame.setFrameShadow(QFrame.Raised)
        #       ---- Buttons ----
        validate_btn = QPushButton("Validate")
        validate_btn.setIcon(QIcon(THUMPS_UP_ICON))
        validate_btn.setIconSize(QSize(16, 16))
        validate_btn.setStyleSheet("font: 15px; background-color: " + GREEN_2)

        reject_btn = QPushButton("Reject")
        reject_btn.setIcon(QIcon(THUMPS_DOWN_ICON))
        reject_btn.setIconSize(QSize(16, 16))
        reject_btn.setStyleSheet("font: 15px; background-color: " + MAROON)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # -----------Add Widgets to Layout ------------ #
        # Title Layout
        title_layout.addWidget(molecule_lbl)
        title_layout.addWidget(name_lbl)
        title_layout.setSpacing(0)

        # Toolbar Layout
        tool_bar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum))
        tool_bar_layout.addWidget(validate_btn)
        tool_bar_layout.addWidget(reject_btn)
        tool_bar_layout.addWidget(cancel_btn)
        tool_bar_layout.setMargin(margin * 2)
        tool_frame.setLayout(tool_bar_layout)

        # Left layout
        left_layout.addLayout(title_layout)
        left_layout.addWidget(self.info_table_widget)
        left_layout.addWidget(self.assignment_table_widget)
        left_layout.setMargin(margin)
        left_layout.setSpacing(margin)

        # Right Layout
        right_layout.addWidget(self.fgraph_widget)
        #right_layout.addWidget(self.assignment_table_widget)
        right_layout.setMargin(margin)

        # Central Layout
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)
        layout.setMargin(margin)
        layout.setSpacing(margin)

        # Main Layout
        mlayout = QVBoxLayout()
        mlayout.addLayout(layout)
        mlayout.addWidget(tool_frame)
        # mlayout.setMargin(margin)
        mlayout.setSpacing(1)
        self.setLayout(mlayout)
        self.setStyleSheet("background:" + BACKGROUND_DARK)

    def __setup_graph__(self):
        self.fgraph_widget.filter_widget.experiment_peaks.click()
        self.fgraph_widget.filter_widget.matches.click()
        self.fgraph_widget.filter_widget.catalogue.click()
        if self.fgraph_widget.filter_widget.full_spectrum.isEnabled():
            self.fgraph_widget.filter_widget.full_spectrum.click()
        # self.fgraph_widget.graph_matches()
        # self.fgraph_widget.graph_catalog()


class InfoTableWidget(QTableWidget):
    def __init__(self, mid):
        super(InfoTableWidget, self).__init__()
        from app.dialogs.manage_database_view.dialog___manage_database import ManageDatabase
        from tables.molecules_table import get_category
        category = get_category(conn, mid)
        self.setMaximumWidth(900)

        if category == "artifact":
            ManageDatabase.populate_info_table_as_artifact(mid, self)
        else:
            ManageDatabase.populate_info_table_as_known(mid, self)

        self.change_settings()

    def change_settings(self):
        # -- Remove -- #
        self.removeRow(0)  # Remove the row: kid
        # --- Set Size Policy --- #
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # -- Set Additional Options -- #
        self.setEditTriggers(QTableWidget.NoEditTriggers)  # disallow in-table editing
        self.setSelectionMode(QAbstractItemView.NoSelection)
        #self.setSelectionBehavior()
        self.setShowGrid(False)
        self.horizontalHeader().setVisible(False)
        self.setSortingEnabled(False)
        self.horizontalHeader().setStretchLastSection(False)
        # -- Set Colors -- #
        stylesheet = "QHeaderView::section{Background-color:" + "#008080" + \
                     ";border - radius:14px;}"
        self.setStyleSheet(stylesheet)
