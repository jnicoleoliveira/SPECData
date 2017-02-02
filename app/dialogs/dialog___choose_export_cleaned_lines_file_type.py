# Author: Jasmine Oliveira
# Date: 2/2/2017

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from analysis.experiment_write_up import ExperimentWriteUp
from app.dialogs.frames.experiment_view.frame___export_cleaned_lines_file_type import Ui_Dialog


class ChooseExportFileType(QDialog):
    def __init__(self):
        super(ChooseExportFileType, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Choose Export Type")
        self.resize(500, 750)

        self.__setup__()

    def __setup__(self):
        """

        """
        ''' Add File Types '''
        for f in ExperimentWriteUp.FileType:
            self.ui.type_cmbobx.addItem(f.title())
