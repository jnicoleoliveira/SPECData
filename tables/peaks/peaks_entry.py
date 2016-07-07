# Author: Jasmine Oliveira
# Date: 06/27/2016
# info_entry:
#       Module that creates peak table entries
#       Public Functions:
#                   * import_file(conn, filepath, mid)
#                   * pid_exists(conn, pid)
#       Private/Helper Functions:
#                   * __checkfile(filepath)
#                   * __import_catfile(conn, filepath, mid)
#                   * __import_spfile(conn, filepath, mid)
#                   * __import_linesfile(conn, filepath, mid)


import sqlite3
from tables.molecules.molecules_entry import mid_exists

def import_file(conn, filepath, mid):
    """
    Imports file to peak table in spectrum database to it's associative molecule
    Molecule must exist for import
    Supports '.cat' , '.sp', '.lines' files.
    :param filepath: Path to import file
    :param mid: Molecule ID
    :return:
    """

    # Check if molecule entry exists
    if mid_exists(conn, mid) is False:
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


def pid_exists(conn, pid):
    """
    Determines if peaks entry is in the database (based on pid)
    :param conn: Sqlite3 database connection
    :param pid: Peak entry id (mid)
    :return: True if peak entry exists. False if entry does not exist.
    """
    # Select row with mid
    cursor = conn.execute("SELECT * FROM peaks WHERE pid=?", (pid,))
    row = cursor.fetchone()

    if row is None:
        # Info entry does not exist.
        return False

    # Info entry exists
    return True


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
    linenum = 0
    with open(filepath) as f:
        for line in f:
            linenum +=1
            try:
                point = str.split((line.strip()))
                freq = float(point[0])                         # get frequency
                inte = abs(float(point[2])) ** float(point[2]) # get actual intensity (logx ^ x)
                conn.execute('INSERT INTO peaks(mid, frequency, intensity) VALUES (?,?,?)',(mid, freq, inte))  # insert into peak table
            except IndexError:
                print "Error in line: " + str(linenum)

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
