# Author: Jasmine Oliveira
# Date: 06/28/2016
# molecule_entry:
#       Module that creates molecule table entries, and gets entry information:
#       Functions:
#                   * new_molecule_entry(conn, name, category):
#                   * mid_exists(conn, mid)
#                   * get_mid(conn, name, category):
#

def new_molecule_entry(conn, name, category):
    """
    Adds a new molecule entry to molecule table
    If molecule already exists, returns null
    :param conn: Sqlite3 database connection
    :param name: Name of molecule
    :param category: Category of molecule
    :return mid: molecule id of new entry
    :return mid: None if already exists
    """

    mid = get_mid(conn, name, category)    # Get mid

    # If entry already exists, return that mid.
    if mid is not None:
        # Entry exists
        print "[ ERROR: Molecule entry already exists. Cancelling action. ]"
        return

    # If entry does not exist.
    # Add new entry to molecule table
    conn.execute('INSERT INTO molecules (name, category) VALUES (?,?)', (name, category))
    print "[ Added entry: " + name + " to molecules ]"

    # Get the new entry's molecule id (mid)
    cursor = conn.execute('SELECT max(mid) FROM molecules')
    mid = cursor.fetchone()[0]

    # Commit Changes
    conn.commit()

    return mid

def get_mid(conn, name, category):
    """
    Retreives molecule id (mid) from molecule table
    :param conn: Sqlite connection
    :param name: Name of molecule
    :param category: Category of molecule entry
    :return: mid: if molecule exists OR None: if molecule does not exist
    """
    cursor = conn.execute("SELECT * FROM molecules WHERE name=? AND category=?", (name,category))
    row = cursor.fetchone()

    if row is None:
        # Molecule entry does not exist.
        return None

    # Molecule entry exists
    return row[0]   # return mid

def mid_exists(conn, mid):
    """
    Determines if molecule entry is in the database (based on mid)
    :param conn: Sqlite connection
    :param cursor: Connection cursor
    :param mid: Molecule entry id (mid)
    :return: True if molecule exists. False if molecule does not exist.
    """
    # Select row with mid
    cursor = conn.execute("SELECT * FROM molecules WHERE mid=?", (mid,))
    row = cursor.fetchone()

    if row is None:
        # Molecule entry does not exist.
        return False

    # Molecule entry exists
    return True