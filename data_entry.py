import sqlite3
from config import *

def checkFile(filename):
    """
    Determines if a file can be opened / is a valid file.
    :param filename: Filepath/name
    :return: True if file can be opened. False if cannot.
    """
    try:
        myfile = open(filename)
    except IOError:
        print "Could not open file!"
        return False

    return True

def import_file(filename, name, type, info):
    """
    Imports file to spectrum database.
    :param filename: Filepath name. (.cat, .sp, .lines format)
    :param name: Name of molecule
    :param type: Type of data (known, experiment)
    :param info: String, info on molecule
    :return: None
    """

    # Check if file can be opened
    if(checkFile(filename) is False):
        return

    # Get File extention
    extention = str.split(filename, ".")[1]

    # Match extention to its appropriate import function
    if extention == '.cat':
        __import_catfile(filename, name, type, info)
    elif extention == '.sp':
        __import_spfile(filename, name, type, info)
    elif extention == '.lines':
        __import_linesfile(filename, name, type, info)
    else:
        print "Invalid import file. TYPE: '.cat' , '.sp', '.lines"



def __import_catfile(filename, name, type, info):
    """
    Inheritently Private Function, imports catfile to database
    :return:
    """
    # Connect to Database
    conn = sqlite3.connect(db_path + "\spectrum.db")

    with open(filename) as f:
        for line in f:
            point = str.split((line.strip()))


def __import_spfile(filename, name, type, info):
    """
    Imports .sp File to database
    :param filename:
    :param name:
    :param type:
    :param info:
    :return:
    """

def __import_linesfile(filename, name, type, info):
    """
    Imports .lines file to spectrum database
    :param filename:
    :param name:
    :param type:
    :param info:
    :return:
    """

