# -----------------------------------------------------------------------------
# Author: Jasmine Oliveira
# Date:   11/18/2016
# -----------------------------------------------------------------------------
# experimentinfo_table.py
# -----------------------------------------------------------------------------
# Module designed as a SQLite API to get, manipulate, and enter data of
# the ExperimentInfo table in the SPECdata database system.
#
#       Peaks table entries have the following format:
#           -> eid           (int:   id of the info table entry)
#           -> mid           (int:   id of the associated molecules row)
#           -> type          (string: type of experiment
#                               (i.e [discharge, heated nozzle, laser ablation, stable]))
#           -> units         (string: frequency units (i.e [MHz, cm-1])
#           -> composition   (string: composition of the molecule (i.e C2H2)
#           -> notes         (string: additional information)
#           -> line-shape    (..
#
#       Public Functions:
#           * get_eid(conn, name, category)
#           * get_type(conn, mid)
#           * get_units(conn, mid)
#           * get_composition(conn, mid)
#

###############################################################################
# Get ExperimentInfo Entry Information
# -----------------------------------------------------------------------------
# Date: 06/28/2016
# -----------------------------------------------------------------------------
# Public Functions:
#       * get_eid(conn, name, category)
#       * get_type(conn, mid)
#       * get_units(conn, mid)
#       * get_composition(conn, mid)
###############################################################################

from molecules_table import mid_exists


def get_eid(conn, mid):
    cursor = conn.execute("SELECT eid FROM ExperimentInfo WHERE mid=?",(mid,))
    line = cursor.fetchone()
    row = line[0]
    return row


def get_type(conn, mid):
    cursor = conn.execute("SELECT type FROM ExperimentInfo WHERE mid=?",(mid,))
    line = cursor.fetchone()
    row = line[0]
    return row


def get_units(conn, mid):
    cursor = conn.execute("SELECT units FROM ExperimentInfo WHERE mid=?",(mid,))
    line = cursor.fetchone()
    row = line[0]
    return row


def get_composition(conn, mid):
    cursor = conn.execute("SELECT composition FROM ExperimentInfo WHERE mid=?",(mid,))
    line = cursor.fetchone()
    row = line[0]
    return row


def get_notes(conn, mid):
    cursor = conn.execute("SELECT notes FROM ExperimentInfo WHERE mid=?",(mid,))
    line = cursor.fetchone()
    row = line[0]
    return row


def get_last_updated(conn, mid):
    cursor = conn.execute("SELECT last_updated FROM ExperimentInfo WHERE mid=?",(mid,))
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
    cursor = conn.execute("SELECT * FROM ExperimentInfo WHERE mid=?", (mid,))
    row = cursor.fetchone()

    if row is None:
        # Molecule entry does not exist.
        return False

    # Molecule entry exists
    return True


def get_info_list(conn, mid):
    """
    Returns a list of the information on a known entry
    In the order: kid, units, composition, temperature, notes, vibrational, isotope, last_updated
    :param conn:
    :param mid:
    :return:
    """
    cursor = conn.execute("SELECT eid, units, composition, type, notes, last_updated"
                          "last_updated FROM ExperimentInfo WHERE mid=?", (mid,))

    line = cursor.fetchone()
    row = line[0]
    return row

###############################################################################
# Update ExperimentInfo Table
# -----------------------------------------------------------------------------
# Date: 07/01/2016
# -----------------------------------------------------------------------------
# Update a table entry's specific row value
# Public Functions:
#       * update_type(conn, mid, type)
#       * update_name(conn, mid, name)
#       * update_date(conn, mid, date)
###############################################################################


def update(conn, mid, row, value):

    if info_exists(conn, mid) is False:
        print "[ ERROR: KnownInfo entry does not exist. Cancelling action! ]"
        return False
    print row
    conn.execute("UPDATE ExperimentInfo SET {r}='{v}' WHERE mid={m}".format(r=row, v=str(value), m=mid))
    conn.commit()

    return True


def update_type(conn, mid, type):
    """
    Changes the category row of a molecule
    :param conn: Connection to sqlite database
    :param mid: Molecule ID (mid) to make changes
    :param type: New type to replace
    :return: True, if updated successfully
    :return: False, if
    """
    if(info_exists(conn, mid) is False):
        print "[ ERROR: ExperimentInfo entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE ExperimentInfo SET type={c} WHERE mid={m}".format(c=type, m=mid))
    conn.commit()
    return True


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
        print "[ ERROR: ExperimentInfo entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE ExperimentInfo SET units={c} WHERE mid={m}".format(c=units, m=mid))
    conn.commit()
    return True


def update_composition(conn, mid, composition):
    """
    Changes the category row of a molecule
    :param conn: Connection to sqlite database
    :param mid: Molecule ID (mid) to make changes
    :param composition: New type to replace
    :return: True, if updated successfully
    :return: False, if
    """

    if info_exists(conn, mid) is False:
        print "[ ERROR: ExperimentInfo entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE ExperimentInfo SET composition={c} WHERE mid={m}".format(c=composition, m=mid))
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
        print "[ ERROR: ExperimentInfo entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE ExperimentInfo SET notes={c} WHERE mid={m}".format(c=notes, m=mid))
    conn.commit()
    return True


def update_last_updated(conn, mid):
    if info_exists(conn, mid) is False:
        print "[ ERROR: KnownInfo entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE ExperimentInfo SET last_updated=datetime('now', 'localtime') WHERE mid=?;", (mid,))
    conn.commit()
    return True


###############################################################################
# Insert ExperimentInfo Table Entry
# -----------------------------------------------------------------------------
# Date: 06/28/2016
# -----------------------------------------------------------------------------
# Inserts a new row entry into the ExperimentInfo table
# Public Functions:
#       * new_entry(conn, mid, type, units, composition, notes):
###############################################################################

def new_entry(conn, mid, type, units, composition, notes):
    """
    Adds a new entry to the ExperimentInfo table
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
        return "[ ERROR: ExperimentInfo entry associated already exists. Cancelling action. ]"

    # If entry does not exist.
    # Add new entry to table
    conn.execute('INSERT INTO ExperimentInfo (mid, type, units, composition, notes)'
                 ' VALUES (?,?,?,?,?)', (mid, type, units, composition, notes))

    print "[ Added info entry: " + mid + " to molecules ]"

    # Get the new entry's id (iid)
    cursor = conn.execute('SELECT max(eid) FROM ExperimentInfo')
    eid = cursor.fetchone()[0]

    # Commit Changes
    conn.commit()

    return eid

##############################################################################
# Remove ExperimentInfo Table Entry
# -----------------------------------------------------------------------------
# Date: 06/28/2016
# -----------------------------------------------------------------------------
# Removes a new row entry from the molecules table
# Public Functions:
#       * remove_entry(conn, mid)
###############################################################################


def remove_entry(conn, mid):
    """
    Removes all info, peak and molecule entries of given mid
    :param conn: Sqlite database connection
    :param mid: Molecule ID (mid) of molecule to be removed
    :return: True if successfully removed
    :return: False, if not removed
    """

    if info_exists(conn, mid) is False:
        # If entry already exists, return that mid.
        return "[ ERROR: ExperimentInfo entry does not exist. Cancelling action. ]"


    # Delete Info Entry
    conn.execute("DELETE FROM ExperimentInfo WHERE mid={m}".format(m=mid))
    conn.commit()

    print "[ Successfully removed from database ]"
    return True
