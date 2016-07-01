# Author: Jasmine Oliveira
# Date: 07/01/2016
# molecule_removal:
#       Module that removes molecule table entries:
#       Functions:
#                   * remove_molecule(conn, mid)

from molecules_entry import mid_exists

def remove_molecule(conn, mid):
    """
    Removes all info, peak and molecule entries of given mid
    :param conn: Sqlite database connection
    :param mid: Molecule ID (mid) of molecule to be removed
    :return: True if successfully removed
    :return: False, if not removed
    """
    if(mid_exists(conn, mid) is False):
        print "[ ERROR: Molecule entry does not exist. Cancelling action! ]"
        return False

    # Delete Info Entry
    conn.execute("DELETE FROM info WHERE mid={m}".format(m=mid))
    # Delete peak entry
    conn.execute("DELETE FROM peaks WHERE mid={m}".format(m=mid))
    # Delete Molecule entry
    conn.execute("DELETE FROM molecules WHERE mid={m}".format(m=mid))

    conn.commit()

    print "[ Successfully removed " + str(mid) + "from database ]"
    return True