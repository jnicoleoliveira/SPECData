""""[Filepaths]
project_directory: /home/joli/PycharmProjects/SPECdata
database_directory: /home/joli/PycharmProjects/SPECdata/data
database_file: /home/joli/PycharmProjects/SPECdata/data/spectrum.db


[OS]
os: Linux

import ConfigParser

Config = ConfigParser.ConfigParser()


#Config.read('./config')"""
class Config ():

    def __init__(self, project_directory, database_directory=None, database_filepath=None):
        self.PROJECT_DIR = project_directory
        self.DATABASE_DIR = database_directory
        self.DATABASE_FILEPATH = database_filepath
        self.CONN = None

    def set_as_default(self):
        """
        Set default Configuration Values.
        Dependent on Project directory
        :return:
        """
        import os
        self.PROJECT_DIR = os.curdir()
        self.DATABASE_DIR = os.path.join(self.PROJECT_DIR, "data")
        self.DATABASE_FILEPATH = os.path.join(self.DATABASE_DIR, 'spectrum.db')
        self.set_connection()

    def set_connection(self):
        """
        Set SQLite Connection to the database_filepath
        :return:
        """
        import sqlite3
        self.CONN = sqlite3.connect(self.database_filepath)

