# Author: Jasmine Oliveira
# Date: 06/27/2016
# SPECdata Configuration File:
#       * Specifies: Program Directory (path)
#                    Database Directory (path)
#                    Log Directory (path)

import os
import sqlite3

# Program directory
PROGRAM_DIR = dir_path = os.path.dirname(os.path.realpath(__file__))
# Database directory
DATABASE_DIR = dir_path = os.path.dirname(os.path.realpath(__file__))
# Log Directory
LOG_DIR = ""

# -------------------------------------------------------------- #
# --------------------- DO NOT EDIT BELOW ---------------------- #
# -------------------------------------------------------------- #

# GLOBAL CONFIG VARIABLES #
global db_path
global db_filepath
global conn

# SET VARIABLES TO DEFINED
db_dir = os.path.join(DATABASE_DIR , "data")
db_filepath = os.path.join(db_dir, "spectrum.db")
experiment_spectrums_path = os.path.join(db_dir, "experiments")
prog_dir = PROGRAM_DIR
resources = os.path.join(PROGRAM_DIR, "resources")

if os.path.exists(db_filepath):
    conn = sqlite3.connect(db_filepath)
