# Author: Jasmine Oliveira
# Date: 07/01/2016
# info_edit:
#       Module that makes edits to info table entries:
#       Functions:
#                   * update_vibration(conn, iid, vibration)
#                   * update_notes(conn, iid, vibration)

from info_entry import iid_exists

def update_vibration(conn, iid, vibration):
    """
    Changes the category row of a molecule
    :param conn: Connection to sqlite database
    :param iid: Info ID (iid) to make changes
    :param vibration: New vibration value to replace old
    :return: True, if updated successfully
    :return: False, if
    """
    if(iid_exists(conn, iid) is False):
        print "[ ERROR: info entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE info SET vibration={v} WHERE iid={i}".format(v=vibration, i=iid))
    conn.commit()
    return True

def update_notes(conn, iid, notes):
    """
    Changes the notes row of a molecule
    :param conn: Connection to sqlite database
    :param iid: Info ID (iid) to make changes
    :param notes: New notes value to replace old
    :return: True, if updated successfully
    :return: False, if
    """
    if(iid_exists(conn, iid) is False):
        print "[ ERROR: info entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE info SET notes={n} WHERE iid={i}".format(n=notes, i=iid))
    conn.commit()
    return True