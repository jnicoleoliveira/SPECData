# Author: Jasmine N Oliveira
# Date 06/16/2017
# QTableWidget that Displays assignments, and allows edits

from PyQt4.QtGui import *

from colors import *
from config import conn
from images import SUBTRACT_ICON, ADD_ICON, EXPORT_ICON


class AssignmentTableWidget(QWidget):
    def __init__(self, experiment_mid, match):
        super(AssignmentTableWidget, self).__init__()
        self.molecule_match = match
        self.experiment_mid = experiment_mid

        self.table_widget = TableWidget(match)
        self.toolbar_widget = ToolbarWidget()

        self.__setup__()

    def __setup__(self):
        layout = QGridLayout()
        frame = QFrame()

        layout.addWidget(self.toolbar_widget)
        layout.addWidget(self.table_widget)
        layout.setMargin(0)
        layout.setSpacing(0)

        frame.setLayout(layout)
        # frame.setStyleSheet("margin:1px; border:1px solid white; ")

        newlayout = QVBoxLayout()
        newlayout.setSpacing(0)
        newlayout.setMargin(0)
        newlayout.addWidget(frame)

        self.setStyleSheet("background:" + FOREGROUND)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setLayout(newlayout)


class TableWidget(QTableWidget):
    def __init__(self, match):
        super(TableWidget, self).__init__()
        self.match = match
        self.__setup__()

    def __setup__(self):
        self.populate_table_widget()

    def populate_table_widget(self):
        """
        Populate table_widget with the following __setup_graph data:
            Experiment PID, Frequency, Intensity with its associative
            match's PID, frequency, and intensity
        :return:
        """
        matches = self.match.matches
        import tables.peaks_table as peaks

        row_count = len(matches)  # Number of values
        column_count = 4  # Columns
        # self.table_widget = QTableWidget()

        # Format Table
        self.setRowCount(row_count)
        self.setColumnCount(column_count)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setSortingEnabled(True)

        # Set Header Label
        self.setHorizontalHeaderLabels(["Frequency", "Intensity", \
                                        "Frequency", "Intensity"])

        # Populate Table Widget with data
        #   Exp_pid, Exp_frequency, Exp_intensity
        #   Match_Pid, Match_frequency, Match_intensity
        for i in range(0, row_count):
            # Get Row Data
            pid = matches[i].pid
            exp_pid = matches[i].exp_pid
            match_frequency, match_intensity = peaks.get_frequency_intensity(conn, pid)
            exp_frequency, exp_intensity = peaks.get_frequency_intensity(conn, exp_pid)
            # Convert Data to QTableWidgetItem
            exp_frequency_item = QTableWidgetItem(str(exp_frequency))
            exp_intensity_item = QTableWidgetItem(str(exp_intensity))
            match_frequency_item = QTableWidgetItem(str(match_frequency))
            match_intensity_item = QTableWidgetItem(str(match_intensity))

            color = QColor(FOREGROUND)
            match_frequency_item.setBackgroundColor(color)
            match_intensity_item.setBackgroundColor(color)
            color = QColor(BACKGROUND_LIGHT)
            exp_frequency_item.setBackground(color)
            exp_intensity_item.setBackground(color)
            # Add Widget Items to Table
            self.setItem(i, 0, exp_frequency_item)
            self.setItem(i, 1, exp_intensity_item)
            self.setItem(i, 2, match_frequency_item)
            self.setItem(i, 3, match_intensity_item)

        # --- Set Size Policy --- #0
        # self.resizeRowsToContents()
        # width = self.horizontalHeader().width()
        # self.setFixedWidth(width)

        # -- Additional Options -- #
        self.setEditTriggers(QTableWidget.NoEditTriggers)  # disallow in-table editing
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)


class ToolbarWidget(QWidget):
    def __init__(self):
        super(ToolbarWidget, self).__init__()
        self.add_btn = QPushButton()
        self.remove_btn = QPushButton()
        self.export_btn = QPushButton()

        self.__setup__()
        self.show()

    def __setup__(self):
        self.__setup_ui__()

    def __setup_ui__(self):
        layout = QHBoxLayout()
        frame = QFrame()

        self.add_btn.setIcon(QIcon(QPixmap(ADD_ICON)))
        self.remove_btn.setIcon(QIcon(QPixmap(SUBTRACT_ICON)))  # .scaled(25,25)))
        self.export_btn.setIcon(QIcon(QPixmap(EXPORT_ICON)))

        self.add_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.remove_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.export_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)

        layout.addWidget(self.add_btn)
        layout.addWidget(self.remove_btn)
        layout.addWidget(self.export_btn)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        layout.setSpacing(3)
        layout.setMargin(5)

        # Frame settings
        # frame.setFrameShape(QFrame.StyledPanel)
        # frame.setFrameShadow(QFrame.Raised)
        # frame.setLineWidth(5)


        frame.setLayout(layout)

        l = QHBoxLayout()
        l.addWidget(frame)
        l.setSpacing(0)
        l.setMargin(0)

        self.setLayout(l)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setMaximumHeight(40)
        self.setStyleSheet("background-color:" + FOREGROUND + ";" +
                           "margin:1px; border:1px solid" + "WHITE" + "; ")

    def add_assignment(self):
        print "add_assignment"
