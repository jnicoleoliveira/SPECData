def getName(conn, mid):
    cursor = conn.execute("SELECT name FROM molecules WHERE mid=?",(mid,))
    line = cursor.fetchone()
    name = line[0]
    return name

def mid_exists(conn, mid):
    """
    Determines if molecule entry is in the database (based on mid)
    :param conn: Sqlite connection
    :param cursor: Connection cursor
    :param mid: Molecule entry id (mid)
    :return: True if molecule exists. False if molecule does not exist.
    """
    # Select row with mid
    cursor = conn.execute("SELECT * FROM molecules WHERE mid=?", (mid,))
    row = cursor.fetchone()

    if row is None:
        # Molecule entry does not exist.
        return False