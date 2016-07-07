import sqlite3

def get_pidlist(conn, mid):
    """

    :param conn:
    :param mid:
    :return:
    """
    cursor = conn.execute("SELECT pid FROM molecules INNER JOIN peaks WHERE molecules.mid = peaks.mid AND molecules.mid=?",(mid,))
    pid_list = cursor.fetchall()
    return pid_list

def get_frequency(conn, pid):
    cursor = conn.execute("SELECT frequency FROM peaks WHERE pid=?",(pid,))
    line = cursor.fetchone()
    frequency = line[0]
    return frequency

def get_unassigned_pidlist(conn, mid):

    # Set of all peaks for molecule
    all = "(SELECT peaks.pid FROM molecules JOIN peaks"\
          " ON molecules.mid = peaks.mid"\
          " WHERE molecules.mid={m})".format(m=mid)

    # Set of all assigned peaks of the molecule
    assigned = "(SELECT peaks.pid FROM peaks JOIN assignments"\
               " ON peaks.pid=assignments.pid"\
               " WHERE peaks.mid={m})".format(m=mid)

    # Unassigned peaks (all - assigned)
    unassigned = "SELECT pid FROM " + all + " EXCEPT SELECT pid FROM " + assigned + ";"
    print unassigned
    cursor = conn.execute(unassigned)

    return cursor.fetchall()