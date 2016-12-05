# Author: Jasmine Oliveira
# Date: 06/27/2016
# SPECdata Configuration File:
#       * Specifies: Program Directory (path)
#                    Database Directory (path)
#                    Log Directory (path)

# Imports
import sqlite3
import os

# Program directory
PROGRAM_DIR = dir_path = os.path.dirname(os.path.realpath(__file__))
print PROGRAM_DIR
# Database directory
DATABASE_DIR = dir_path = os.path.dirname(os.path.realpath(__file__))

# Log Directory
LOG_DIR = ""

##################################################################
####################### DO NOT EDIT BELOW ########################
##################################################################


# GLOBAL CONFIG VARIABLES #
global db_path
global db_filepath
global conn

# SET VARIABLES TO DEFINED
db_dir = os.path.join(DATABASE_DIR , "data")
db_filepath = os.path.join(db_dir, "spectrum.db")
experiment_spectrums_path = os.path.join(db_filepath, "experiments")
prog_dir = PROGRAM_DIR
conn = sqlite3.connect(db_filepath)
resources = os.path.join(PROGRAM_DIR, "resources")