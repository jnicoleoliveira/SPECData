# Author: Jasmine Oliveira
# Date: 06/06/2017
# Description:
#   Updated AssignmentView from previous AssignmentWindow (8/24/2016)

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from app.widgets.widget___donut_chart import DonutChartWidget
from app.widgets.widget___filter_graph import FilterGraphWidget
from colors import *
from config import conn
from images import LOGO_ICON


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
        # Create Layouts
        layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        # ------------ Create Components -------------- #
        # Name Label
        name_lbl = QLabel(self.match.name)
        name_lbl.setStyleSheet("font: 15px;")
        name_lbl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # Graphing Widget
        self.fgraph_widget = FilterGraphWidget(self.experiment.mid, self.match)
        # Info Table Widget
        self.info_table_widget = InfoTableWidget(self.match.mid)
        self.info_table_widget.setMinimumHeight((self.info_table_widget.rowCount()
                                                 * self.info_table_widget.rowHeight(0)) + 5)
        # Donut Widget
        self.donut = DonutChartWidget()
        self.donut.setMaximumSize(100, 100)
        # Assignment Table Widget
        # self.assignment_table_widget = QTableWidget()

        # -----------Add Widgets to Layout ------------ #
        # Left layout
        left_layout.addWidget(name_lbl)
        left_layout.addWidget(self.info_table_widget)
        left_layout.addSpacerItem(QSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)))
        left_layout.addWidget(self.donut)
        # Right Layout
        right_layout.addWidget(self.fgraph_widget)
        right_layout.addWidget(self.assignment_table_widget)
        # Central Layout
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.setLayout(layout)

    def __setup_graph__(self):
        self.fgraph_widget.filter_widget.matches.click()
        # self.fgraph_widget.filter_widget.catalogue.click()
        # self.fgraph_widget.graph_matches()
        # self.fgraph_widget.graph_catalog()


class InfoTableWidget(QTableWidget):
    def __init__(self, mid):
        super(InfoTableWidget, self).__init__()
        from app.dialogs.manage_database_view.dialog___manage_database import ManageDatabase
        from tables.molecules_table import get_category
        category = get_category(conn, mid)

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
