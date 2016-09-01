# Author: Jasmine Oliveira
# Date: 06/27/2016
import sqlite3
import molecule_entry
from config import *

def import_peaks(filepath, mid):
    """
    Imports file to peak table in spectrum database to it's associative molecule
    Molecule must exist for import
    :param filepath: Path to import file
    :param mid: Molecule ID
    :return:
    """

    # Connect to Database, create cursor
    conn = sqlite3.connect(db_filepath)
    cursor = conn.cursor()

    # Check if molecule entry exists
    if (molecule_entry.mid_exists(conn, cursor, mid)):
        # Molecule does not exist, ERR return
        print "[ ERROR: Molecule entry does not exist. Cancelling action! ]"
        return

    # Check if file can be opened
    if __checkfile(filepath) is False:
        # File cannot be opened. ERR return
        return

    # Get File extention
    extention = str.split(filepath, ".")[1]

    # Match extention to its appropriate import function
    if extention == 'cat':
        __import_catfile(conn, filepath, mid)
    elif extention == 'sp':
        __import_spfile(conn, filepath, mid)
    elif extention == 'lines':
        __import_linesfile(conn, filepath, mid)
    else:
        print "Invalid import file. EXTENTION must be: '.cat' , '.sp', '.lines'"


def __import_catfile(conn, filepath, mid):
    """
    Inheritently Private Function, imports catfile to database
    Adds new molecule entry and its respective peaks
    Cancels action if molecule entry already exists (i.e. name && category)
    :param conn: Database connection
    :param filepath: Path to import file
    :param mid: Molecule ID
    :return:
    """

    # Store peak data from file, to 'peaks' table
    # Uses associative 'mid' for entry's foreign key
    with open(filepath) as f:
        for line in f:
            point = str.split((line.strip()))
            freq = float(point[0])                         # get frequency
            inte = abs(float(point[2])) ** float(point[2]) # get actual intensity (logx ^ x)
            conn.execute('INSERT INTO peaks(mid, frequency, intensity) VALUES (?,?,?)',(mid, freq, inte))   # insert into peak table

    # Commit Changes
    conn.commit()

    print "[ Added entry peaks ] "



def __import_spfile(conn, filepath, mid):
    """
    Inheritently Private Function, imports .sp File to database
    :param conn: Database connection
    :param filepath: Path to import file
    :param mid: Molecule ID
    :return:
    """
    # Store peak data in file, to 'peaks' table
    with open(filepath) as f:
        for line in f:
            point = str.split((line.strip()))
            freq = float(point[0])      # get frequency
            inte = float(point[1])      # get actual intensity (logx ^ x)
            conn.execute('INSERT INTO peaks(mid, frequency, intensity) VALUES (?,?,?)',(mid, freq, inte))   # insert into peak table

    # Commit Changes
    conn.commit()

    print "[ Added entry peaks ] "



def __import_linesfile(conn, filepath, mid):
    """
    Inheritently Private Function, imports .lines file to spectrum database
    :param conn: Database connection
    :param filepath: Path to import file
    :param mid: Molecule ID
    :return:
    """

def __checkfile(filepath):
    """
    Determines if a file can be opened / is a valid file.
    :param filepath: Filepath/name
    :return: True if file can be opened. False if cannot.
    """
    try:
        myfile = open(filepath)
    except IOError:
        print "Could not open file!"
        return False

    return True