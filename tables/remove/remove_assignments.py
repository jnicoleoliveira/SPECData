# Author: Jasmine Oliveira
# Date: 07/06/2016
# assignments_removal:
#       Module that removes assignment table entries:
#       Functions:
#                   * remove_all(conn, mid)
#                   * remove_assignment(conn, aid)

from tables.entry.entry_molecules import mid_exists
from tables.get.get_assignments import aid_exists


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
    :param pid: Assignment entry ID (aid)
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

