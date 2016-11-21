# -----------------------------------------------------------------------------
# Author: Jasmine Oliveira
# Date:   11/18/2016
# -----------------------------------------------------------------------------
# knowninfo_table.py
# -----------------------------------------------------------------------------
# Module designed as a SQLite API to get, manipulate, and enter data of
# the KnownInfo table in the SPECdata database system.
#
#       Peaks table entries have the following format:
#           -> kid           (int:   id of the info table entry)
#           -> mid           (int:   id of the associated molecules row)
#           -> units         (string: frequency units (i.e [MHz, cm-1])
#           -> temperature   (float: temperature of associated data)
#           -> composition   (string: composition of the molecule (i.e C2H2)
#           -> isotope       (bool: is an isotope)
#           -> vibrational   (vibration: is vibrational)
#           -> notes         (string: additional information)
#
#       Public Functions:
#           * get_eid(conn, name, category)
#           * get_type(conn, mid)
#           * get_units(conn, mid)
#           * get_composition(conn, mid)
#

# Imports
from molecules_table import mid_exists


###############################################################################
# Get KnownInfo Entry Information
# -----------------------------------------------------------------------------
# Public Functions:
#       * get_eid(conn, name, category)
#       * get_units(conn, mid)
#       * get_composition(conn, mid)
###############################################################################

def get_kid(conn, mid):
    cursor = conn.execute("SELECT kid FROM KnownInfo WHERE mid=?",(mid,))
    line = cursor.fetchone()
    row = line[0]
    return row


def get_units(conn, mid):
    cursor = conn.execute("SELECT units FROM KnownInfo WHERE mid=?",(mid,))
    line = cursor.fetchone()
    row = line[0]
    return row


def get_composition(conn, mid):
    cursor = conn.execute("SELECT composition FROM KnownInfo WHERE mid=?",(mid,))
    line = cursor.fetchone()
    row = line[0]
    return row


def get_temperature(conn, mid):
    cursor = conn.execute("SELECT temperature FROM KnownInfo WHERE mid=?",(mid,))
    line = cursor.fetchone()
    row = line[0]
    return row


def get_notes(conn, mid):
    cursor = conn.execute("SELECT notes FROM KnownInfo WHERE mid=?",(mid,))
    line = cursor.fetchone()
    row = line[0]
    return row


def is_vibrational(conn,mid):
    cursor = conn.execute("SELECT vibration FROM KnownInfo WHERE mid=?",(mid,))
    line = cursor.fetchone()
    row = line[0]
    return row


def is_isotype(conn,mid):
    cursor = conn.execute("SELECT isotope FROM KnownInfo WHERE mid=?",(mid,))
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
    cursor = conn.execute("SELECT * FROM KnownInfo WHERE mid=?", (mid,))
    row = cursor.fetchone()

    if row is None:
        # Molecule entry does not exist.
        return False

    # Molecule entry exists
    return True


###############################################################################
# Update KnownInfo Table
# -----------------------------------------------------------------------------
# Update a table entry's specific row value
# Public Functions:
#       * update_temperature(conn, mid, temperature)
#       * update_isotope(conn, mid, bool)
#       * update_vibrational(conn, mid, bool)
#       * update_units(conn, mid, units)
#       * update_composition(conn, mid, composition)
#       * update_notes(conn, mid, notes)
###############################################################################


def update_temperature(conn, mid, temperature):
    """
    Changes the category row of a molecule
    :param conn: Connection to sqlite database
    :param mid: Molecule ID (mid) to make changes
    :param temperature: New type to replace
    :return: True, if updated successfully
    :return: False, if
    """

    if info_exists(conn, mid) is False:
        print "[ ERROR: KnownInfo entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE KnownInfo SET temperature={c} WHERE mid={m}".format(c=temperature, m=mid))
    conn.commit()
    return True


def update_isotope(conn, mid, bool):
    """
    Changes the category row of a molecule
    :param conn: Connection to sqlite database
    :param mid: Molecule ID (mid) to make changes
    :param bool: New type to replace
    :return: True, if updated successfully
    :return: False, if
    """
    if bool is not True or False:
        return False

    if info_exists(conn, mid) is False:
        print "[ ERROR: KnownInfo entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE KnownInfo SET isotope={c} WHERE mid={m}".format(c=bool, m=mid))
    conn.commit()
    return True


def update_vibrational(conn, mid, bool):
    """
    Changes the category row of a molecule
    :param conn: Connection to sqlite database
    :param mid: Molecule ID (mid) to make changes
    :param bool: New type to replace
    :return: True, if updated successfully
    :return: False, if
    """
    if bool is not True or False:
        return False

    if info_exists(conn, mid) is False:
        print "[ ERROR: KnownInfo entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE KnownInfo SET vibrational={c} WHERE mid={m}".format(c=bool, m=mid))
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
        print "[ ERROR: KnownInfo entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE KnownInfo SET units={c} WHERE mid={m}".format(c=units, m=mid))
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
        print "[ ERROR: KnownInfo entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE KnownInfo SET composition={c} WHERE mid={m}".format(c=composition, m=mid))
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
        print "[ ERROR: KnownInfo entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE KnownInfo SET notes={c} WHERE mid={m}".format(c=notes, m=mid))
    conn.commit()
    return True


###############################################################################
# Insert KnownInfo Table Entry
# -----------------------------------------------------------------------------
# Inserts a new row entry into the KnownInfo table
# Public Functions:
#       * new_entry(conn, mid, units, temperature, composition, isotope, vibrational, notes)
###############################################################################

def new_entry(conn, mid, units, temperature, composition, isotope, vibrational, notes):
    """
    Adds a new entry to the KnownInfo table
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
        return "[ ERROR: KnownInfo entry associated already exists. Cancelling action. ]"

    # If entry does not exist.
    # Add new entry to table
    conn.execute('INSERT INTO KnownInfo (mid, units, temperature, composition, isotope, vibrational, notes)'
                 ' VALUES (?,?,?,?,?,?,?)', (mid, units, temperature, composition, isotope, vibrational, notes))

    print "[ Added info entry: " + mid + " to molecules ]"

    # Get the new entry's id (iid)
    cursor = conn.execute('SELECT max(kid) FROM KnownInfo')
    kid = cursor.fetchone()[0]

    # Commit Changes
    conn.commit()

    return kid


##############################################################################
# Remove KnownInfo Table Entry
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
        return "[ ERROR: KnownInfo entry does not exist. Cancelling action. ]"


    # Delete Info Entry
    conn.execute("DELETE FROM KnownInfo WHERE mid={m}".format(m=mid))
    conn.commit()

    print "[ Successfully removed from database ]"
    return True
