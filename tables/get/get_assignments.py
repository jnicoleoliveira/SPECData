def get_assigned_pid_list(conn, assigned_mid, mid=None):
    """
    Returns pid list of peaks assigned to a particular molecule
    :param conn: SQLite database connection
    :param assigned_mid: Assigned molecule ID (assigned_mid)(mid)
    :param mid: Molecule ID (mid) of experiment being assigned
    :return:
    """

    if(mid is None):
        # Get Assignments associated with the assigned_mid ( all )
        cursor = conn.execute("SELECT pid FROM assignments WHERE assigned_mid=?", (assigned_mid,))
        rows = cursor.fetchall()
    else:
        # Get Assignments associated with the assigned_mid, and mid ( only those associated with particular experiment )
        cursor = conn.execute("SELECT pid FROM assignments WHERE assigned_mid=? AND mid=?", (assigned_mid, mid))
        rows = cursor.fetchall()

    if rows is not None:
        pidlist = []
        for row in rows:
            pidlist.append(row[0])

        return pidlist

    return None


def aid_exists(conn, aid):
    """
    Determines if assignments entry is in the database (based on aid)
    :param conn: Sqlite connection
    :param cursor: Connection cursor
    :param mid: Assignments entry ID (aid)
    :return: True if assignment exists. False if assignment does not exist.
    """
    # Select row with mid
    cursor = conn.execute("SELECT * FROM assignments WHERE aid=?", (aid,))
    row = cursor.fetchone()

    if row is None:
        # Assignments entry does not exist.
        return False

    # Assignments entry exists
    return True


def has_assignments(conn, mid):
    """
    Determines if a molecule has assignments
    :param conn: SQLite Database conenction
    :param mid: Molecule ID (mid) of molecule to check
    :return: False, if there are no assignments. True, if there are assignments.
    """
    cursor = conn.execute("SELECT * FROM assignments WHERE mid=?",(mid,))
    row = cursor.fetchone()

    if row is None:
        # There are no assignments to this molecule
        return False

    # There are assignments to this molecule
    return True


def get_assigned_mids(conn, mid):
    """
    Returns list of assigned mids to a particular molecule
    :param conn:
    :param mid:
    :return:
    """
    cursor = conn.execute("SELECT DISTINCT(assigned_mid) FROM assignments WHERE mid=?", (mid,))
    rows = cursor.fetchall()

    if rows is not None:
        assigned_mid_list = []
        for row in rows:
            assigned_mid_list.append(row[0])
        return assigned_mid_list

    return None


def get_assignment_count(conn, mid, assigned_mid=None):

    if assigned_mid is None:
        cursor = conn.execute("SELECT COUNT(pid) FROM assignments WHERE mid=?",(mid,))
    else:
        cursor = conn.execute("SELECT COUNT(pid) FROM assignments WHERE mid=? AND assigned_mid=?",(mid,assigned_mid))

    row = cursor.fetchone()

    if row is None:
        # Assignment doesnt exist
        return None

    count = row[0]
    return count
