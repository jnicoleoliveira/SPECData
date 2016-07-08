from tables.entry.entry_molecules import mid_exists

def update_category(conn, mid, category):
    """
    Changes the category row of a molecule
    :param conn: Connection to sqlite database
    :param mid: Molecule ID (mid) to make changes
    :param category: New category to replace
    :return: True, if updated successfully
    :return: False, if
    """
    if(mid_exists(conn, mid) is False):
        print "[ ERROR: Molecule entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE molecules SET category={c} WHERE mid={m}".format(c=category, m=mid))
    conn.commit()
    return True

def update_name(conn, mid, name):
    """
    Changes the name row of a molecule
    :param conn: Connection to sqlite database
    :param mid: Molecule ID (mid) to make changes
    :param name: New name to replace
    :return: True, if updated successfully
    :return: False, if
    """
    if(mid_exists(conn, mid) is False):
        print "[ ERROR: Molecule entry does not exist. Cancelling action! ]"
        return False

    conn.execute("UPDATE molecules SET name={n} WHERE mid={m}".format(n=name, m=mid))
    conn.commit()
    return True
