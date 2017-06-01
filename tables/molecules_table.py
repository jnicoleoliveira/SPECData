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
    cursor = conn.execute("SELECT mid FROM molecules WHERE category='known'"
                          " OR category='artifact'")
    rows = cursor.fetchall()

    mids = []
    for row in rows:
        mids.append(row[0])

    return mids


def get_mids_where_category_in(conn, category):
    """

    :param conn:
    :param category:
    :return:
    """

    # Select rows with mid
    query = "SELECT mid, name FROM molecules WHERE category IN " + get_in_string(category)
    cursor = conn.execute(query)
    rows = cursor.fetchall()

    mids = []
    for row in rows:
        mids.append(row[0])

    return mids


def get_mids_where_units_in(conn, units, category=None):

    in_units = "WHERE UNITS IN " + get_in_string(units)
    known_query = "SELECT M.mid FROM molecules AS M JOIN KnownInfo AS K ON M.mid=K.mid " + in_units
    experiment_query = "SELECT M.mid FROM molecules AS M JOIN ExperimentInfo AS E ON M.mid=E.mid " + in_units

    if category is None:
        query = known_query + " UNION " + experiment_query
    elif category is 'known':
        query = known_query
    else:
        query = experiment_query

    cursor = conn.execute(query)
    rows = cursor.fetchall()

    mids = []
    for row in rows:
        mids.append(row[0])

    return mids


def get_mids_in_temperature_range(conn, min, max):

    if min is not None and max is None:
        string = " WHERE temperature >= " + str(min)
    elif max is not None and min is None:
        string = " WHERE temperature <=" + str(max)
    elif max is not None and min is not None:
        string = " WHERE temperature >= " + str(min) + " AND temperature <= " + str(max)
    else:
        string = ""

    query = "SELECT M.mid FROM molecules M JOIN KnownInfo K ON M.mid=K.mid" + string
    # print query
    cursor = conn.execute(query)
    rows = cursor.fetchall()

    mids = []
    for row in rows:
        mids.append(row[0])

    return mids


def get_mids_where_types_in(conn, types):

    query = "SELECT M.mid FROM molecules M JOIN ExperimentInfo E ON M.mid=E.mid" \
            " WHERE type IN " + get_in_string(types)

    cursor = conn.execute(query)
    rows = cursor.fetchall()

    mids = []
    for row in rows:
        mids.append(row[0])

    return mids


def get_mids_where_is_isotope(conn, bool):

    bool = 1 if bool is True else 0

    # Select rows with mid
    query = "SELECT M.mid FROM molecules M JOIN KnownInfo K ON M.mid=K.mid WHERE isotope IS " + str(bool)
    cursor = conn.execute(query)
    rows = cursor.fetchall()

    mids = []
    for row in rows:
        mids.append(row[0])

    return mids


def get_mids_where_is_vibrational(conn, bool):

    bool = 1 if bool is True else 0

    # Select rows with mid
    query = "SELECT M.mid FROM molecules M JOIN KnownInfo K ON M.mid=K.mid WHERE vibrational IS " + str(bool)
    cursor = conn.execute(query)
    rows = cursor.fetchall()

    mids = []
    for row in rows:
        mids.append(row[0])

    return mids


def get_in_string(array):
    """
    Returns a string of the array in the format (a1, a2, a3 .. an)
    :param array: array of elements
    :return:
    """

    if array is None or len(array) is 0:
        return None

    string = "("
    for i in range(0, len(array)-1):
        string += "'" + str(array[i]) + "', "

    string += "'" + str(array[len(array)-1]) + "')"

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

def name_exists(conn, name):
    """
    Determines if molecule entry is in the database (based on mid)
    :param conn: Sqlite connection
    :param cursor: Connection cursor
    :param mid: Molecule entry id (mid)
    :return: True if molecule exists. False if molecule does not exist.
    """
    # Select row with mid
    cursor = conn.execute("SELECT * FROM molecules WHERE name=?", (name,))
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

    conn.execute("UPDATE molecules SET category='{c}' WHERE mid={m}".format(c=category, m=mid))
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

    print "UPDATE molecules SET name={n} WHERE mid={m}".format(n=name, m=mid)
    conn.execute("UPDATE molecules SET name='{n}' WHERE mid={m}".format(n=name, m=mid))
    conn.commit()
    return True


def update(conn, mid, row, value):
    print "CHANGE:" + str(mid) + " " + str(row) + "  " + str(value)

    if row == 'name':
        update_name(conn, mid, value)  # update molecules.name
        return

    if row == 'category':
        update_category(conn, mid, value)  # update molecules.category
        return

    if get_category(conn, mid) == 'experiment':
        update_experiment(conn, mid, row, value)
        return

    update_known(conn, mid, row, value)


def update_experiment(conn, mid, row, value):
    if row == 'last_updated':
        from experimentinfo_table import update_last_updated
        update_last_updated(conn, mid)
    else:
        from experimentinfo_table import update as u
        u(conn, mid, row, value)


def update_known(conn, mid, row, value):
    if row == 'last_updated':
        from knowninfo_table import update_last_updated
        update_last_updated(conn, mid)
    else:
        from knowninfo_table import update as u
        u(conn, mid, row, value)


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
    from assignments_table import remove_all as del_assignment
    from affirmedassignment_table import remove_all as del_affirmed
    if(mid_exists(conn, mid) is False):
        print "[ ERROR: Molecule entry does not exist. Cancelling action! ]"
        return False

    info_table_name = 'ExperimentInfo' if get_category(conn,mid) is 'experiment' else 'KnownInfo'

    # Delete Info Entry
    conn.execute("DELETE FROM {i} WHERE mid={m}".format(i=info_table_name, m=mid))
    # Delete Assignment Entry
    del_assignment(conn, mid)
    # Delete AffirmedAssignment Entry
    del_affirmed(conn, mid)
    # Delete peak entry
    conn.execute("DELETE FROM peaks WHERE mid={m}".format(m=mid))
    # Delete Molecule entry
    conn.execute("DELETE FROM molecules WHERE mid={m}".format(m=mid))

    conn.commit()

    print "[ Successfully removed " + str(mid) + "from database ]"
    return True