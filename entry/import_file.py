import sqlite3
from config import *

def import_file(filename, name, category):
    """
    Imports file to spectrum database.
    :param filename: Filepath name. (.cat, .sp, .lines format)
    :param name: Name of molecule
    :param type: Type of data (known, experiment)
    :param info: String, info on molecule
    :return: None
    """

    # Check if file can be opened
    if __checkfile(filename) is False:
        return

    # Get File extention
    extention = str.split(filename, ".")[1]

    # Match extention to its appropriate import function
    if extention == 'cat':
        __import_catfile(filename, name, category)
    elif extention == 'sp':
        __import_spfile(filename, name, category)
    elif extention == 'lines':
        __import_linesfile(filename, name, category)
    else:
        print "Invalid import file. TYPE: '.cat' , '.sp', '.lines"


def __import_catfile(filename, name, category):
    """
    Inheritently Private Function, imports catfile to database
    Adds new molecule entry and its respective peaks
    Cancels action if molecule entry already exists (i.e. name && category)
    :param filename:
    :param name:
    :param category:
    :return:
    """
    # Connect to Database, create cursor
    conn = sqlite3.connect(db_filepath)
    cursor = conn.cursor()

    # Check if molecule exists
    cursor = conn.execute("SELECT * FROM molecules WHERE name=? AND category=?", (name,category))
    if cursor.fetchone() is None:
        # Exists throws error. Return.
        print "[ ERROR: Molecule entry already exists. Cancelling action. ]"
        return

    # Does not exist.
    # Add new entry to molecule table
    conn.execute('INSERT INTO molecules (name, category) VALUES (?,?)', (name, category))
    print "[ Added entry: " + name + " to molecules ]"

    # Get the new entry's molecule id (mid)
    cursor = conn.execute('SELECT max(mid) FROM molecules')
    mid = cursor.fetchone()[0]


    # Store peak data in file, to 'peaks' table
    # Uses associative 'mid' for entry's foreign key
    with open(filename) as f:
        for line in f:
            point = str.split((line.strip()))
            freq = float(point[0])                         # get frequency
            inte = abs(float(point[2])) ** float(point[2]) # get actual intensity (logx ^ x)
            conn.execute('INSERT INTO peaks(mid, frequency, intensity) VALUES (?,?,?)',(mid, freq, inte))   # insert into peak table

    print "[ Added entry peaks ] "

    # Commit Changes
    conn.commit()

def __import_spfile(filename, name, category, info):
    """
    Inheritently Private Function, imports .sp File to database
    :param filename:
    :param name:
    :param category:
    :param info:
    :return:
    """
    # Connect to Database, create cursonr
    conn = sqlite3.connect(db_filepath)
    cursor = conn.cursor()

    # Add Name, category and Info to molecule table
    conn.execute('INSERT INTO molecules (name, category) VALUES (?,?)', (name, category))
    print "[ Added entry: " + name + " to molecules ]"

    cursor = conn.execute('SELECT max(mid) FROM molecules')
    mid = cursor.fetchone()[0]  # get the inserted molecule id (mid)

    # Store peak data in file, to 'peaks' table
    with open(filename) as f:
        for line in f:
            point = str.split((line.strip()))
            freq = float(point[0])      # get frequency
            inte = float(point[1])      # get actual intensity (logx ^ x)
            conn.execute('INSERT INTO peaks(mid, frequency, intensity) VALUES (?,?,?)',(mid, freq, inte))   # insert into peak table

    print "[ Added entry peaks ] "

    # Commit Changes
    conn.commit()


def __import_linesfile(filename, name, category):
    """
    Inheritently Private Function, imports .lines file to spectrum database
    :param filename:
    :param name:
    :param category:
    :return:
    """

def __checkfile(filename):
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

