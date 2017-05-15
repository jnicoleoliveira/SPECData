# Author: Jasmine Oliveira
# Date: 5/12/2017

from PyQt4.QtGui import *

from app.error import is_file
from app.events import select_file, display_error_message
from dialog___create_executable import CreateExecutable
from dialog___wizard_window import WizardWindow

class SetupDatabase(WizardWindow):
    def __init__(self):
        super(SetupDatabase, self).__init__(True)

        ''' Widgets '''
        self.create_database_btn = QRadioButton()
        self.import_database_btn = QRadioButton()
        self.file_txt = QLineEdit()
        self.select_btn = QToolButton()
        self.file_path = None

        ''' Setup '''
        self.title.setText("Setup Database")
        self.__setup_center_layout()
        self.__setup_buttons()
        self.show()

    def __setup_buttons(self):

        self.rightbtn.setText("Cancel")
        self.leftbtn.setText("Next")

        self.leftbtn.clicked.connect(self.next_btn_action)
        self.rightbtn.clicked.connect(self.close)

        self.import_database_btn.toggled.connect(self.import_database_btn_clicked)
        self.select_btn.clicked.connect((lambda x: select_file(self.file_txt)))

    def __setup_center_layout(self):
        """

        :return:
        """
        # Radio Buttons
        self.create_database_btn.setText("No, create a new database.")
        self.create_database_btn.setStyleSheet(self.body_font)
        self.import_database_btn.setText("Yes, import a database..")
        self.import_database_btn.setStyleSheet(self.body_font)

        # Description
        description = QLabel("Do you want to import a database from another version of SPECdata?")
        description.setStyleSheet(self.body_font)
        description.setContentsMargins(0, 15, 0, 0)
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)

        #################################################
        # Import Database
        #################################################

        # File Selection
        file_layout = QHBoxLayout()
        self.select_btn.setText("...")
        self.select_btn.setDisabled(True)
        self.file_txt.setDisabled(True)
        file_layout.addSpacerItem(QSpacerItem(20, 20))
        file_layout.addWidget(self.file_txt)
        file_layout.addWidget(self.select_btn)

        # Import Layout
        import_layout = QVBoxLayout()
        import_layout.addWidget(self.import_database_btn)
        import_layout.addLayout(file_layout)
        import_layout.setSpacing(0)


        # Radio Button Full Layout
        layout = QVBoxLayout()
        layout.setSpacing(6)
        layout.addWidget(self.create_database_btn)
        layout.addLayout(import_layout)
        layout.setContentsMargins(5, 5, 0, 0)

        # Add Buttons to Cetner
        # self.center_layout.addItem(spacer, 0, 0)
        self.center_layout.addWidget(description, 1, 0)
        self.center_layout.addLayout(layout, 2, 0)
        self.center_layout.addItem(spacer, 3, 0)

    def import_database_btn_clicked(self):
        """
        Toggle file selector and btn enabled/disabled
        :return:
        """
        if self.file_txt.isEnabled():
            self.file_txt.setDisabled(True)
            self.select_btn.setDisabled(True)
        else:
            self.file_txt.setEnabled(True)
            self.select_btn.setEnabled(True)

    def open_next_window(self):
        self.close()
        window = CreateExecutable()
        window.show()
        window.exec_()

    def next_btn_action(self):
        error = None
        if self.create_database_btn.isChecked():
            msg = self.create_new_database()
        elif self.import_database_btn.isChecked():
            self.file_path = str(self.file_txt.text())
            if is_file(self.file_path):
                msg = self.import_database()
            else:
                error = "Invalid file selection!"
                msg = "Please select a valid database file."
        else:
            error = "Please choose an option to continue."
            msg = "Choose an option to create a new or import an existing database."
        if error is None:
            self.open_next_window()
        else:
            display_error_message(error, msg, msg)

    def check_schema(self, path):
        import sqlite3
        tconn = sqlite3.connect(path)
        tconn.execute("")

    def import_database(self):
        """

        :return:
        """

        import os
        from config import db_dir, experiment_spectrums_path

        log = ""

        # Create 'data' directory
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            log += "[Created Directory:  " + db_dir + "]" + "\n"

        # Create 'experiments' directory
        if not os.path.exists(experiment_spectrums_path):
            os.makedirs(experiment_spectrums_path)
            log += "[Created Directory: " + experiment_spectrums_path + "]" + "\n"

        # Copy File to Location ("Import")
        from shutil import copyfile
        experiment_file_path = os.path.join(db_dir + "spectrum.db")
        copyfile(str(self.file_path), experiment_file_path)
        return None, None

    def create_new_database(self):
        import os
        import sqlite3
        from config import db_dir, db_filepath, experiment_spectrums_path, schema

        log = ""
        # Create 'data' directory
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            log += "[Created Directory: " + db_dir + "]" + "\n"

        # Create spectrum database file
        conn = sqlite3.connect(db_filepath)
        log += "[Created Database File: " + db_filepath + " ]" + "\n"

        # Create 'experiments' directory
        if not os.path.exists(experiment_spectrums_path):
            os.makedirs(experiment_spectrums_path)
            log += "[Created Directory: " + experiment_spectrums_path + "]" + "\n"

        # Create Cursor
        cursor = conn.cursor()

        # Execute SQL Script 'build_tables'
        script = open(schema, 'r').read()
        sqlite3.complete_statement(script)

        try:
            cursor.executescript(script)
        except Exception as e:
            cursor.close()
            print "Table Already exists!"

        log += "[Built Tables]" + "\n"

        # Close DB connection
        conn.close()
        log += "[INIT COMPLETE]" + "\n"

        return None, None

class SetupComplete(WizardWindow):
    def __init__(self):
        super(SetupComplete, self).__init__()

    def __setup_buttons(self):
        self.rightbtn.setText("Cancel")
        self.leftbtn.setText("Next")
        self.rightbtn.clicked.connect()
        self.leftbtn.clicked.connect()

        # def __setup_center_layout(self):
        #     layout =
        #
        # def right_btn_action(self):
