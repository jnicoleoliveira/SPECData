# Author: Jasmine Oliveira
# Date: 2/2/2017

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from analysis.filetypes import *
from app.dialogs.frames.experiment_view.frame___export_cleaned_lines_file_type import Ui_Dialog
from app.events import display_error_message
from images import LOGO_ICON


class ChooseExportFileType(QDialog):
    def __init__(self):
        super(ChooseExportFileType, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowIcon(QIcon(QPixmap(LOGO_ICON)))

        self.setWindowTitle("Choose Export Type")
        self.resize(250, 250)

        self.file_types = []
        self.selected_type = None
        self.option = None

        self.type = None
        self.format = None
        self.delimiter = None
        self.shots = None

        self.__setup__()

    def OK(self):

        type_index = self.ui.type_cmbobx.currentIndex()
        format_index = self.ui.format_cmbobx.currentIndex()
        option = self.option

        if type_index == -1:
            display_error_message("Invalid input.", "Be sure to check that all fields are complete.",
                                  "Missing: File Type")
            return
        elif format_index == -1:
            display_error_message("Invalid input.", "Be sure to check that all fields are complete.",
                                  "Missing: File Format")
            return

        self.type = self.selected_type
        self.format = EXPORT_FILE_TYPES[self.selected_type].formats[format_index]

        if option is not None:
            print "NOT NONE"
            if isinstance(option, self.FTBOption):
                print "FTB TYPE"
                self.shots = option.get_shots()
                if self.shots is None:
                    display_error_message("Invalid input.", "Be sure to check that all fields are complete.",
                                          "Missing: Shots")
                    return
            elif isinstance(option, self.DelimiterOption):
                print "DELIMITER TYPE"
                self.delimiter = option.get_delimiter()
                if self.delimiter is None:
                    display_error_message("Invalid input.", "Be sure to check that all fields are complete.",
                                          "Missing: Delimiter")
                    return

        self.accept()

    def get_values(self):
        """
        Gets the values from the form
        :return: Type, format, delimiter, shots
        """
        return self.type, self.format, self.delimiter, self.shots

    def __setup__(self):
        """

        """
        ''' Add File Types to Combo Box'''
        for key, value in EXPORT_FILE_TYPES.iteritems():
            string = key.title() + "(" + value.extension + ")"
            self.ui.type_cmbobx.addItem(string)
            self.file_types.append(key)

        self.ui.type_cmbobx.setCurrentIndex(-1)

        self.connect(self.ui.type_cmbobx, SIGNAL("currentIndexChanged(const QString&)"), self.__populate_format_cmbobx)
        self.connect(self.ui.format_cmbobx, SIGNAL("currentIndexChanged(const QString&)"),
                     self.__populate_additional_options)
        self.ui.cancel_btn.clicked.connect(self.close)
        self.ui.ok_btn.clicked.connect(self.OK)

    def __populate_format_cmbobx(self):
        self.ui.format_cmbobx.clear()

        index = self.ui.type_cmbobx.currentIndex()
        key = self.file_types[index]
        self.selected_type = key

        for format in EXPORT_FILE_TYPES[key].formats:
            self.ui.format_cmbobx.addItem(format.title())

    def __populate_additional_options(self):

        index = self.ui.format_cmbobx.currentIndex()
        format = EXPORT_FILE_TYPES[self.selected_type].formats[index]

        frame = self.ui.additional_options_frame
        self.delete_layout(frame.layout())

        # New Layout
        try:
            layout = self.__setup_additional_options_layout(format)
        except AttributeError:
            return

        try:
            if layout is not None:
                frame.setLayout(layout)
        except RuntimeError:
            return

    def __setup_additional_options_layout(self, format):

        if format == FileFormat.DELIMITER:
            self.option = self.DelimiterOption()
        elif format == FileFormat.FTB_ESTIMATED_SHOTS:
            self.option = self.FTBOption(True)
        elif format == FileFormat.FTB_FIXED_SHOTS:
            self.option = self.FTBOption()
        else:
            self.option = None
            return None

        return self.option.layout

    def delete_layout(self, layout):
        import sip
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.delete_layout(item.layout())
            sip.delete(layout)

    class DelimiterOption():
        def __init__(self):
            self.layout = QGridLayout()
            self.radio_btns = []

            self.line_edit = QLineEdit()
            self.__setup__()

        def __setup__(self):

            label = QLabel("Delimiter")
            space_btn = QRadioButton("Space")
            tab_btn = QRadioButton("Tab")
            comma_btn = QRadioButton("Comma")
            other_btn = QRadioButton("Other")

            h_layout = QHBoxLayout()
            h_layout.addWidget(other_btn)
            h_layout.addWidget(self.line_edit)

            v_layout = QHBoxLayout()
            v_layout.addWidget(space_btn)
            v_layout.addWidget(tab_btn)
            v_layout.addWidget(comma_btn)

            self.layout.addWidget(label, 0, 0)
            self.layout.addLayout(v_layout, 1, 0)
            self.layout.addLayout(h_layout, 2, 0)

            self.radio_btns.append(space_btn)
            self.radio_btns.append(tab_btn)
            self.radio_btns.append(comma_btn)
            self.radio_btns.append(other_btn)

        def get_delimiter(self):
            for btn in self.radio_btns:
                if btn.isChecked():
                    text = str(btn.text())
                    if text == "Space":
                        return " "
                    elif text == "Tab":
                        return "\t"
                    elif text == "Comma":
                        return ","
                    elif text == "Other":
                        if self.line_edit.text() is not "":
                            return self.line_edit.text()

            return None

    class FTBOption:
        def __init__(self, auto=False):
            self.layout = QGridLayout()
            self.line_edit = QLineEdit()
            self.__setup__(auto)

        def __setup__(self, auto):
            text = "Max Shots" if auto is True else "Shots"

            label = QLabel(text)
            self.layout.addWidget(label, 0, 0)
            self.layout.addWidget(self.line_edit, 0, 1)

        def get_shots(self):
            if self.line_edit.text() == "":
                return None
            return self.line_edit.text()
