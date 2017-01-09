# -----------------------------------------------------------------------------
# Author: Jasmine Oliveira
# Date:   11/21/2016 (Refactored API)
# -----------------------------------------------------------------------------
# assignments_table.py:
# -----------------------------------------------------------------------------
# Module designed as a SQLite API to get, manipulate, and enter data of
# the assignments table in the SPECdata database system. A single row in the
# table represents a single peak and an assigned peak.
#
#       Peaks table entries have the following format:
#           -> aid           (int:   id of the assignment table entry)
#           -> pid           (int:   id of the experiment peak)
#           -> assigned_pid  (int:   id of the assigned peak)


from molecules_table import mid_exists

###############################################################################
# Get Assignments Table Information
# -----------------------------------------------------------------------------
# Date: 07/08/2016
# -----------------------------------------------------------------------------
# Get data from the peaks table
# Public Functions:
#       * aid_exists(conn, aid)
#       * get_assigned_mids(conn, mid)
#       * assignment_exists(conn, pid, assigned_pid)
#       * get_assignment_count(conn, mid, assigned_mid=None)
#       * get_assignment_tuples_list(conn, mid)
#       * has_assignments(conn, mid)
###############################################################################


def aid_exists(conn, aid):
    """
    Determines if assignments entry is in the database (based on aid)
    :param conn: Sqlite connection
    :param cursor: Connection cursor
    :param aid: Assignments entry ID (aid)
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


def assignment_exists(conn, pid, assigned_pid):
    """
    Determines if assignments entry is in the database (based on assignment info)
    :param conn: Sqlite connection
    :param pid: Assignments entry ID (aid)
    :param assigned_pid: Connection cursor
    :return: True if assignment exists. False if assignment does not exist.
    """
    # Select row with mid
    cursor = conn.execute("SELECT * FROM assignments WHERE "
                          "pid=? AND assigned_pid=?", (pid, assigned_pid))
    row = cursor.fetchone()

    if row is None:
        # Assignments entry does not exist.
        return False

    # Assignments entry exists
    return True


def get_assigned_mids(conn, mid):
    """
    Returns list of assigned mids to a particular molecule
    :param conn:
    :param mid:
    :return:
    """
    cursor = conn.execute("SELECT DISTINCT (P.mid) FROM"
                          "(SELECT DISTINCT(assigned_pid)"
                          "FROM assignments AS a JOIN peaks as P ON P.pid=A.pid WHERE P.mid=?)"
                          "as A JOIN Peaks as P"
                          "ON A.assigned_pid = P.pid;", (mid,))
    rows = cursor.fetchall()

    if rows is not None:
        assigned_mid_list = []
        for row in rows:
            assigned_mid_list.append(row[0])
        return assigned_mid_list

    return None


def get_assignment_count(conn, mid, assigned_mid=None):

    if assigned_mid is None:
        cursor = conn.execute("SELECT COUNT(p.pid) FROM assignments as a join peaks as p "
                              "ON p.pid=a.pid WHERE p.mid=?",(mid,))
    else:
        cursor = conn.execute("SELECT COUNT(p.pid) FROM "
                              "(SELECT a.assigned_pid FROM assignments as a join peaks as p "
                              "ON p.pid=a.pid WHERE p.mid=?)"
                              "AS a join peaks as p ON a.assigned_pid=p.pid"
                              "WHERE p.mid=?",(mid, assigned_mid))
        #                      "ON p.pid = a.pid WHERE mid=? AND assigned_mid=?",(mid,assigned_mid))

    row = cursor.fetchone()

    if row is None:
        # Assignment doesnt exist
        return None

    count = row[0]
    return count


def get_assignment_tuples_list(conn, mid):
    cursor = conn.execute("SELECT A.pid, A.assigned_pid "
                          "FROM assignments as A JOIN peaks as P "
                          "ON P.pid=A.pid WHERE P.mid=?;", (mid,))

    rows = cursor.fectchall()

    tuples = []
    for row in rows:
        tuples.append([row[0], row[1]])

    return tuples


def get_assignment_aid_list(conn, mid):
    cursor = conn.execute("SELECT A.aid "
                          "FROM assignments as A JOIN peaks as P "
                          "ON P.pid=A.pid WHERE P.mid=?;", (mid,))

    rows = cursor.fetchall()

    aids = []
    for row in rows:
        aids.append(row[0])

    return aids


def has_assignments(conn, mid):
    """
    Determines if a molecule has assignments
    :param conn: SQLite Database conenction
    :param mid: Molecule ID (mid) of molecule to check
    :return: False, if there are no assignments. True, if there are assignments.
    """
    cursor = conn.execute("SELECT * FROM assignments as A JOIN"
                          "peaks as P ON P.pid=A.pid WHERE P.mid=?;", (mid,))

    row = cursor.fetchone()

    if row is None:
        # There are no assignments to this molecule
        return False

    # There are assignments to this molecule
    return True


###############################################################################
# Insert Peaks Table Entry
# -----------------------------------------------------------------------------
# Date: 07/08/2016
# -----------------------------------------------------------------------------
# Inserts row entries into the Assignment table
# Public Functions:
#       * new_assignment_entry(conn, pid, assigned_pid)
###############################################################################


def new_assignment_entry(conn, pid, assigned_pid):
    """
    Enters a new assignment entry into the database.
    :param conn: SQLite database connection
    :param pid: Peak ID
    :param assigned_pid: Assigned Peak ID
    :return: aid of new assignment entry
    """
    conn.execute("INSERT INTO assignments(pid, assigned_pid) VALUES (?,?)", (pid, assigned_pid))

    # Get the new entry's molecule id (mid)
    cursor = conn.execute('SELECT max(aid) FROM assignments')
    aid = cursor.fetchone()[0]

    # Commit Changes
    conn.commit()

    return aid
##############################################################################
# Remove Assignment Table Entry
# -----------------------------------------------------------------------------
# Date: 07/08/2016
# -----------------------------------------------------------------------------
# Removes row entry/entries from the Assignment table
# Public Functions:
#       * remove_all(conn, mid):
#       * remove_assignment(conn, aid)
###############################################################################


def remove_all(conn, mid):
    """
    Removes all entries for a specified molecule
    :param conn: Connection to sqlite3 database
    :param mid: Molecule entry ID (mid) to remove associated peaks
    :return: True, if assignments are removed successfuly, otherwise False
    """
    if(mid_exists(conn, mid) is False):
        print "[ ERROR: Molecule entry does not exist. Cancelling action! ]"
        return False

    sql="DELETE FROM assignments WHERE aid IN (" \
        " SELECT aid" \
        " FROM peaks INNER JOIN assignments ON (assignments.pid=peaks.pid)"\
        " WHERE peaks.mid={m}" \
        ");".format(m=mid)

    conn.execute(sql)
    conn.commit()

    return True


def remove_assignment(conn, aid):
    """
    Removes a specified assignment entry, by its aid
    :param conn: Connection to sqlite3 database
    :param aid: Assignment entry ID (aid)
    :return: True, if assignment removes successfuly, otherwise False
    """
    # Determine if aid exists
    if(aid_exists(conn, aid) is False):
        print "[ ERROR: assignment entry does not exist. Cancelling action! ]"
        return False

    # Exists, remove assignment
    conn.execute("DELETE FROM assignments WHERE aid={a}".format(a=aid))
    conn.commit()

    return True

