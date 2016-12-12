# -----------------------------------------------------------------------------
# Author: Jasmine Oliveira
# Date:   11/18/2016 (Refactored API)
# -----------------------------------------------------------------------------
# molecules_table.py:
# -----------------------------------------------------------------------------
# Module designed as a SQLite API to get, manipulate, and enter data of
# the molecules table in the SPECdata database system.
#
#       Molecules table entries have the following format:
#           -> mid      (int:    id of the molecules table entry)
#           -> name     (string: name of molecule)
#           -> category (string: category of the molecule (experiment, known, artifact)
#           -> date     (text:   last date peaks information updated)
#
#       Public Functions:
#           [Table Information]
#               * get_experiment_list(conn)
#               * get_mid_list(conn)
#           [Entry Information]
#               * get_mid(conn, name, category)
#               * get_name(conn, mid)
#               * mid_exists(conn, mid)
#           [Update Entry]
#               * update_category(conn, mid, category)
#               * update_name(conn, mid, name)
#               * update_date(conn, mid, date)
#           [Insert Entry]
#               * new_molecule_entry(conn, name, category)
#           [Remove Entry]
#               * remove_molecule(conn, mid)
#
#       Private Functions:
#               - None
# -----------------------------------------------------------------------------


###############################################################################
# Get Molecules Table Information
# -----------------------------------------------------------------------------
# Date: 07/01/2016
# -----------------------------------------------------------------------------
# Get data from the molecule table
# Public Functions:
#       * get_experiment_list(conn)
#       * get_mid_list(conn)
###############################################################################

def get_experiment_list(conn):
    """
    Gets list of experiment mids (molecule entries whose category is
    'experiment') in the specified database
    :param conn: Sqlite connection to spectrum database
    :return: list of mids (ints)
    """
    # Select row with mid
    cursor = conn.execute("SELECT mid, name FROM molecules WHERE category='experiment'")
    rows = cursor.fetchall()

    mids = []
    names = []
    for row in rows:
        mids.append(row[0])
        names.append(row[1])

    return mids, names

def get_all_mid_list(conn):
    """
    Gets list of all mids in the specified database
    :param conn: Sqlite connection to spectrum database
    :return: list of mids (ints)
    """
    # Select row with mid
    cursor = conn.execute("SELECT mid FROM molecules")
    rows = cursor.fetchall()

    mids = []
    for row in rows:
        mids.append(row[0])

    return mids

def get_mid_list(conn):
    """
    Gets list of all mids in the specified database
    :param conn: Sqlite connection to spectrum database
    :return: list of mids (ints)
    """
    # Select row with mid
    cursor = conn.execute("SELECT mid, name FROM molecules WHERE category='known'"
                          " OR category='artifact'")
    rows = cursor.fetchall()

    mids = []
    for row in rows:
        mids.append(row[0])

    return mids


def get_molecules_where(conn, category, units=None, min_temp=None, max_temp=None, composition=None,  isotope=None, vibrational=None, type=None,):
    """
    Gets list of all
    """

    query = ""
    info_table = "ExperimentInfo"

    ''' Filter by Molecule '''
    if category is None:
        query = "SELECT mid FROM molecules"
    else:
        query = "SELECT mid FROM molecules WHERE category IN" + get_in_string(category)

    ''' Filter by KnownInfo '''
    if ("known" in category or "artifact" in category) and \
            len(filter(None, [units, min_temp, max_temp, composition, isotope, vibrational])) is not 0:

        query = "SELECT A.mid FROM (" + query + ") as A JOIN KnownInfo" \
                + " as B ON A.mid = B.mid WHERE "

        strings = []

        if units is not None:
            s = "units IN " + get_in_string(units)
            strings.append(s)

        if min_temp is not None:
            s = "temperature >= " + str(min_temp)
            strings.append(s)

        if max_temp is not None:
            s = "temperature <= " + str(max_temp)
            strings.append(s)

        if isotope is not None:
            s = "isotope = " + str(isotope)
            strings.append(s)

        if vibrational is not None:
            s = "vibrational = " + str(vibrational)
            strings.append(s)

        for i in range(0, len(strings)-1):
            query += strings[i] + " AND "

        query += strings[len(strings)-1]

    ''' Filter by Experiment '''
    if ("experiment" in category) and \
        len(filter(None, [units, type, composition])) is not 0:

        query = "SELECT A.mid FROM (" + query + ") as A JOIN ExperimentInfo" \
                + " as B ON A.mid = B.mid WHERE "

        strings = []

        if units is not None:
            s = "units IN " + get_in_string(units)
            strings.append(s)

        if type is not None:
            s = "type IN " + get_in_string(type)
            strings.append(s)

        for i in range(0, len(strings)-1):
            query += strings[i] + " AND "

        query += strings[len(strings)-1]

    print query
    cursor = conn.execute(query)

    mids = []
    rows = cursor.fetchall()
    for row in rows:
        mids.append(row[0])

    return mids

def get_in_string(array):
    string = "("
    for i in range(0, len(array)-1):
        string += "'" + array[i] + "', "

    string += "'" + array[len(array)-1] + "')"

    return string

###############################################################################
# Get Molecules Entry Information
# -----------------------------------------------------------------------------
# Date: 06/28/2016
# -----------------------------------------------------------------------------
# Public Functions:
#       * get_mid(conn, name, category)
#       * get_name(conn, mid)
#       * mid_exists(conn, mid)
###############################################################################


def get_mid(conn, name, category):
    """
    Retreives molecule id (mid) from molecule table
    :param conn: Sqlite connection
    :param name: Name of molecule
    :param category: Category of molecule entry
    :return: mid: if molecule exists OR None: if molecule does not exist
    """
    cursor = conn.execute("SELECT * FROM molecules WHERE name=? AND category=?", (name, category))
    row = cursor.fetchone()

    if row is None:
        # Molecule entry does not exist.
        return None

    # Molecule entry exists
    return row[0]   # return mid


def get_name(conn, mid):
    cursor = conn.execute("SELECT name FROM molecules WHERE mid=?",(mid,))
    line = cursor.fetchone()
    name = line[0]
    return name


def get_category(conn, mid):
    cursor = conn.execute("SELECT category FROM molecules WHERE mid=?",(mid,))
    line = cursor.fetchone()
    name = line[0]
    return name

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


###############################################################################
# Update Molecules Table
# -----------------------------------------------------------------------------
# Date: 07/01/2016
# -----------------------------------------------------------------------------
# Update a table entry's specific row value
# Public Functions:
#       * update_category(conn, mid, category)
#       * update_name(conn, mid, name)
#       * update_date(conn, mid, date)
###############################################################################


def update_category(conn, mid, category):
    """
    Changes the category row of a molecule
    :param conn: Connection to sqlite database
    :param mid: Molecule ID (mid) to make changes
    :param category: New category to replace
    :return: True, if updated successfully
    :return: False, if
    """
    if(mid_exists(conn, mid) is False):
        print "[ ERROR: Molecule entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE molecules SET category={c} WHERE mid={m}".format(c=category, m=mid))
    conn.commit()
    return True


def update_name(conn, mid, name):
    """
    Changes the name row of a molecule
    :param conn: Connection to sqlite database
    :param mid: Molecule ID (mid) to make changes
    :param name: New name to replace
    :return: True, if updated successfully
    :return: False, if
    """
    if(mid_exists(conn, mid) is False):
        print "[ ERROR: Molecule entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE molecules SET name={n} WHERE mid={m}".format(n=name, m=mid))
    conn.commit()
    return True


###############################################################################
# Insert Molecule Table Entry
# -----------------------------------------------------------------------------
# Date: 06/28/2016
# -----------------------------------------------------------------------------
# Inserts a new row entry into the molecules table
# Public Functions:
#       * new_molecule_entry(conn, name, category):
###############################################################################

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


##############################################################################
# Remove Molecule Table Entry
# -----------------------------------------------------------------------------
# Date: 06/28/2016
# -----------------------------------------------------------------------------
# Removes a new row entry from the molecules table
# Public Functions:
#       * remove_molecule(conn, mid)
###############################################################################


def remove_molecule(conn, mid):
    """
    Removes all info, peak and molecule entries of given mid
    :param conn: Sqlite database connection
    :param mid: Molecule ID (mid) of molecule to be removed
    :return: True if successfully removed
    :return: False, if not removed
    """
    if(mid_exists(conn, mid) is False):
        print "[ ERROR: Molecule entry does not exist. Cancelling action! ]"
        return False

    # Delete Info Entry
    conn.execute("DELETE FROM info WHERE mid={m}".format(m=mid))
    # Delete peak entry
    conn.execute("DELETE FROM peaks WHERE mid={m}".format(m=mid))
    # Delete Molecule entry
    conn.execute("DELETE FROM molecules WHERE mid={m}".format(m=mid))

    conn.commit()

    print "[ Successfully removed " + str(mid) + "from database ]"
    return True