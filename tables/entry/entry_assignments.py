# Author: Jasmine Oliveira
# Date: 7/08/2016
#


def add_assignment(conn, pid, mid, assigned_mid, assigned_pid):
    """

    :param conn:
    :param pid:
    :param mid:
    :param assigned_mid:
    :param assigned_pid:
    :return:
    """
    cursor = conn.execute("INSERT INTO assignments(pid, mid, assigned_mid, assigned_pid) VALUES (?,?,?,?)",(pid, mid, assigned_mid, assigned_pid))
    conn.commit()