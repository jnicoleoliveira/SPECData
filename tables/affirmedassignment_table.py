# -----------------------------------------------------------------------------
# Author: Jasmine Oliveira
# Date:   1/08/2017
# -----------------------------------------------------------------------------
# affirmedassignment_table.py:
# -----------------------------------------------------------------------------
# Module designed as a SQLite API to get, manipulate, and enter data of
# the AffirmedAssignments table in the SPECdata database system. A single row
# in the table represents an assignment, and its affirmed status.
#
#       Peaks table entries have the following format:
#           -> fid           (int:   id of the affirmed assignment table entry)
#           -> aid           (int:   id of the assignment table entry)
#           -> status        (string: status of the assignment)

from tables.assignments_table import aid_exists, get_assignment_aid_list
from tables.molecules_table import get_in_string

def get_status(conn, aid):
    """
    Determines if assignments entry is in the database (based on aid)
    """
    # Select row with mid
    cursor = conn.execute("SELECT status FROM AffirmedAssignments WHERE aid=?", (aid,))
    row = cursor.fetchone()

    if row is None:
        # Assignments entry does not exist.
        return False

    # Assignments entry exists
    return row[0]

def entry_exists(conn, aid):
    """
    Determines if assignments entry is in the database (based on aid)
    """
    # Select row with mid
    cursor = conn.execute("SELECT * FROM AffirmedAssignments WHERE aid=?", (aid,))
    row = cursor.fetchone()

    if row is None:
        # Assignments entry does not exist.
        return False

    # Assignments entry exists
    return True


def new_entry(conn, aid, status):
    """
    Enters a new assignment entry into the database.
    :param conn: SQLite database connection
    :param aid: id of the assignment table entry
    :param status: status of the assignment
    :return:
    """
    conn.execute("INSERT INTO AffirmedAssignments(aid, status) VALUES (?,?)", (aid, status))

    # Get the new entry's molecule id (mid)
    cursor = conn.execute('SELECT max(fid) FROM AffirmedAssignments')
    fid = cursor.fetchone()[0]

    # Commit Changes
    conn.commit()

    return fid


def update_status(conn, aid, status):

    if aid_exists(conn, aid) is False:
        print "[ ERROR: assignment entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE AffirmedAssignments SET status={s}"
                 " WHERE aid={a}".format(s=status, a=aid))
    conn.commit()
    return True


def remove_all(conn, mid):

    aid_list = get_assignment_aid_list(conn, mid)
    print "[ REMOVE AID LIST: " + str(aid_list) + " ]"
    if aid_list  is None or len(aid_list) is 0:
        return False

    string = "DELETE FROM AffirmedAssignments WHERE aid IN" + get_in_string(aid_list)
    print string
    conn.execute(string)
    conn.commit()

    return True
