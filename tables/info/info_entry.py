# Author: Jasmine Oliveira
# Date: 07/01/2016

from tables.molecules.molecules_entry import mid_exists

def new_info_entry(conn, mid, vibration, notes):
    """
    Adds a new info entry to info table
    Associative molecule entry must exist, and it's info entry must not.
    :param conn: Connection to sqlite3 database
    :param mid: Molecule ID (mid) for the associate info entry
    :param vibration: Vibration of molecule
    :param notes: Notes regarding the molecule
    :return: Info entry id (iid) of new entry
    :return None if info entry already exists or molecule entry does not exist
    """

    # Check if molecule entry exists
    if mid_exists(conn, mid) is False:
        # Molecule does not exist, ERR return
        print "[ ERROR: Molecule entry does not exist.]"
        return #none

    iid = get_iid(conn, mid)    # Get iid
    # If entry already exists, return that mid.
    if iid is not None:
        # Entry exists
        print "[ ERROR: Info entry already exists.]"
        return #none


    # If entry does not exist.
    # Add new entry to info table
    conn.execute('INSERT INTO info (mid, vibration, notes) VALUES (?,?,?)', (mid, vibration, notes))

    # Get the new entry's info id (iid)
    cursor = conn.execute('SELECT max(mid) FROM info')
    iid = cursor.fetchone()[0]
    print "[ Added entry: iid:" + str(iid) + " to info ]"

    # Commit Changes
    conn.commit()

    return iid

def get_iid(conn, mid):
    """
    Retreives info entry id (iid) from info table
    :param conn: Connection to sqlite3 database
    :param mid: Molecule ID (mid) of the associated info entry
    :return: Info entry id (iid)
    :return: None, if entry is not found
    """
    cursor = conn.execute("SELECT iid FROM info WHERE mid=?", (mid,))
    row = cursor.fetchone()

    if row is None:
        # Info entry does not exist.
        return None

    # Info entry exists
    return row[0]   # return iid

def iid_exists(conn, iid):
    """
    Determines if info entry is in the database (based on iid)
    :param conn: Sqlite3 database connection
    :param iid: Info entry id (mid)
    :return: True if info entry exists. False if entry does not exist.
    """
    # Select row with mid
    cursor = conn.execute("SELECT * FROM info WHERE iid=?", (iid,))
    row = cursor.fetchone()

    if row is None:
        # Info entry does not exist.
        return False

    # Info entry exists
    return True