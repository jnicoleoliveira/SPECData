import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


def clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()

        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


def select_file(plain_txt_box):
    """
    Displays a 'select file box'.
    After selection, it inserts the file path chosen in the plain_text_box
    :param plain_txt_box: Text box for path to be written
    :return:
    """
    import os
    w = QWidget()
    w.resize(320, 240)
    w.setWindowTitle("Open File")
    file_path = QFileDialog.getOpenFileName(w, 'Open File', os.path.curdir)
    plain_txt_box.setPlainText(file_path)


def save_as_file(line_edit_txt_box):
    """

    :param line_edit_txt_box:
    :return:
    """
    import os
    w = QWidget()
    w.resize(320, 240)
    w.setWindowTitle("Save As")
    filters = "Text files (*.txt);;Spectrum Files (*.sp);;Cat File (*.cat);;Lines file (*.lines)"
    selected_filter = "Lines file (*.lines)"
    file_path = QFileDialog.getSaveFileName(w, 'Save As', os.path.curdir, filters, selected_filter)
    line_edit_txt_box.setText(file_path)


def display_error_message(text, informative_text,  detailed_text):
    """
    Displays a Message Box, for an error message.
    :param text: General Error Statement
    :param informative_text: String for further information of the error
    :param detailed_text: Specific, and detailed error found.
    :return:
    """
    msg = QMessageBox()
    msg.resize(320, 120)
    msg.setIcon(QMessageBox.Critical)
    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle("Error")
    msg.setDetailedText(detailed_text)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def display_informative_message(text):
    """
    Displays a Message Box, for an informative message.
    :param text: (String) General Info Statement
    :return:
    """
    msg = QMessageBox()
    msg.resize(320, 120)
    msg.setIcon(QMessageBox.Information)
    msg.setText(text)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setWindowTitle("Info Message")
    msg.exec_()


def display_overwrite_file_question_message(file_name):
    """
    Displays a Message Box, for an overwrite file question?
    :param file_name: (string) Name of file to overwrite
    :return: True: If selected YES to overwrite
             False: If selected NO to overwrite
    """
    msg = QMessageBox()
    msg.resize(320, 120)
    msg.setIcon(QMessageBox.Question)
    msg.setText("A file named " + file_name + " already exists."\
                + " Are you sure you want to overwrite it?")
    msg.setStandardButtons(QMessageBox.Yes, QMessageBox.No)
    msg.setWindowTitle("Overwrite File?")
    msg.exec_()

    result = msg.result()

    if result is QMessageBox.Yes:
        return True

    return False



