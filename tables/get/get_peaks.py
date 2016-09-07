import sqlite3


def get_max_frequency(conn, mid):
    """
    Gets the maximum frequency of a molecule
    :param conn: Connection to SQLite Database
    :param mid: Molecule entry ID
    :return: Maximum frequency of a molecule
    """
    cursor = conn.execute("SELECT MAX(frequency) FROM peaks WHERE mid=?",(mid,))
    line = cursor.fetchone()
    frequency = line[0]
    return frequency


def get_max_intensity(conn, mid):
    """
    Gets the maximum intensity of a molecule
    :param conn: Connection to SQLite Database
    :param mid: Molecule entry ID
    :return: Maximum intensity of a molecule
    """
    cursor = conn.execute("SELECT MAX(intensity) FROM peaks WHERE mid=?",(mid,))
    line = cursor.fetchone()
    intensity = line[0]
    return intensity

def get_average_intensity(conn, mid):
    """
    Gets the average intensity of a molecule
    :param conn: Connection to SQLite Database
    :param mid: Molecule entry ID
    :return: Average intensity of a molecule
    """
    cursor = conn.execute("SELECT AVG(intensity) FROM peaks WHERE mid=?",(mid,))
    line = cursor.fetchone()
    intensity = line[0]
    return intensity


def get_frequency(conn, pid):
    """
    Returns the frequency of a given peak
    :param conn: SQLite Database connection
    :param pid: Peak ID (pid) of specified peak
    :return:
    """
    cursor = conn.execute("SELECT frequency FROM peaks WHERE pid=?",(pid,))
    line = cursor.fetchone()
    frequency = line[0]
    return frequency


def get_frequency_intensity_list(conn, mid):
    """
    Returns frequency and intensity list of a particular module
    :param conn: SQLite Database connection
    :param mid: Molecule ID (mid) of associated peaks
    :return:
    """
    cursor = conn.execute("SELECT frequency, intensity FROM peaks WHERE mid=?",(mid,))
    rows = cursor.fetchall()

    frequency_list = []
    intensity_list = []
    for row in rows:
        frequency_list.append(row[0])
        intensity_list.append(row[1])

    return frequency_list, intensity_list


def get_intensity(conn, pid):
    """
    Returns the intensity of a specified peak
    :param conn:
    :param pid:
    :return:
    """
    cursor = conn.execute("SELECT intensity FROM peaks WHERE pid=?",(pid,))
    line = cursor.fetchone()
    intensity = line[0]
    return intensity


def get_pid_list(conn, mid):
    """
    Returns PID List (ordered by descending intensity)
    :param conn: SQLite Database connection
    :param mid: Molecule ID (mid) of associated peaks
    :return:
    """
    cursor = conn.execute("SELECT pid FROM peaks"\
                          " WHERE mid=?" \
                          " ORDER BY intensity DESC",(mid,))
    rows = cursor.fetchall()

    if rows is not None:
        pid_list = []
        for row in rows:
            pid_list.append(row[0])

        return pid_list

    return None


def get_peak_count(conn, mid):
    """
    Returns the count of peaks associated with this molecule
    :param conn:
    :param mid:
    :return:
    """
    cursor = conn.execute("SELECT COUNT(pid) FROM PEAKS"\
                          " WHERE mid=?", (mid,))
    rows = cursor.fetchone()
    return rows[0]


def get_unassigned_pid_list(conn, mid):
    """

    :param conn: SQLite Database connection
    :param mid: Molecule ID (mid) of associated peaks
    :return:
    """
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