from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time


class LoadingProgressScreen:

    def __init__(self, parent=None):
        self.dialog = QProgressDialog("Please Wait", "Cancel", 0, 100)

    def start(self):
        self.dialog.setWindowModality(Qt.WindowModal)
        self.dialog.setAutoReset(True)
        self.dialog.setAutoClose(True)
        self.dialog.setMinimum(0)
        self.dialog.setMaximum(100)
        self.dialog.resize(200, 200)
        self.dialog.setWindowTitle("Progress")
        self.dialog.show()
        self.dialog.setValue(0)
        QApplication.processEvents()


    def next_value(self, value):
        self.dialog.setValue(value)
        QApplication.processEvents()
        #self.dialog.show()

    def set_caption(self,text):
        self.dialog.setLabelText(text)

    def end(self):
        self.dialog.setValue(100)
        time.sleep(2)
        self.dialog.hide()

