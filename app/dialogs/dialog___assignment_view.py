# Author: Jasmine Oliveira
# Date: 06/06/2017
# Description:
#   Updated AssignmentView from previous AssignmentWindow (8/24/2016)

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from app.widgets.widget___filter_graph import FilterGraphWidget
from config import conn
from images import LOGO_ICON


class AssignmentWindow(QDialog):

    def __init__(self, match, color, experiment):
        super(AssignmentWindow, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowIcon(QIcon(QPixmap(LOGO_ICON)))
        self.setWindowTitle("Assignment View")
        self.resize(1500, 750)

        # Data
        self.match = match
        self.color = color
        self.experiment = experiment

        # Widgets
        self.fgraph_widget = FilterGraphWidget()
        self.info_table_widget = InfoTableWidget(match.mid)

        self.__setup__()
        self.show()

    def __setup__(self):
        layout = QHBoxLayout()
        layout.addWidget(self.info_table_widget)
        layout.addWidget(self.fgraph_widget)

        self.setLayout(layout)


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
        # --- Set Size Policy --- #
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # -- Set Additional Options -- #
        self.setEditTriggers(QTableWidget.NoEditTriggers)  # disallow in-table editing
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setShowGrid(False)
        self.horizontalHeader().setVisible(False)
        self.setSortingEnabled(False)
        self.horizontalHeader().setStretchLastSection(False)

        # -- Set Colors -- #
        stylesheet = "QHeaderView::section{Background-color:" + "#008080" + \
                     ";border - radius:14px;}"
        self.setStyleSheet(stylesheet)
