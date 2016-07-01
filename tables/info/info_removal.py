# Author: Jasmine Oliveira
# Date: 07/01/2016
# info_removal:
#       Module that removes info table entries:
#       Functions:
#                   * remove_info(conn, iid):


from info_entry import iid_exists

def remove_info(conn, iid):
    """
    Removes info entry of a given iid
    :param conn: Sqlite database connection
    :param mid: Info ID (iid) of entry to be removed
    :return: True if successfully removed
    :return: False, if not removed
    """
    if(iid_exists(conn, iid) is False):
        print "[ ERROR: Info entry does not exist. Cancelling action! ]"
        return False

    # Delete Info Entry
    conn.execute("DELETE FROM info WHERE iid={i}".format(i=iid))
    conn.commit()

    print "[ Successfully removed iid:" + str(iid) + " from database ]"
    return True