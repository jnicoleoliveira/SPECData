# -----------------------------------------------------------------------------
# Author: Jasmine Oliveira
# Date:   11/18/2016
# -----------------------------------------------------------------------------
# artifactinfo.py
# -----------------------------------------------------------------------------
# Module designed as a SQLite API to get, manipulate, and enter data of
# the ArtifactInfo table in the SPECdata database system.
#
#       ArtifactInfo table entries have the following format:
#           -> rid           (int:   id of the info table entry)
#           -> mid           (int:   id of the associated molecules row)
#           -> notes         (string: additional information)
#
#       Public Functions:
#           * get_rid(conn, name, category)
#           * get_units(conn, mid)
#           * get_notes(conn, mid)
#           * info_exists(conn, mid)
#           * update_units(conn, mid, units)
#           * update_notes(conn, mid, notes)
#           * new_entry(conn, mid, units, notes)
#           * remove_entry(conn, mid)
#

# Imports
from molecules_table import mid_exists


###############################################################################
# Get ArtifactInfo Entry Information
# -----------------------------------------------------------------------------
# Public Functions:
#       * get_rid(conn, name, category)
#       * get_units(conn, mid)
#       * get_notes(conn, mid)
#       * info_exists(conn, mid)
###############################################################################

def get_rid(conn, mid):
    cursor = conn.execute("SELECT rid FROM ArtifactInfo WHERE mid=?",(mid,))
    line = cursor.fetchone()
    row = line[0]
    return row


def get_units(conn, mid):
    cursor = conn.execute("SELECT units FROM ArtifactInfo WHERE mid=?",(mid,))
    line = cursor.fetchone()
    row = line[0]
    return row


def get_notes(conn, mid):
    cursor = conn.execute("SELECT notes FROM ArtifactInfo WHERE mid=?",(mid,))
    line = cursor.fetchone()
    row = line[0]
    return row


def info_exists(conn, mid):
    """
    Determines if molecule entry is in the database (based on mid)
    :param conn: Sqlite connection
    :param cursor: Connection cursor
    :param mid: Molecule entry id (mid)
    :return: True if molecule exists. False if molecule does not exist.
    """
    # Select row with mid
    cursor = conn.execute("SELECT * FROM ArtifactInfo WHERE mid=?", (mid,))
    row = cursor.fetchone()

    if row is None:
        # Molecule entry does not exist.
        return False

    # Molecule entry exists
    return True


###############################################################################
# Update ArtifactInfo Table
# -----------------------------------------------------------------------------
# Update a table entry's specific row value
# Public Functions:
#       * update_units(conn, mid, units)
#       * update_notes(conn, mid, notes)
###############################################################################


def update_units(conn, mid, units):
    """
    Changes the category row of a molecule
    :param conn: Connection to sqlite database
    :param mid: Molecule ID (mid) to make changes
    :param units: New type to replace
    :return: True, if updated successfully
    :return: False, if
    """

    if info_exists(conn, mid) is False:
        print "[ ERROR: ArtifactInfo entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE ArtifactInfo SET units={c} WHERE mid={m}".format(c=units, m=mid))
    conn.commit()
    return True


def update_notes(conn, mid, notes):
    """
    Changes the category row of a molecule
    :param conn: Connection to sqlite database
    :param mid: Molecule ID (mid) to make changes
    :param notes: New type to replace
    :return: True, if updated successfully
    :return: False, if
    """

    if info_exists(conn, mid) is False:
        print "[ ERROR: ArtifactInfo entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE ArtifactInfo SET notes={c} WHERE mid={m}".format(c=notes, m=mid))
    conn.commit()
    return True


###############################################################################
# Insert ArtifactInfo Table Entry
# -----------------------------------------------------------------------------
# Inserts a new row entry into the ArtifactInfo table
# Public Functions:
#       * new_entry(conn, mid, units, notes):
###############################################################################

def new_entry(conn, mid, units, notes):
    """
    Adds a new entry to the ArtifactInfo table
    If molecule already exists, returns null
    :param conn: Sqlite3 database connection
    :param mid: Molecule id of the associated molecule
    :param type:  type of experiment
    :param units: frequency units (i.e [MHz, cm-1]
    :param composition: composition of the molecule (i.e C2H2)
    :param notes: additional information
    :return:
    """

    if mid_exists(conn, mid) is False:
        return "[ERROR: Molecule entry does not exist!"
    elif info_exists(conn, mid) is True:
        # If entry already exists, return that mid.
        return "[ ERROR: ArtifactInfo entry associated already exists. Cancelling action. ]"

    # If entry does not exist.
    # Add new entry to table
    conn.execute('INSERT INTO ArtifactInfo (mid, units, notes)'
                 ' VALUES (?,?,?)', (mid, units, notes))

    print "[ Added info entry: " + mid + " to molecules ]"

    # Get the new entry's id (iid)
    cursor = conn.execute('SELECT max(kid) FROM ArtifactInfo')
    kid = cursor.fetchone()[0]

    # Commit Changes
    conn.commit()

    return kid


##############################################################################
# Remove ArtifactInfo Table Entry
# -----------------------------------------------------------------------------
# Removes a new row entry from the molecules table
# Public Functions:
#       * remove_entry(conn, mid)
###############################################################################


def remove_entry(conn, mid):
    """
    Removes entry in ArtifactInfo table with associated mid
    :param conn: Sqlite database connection
    :param mid: Molecule ID (mid) of molecule to be removed
    :return: True if successfully removed
    :return: False, if not removed
    """

    if info_exists(conn, mid) is False:
        # If entry already exists, return that mid.
        return "[ ERROR: ArtifactInfo entry does not exist. Cancelling action. ]"


    # Delete Info Entry
    conn.execute("DELETE FROM ArtifactInfo WHERE mid={m}".format(m=mid))
    conn.commit()

    print "[ Successfully removed from database ]"
    return True
