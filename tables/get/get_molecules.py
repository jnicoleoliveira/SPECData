def getName(conn, mid):
    cursor = conn.execute("SELECT name FROM molecules WHERE mid=?",(mid,))
    line = cursor.fetchone()
    name = line[0]
    return name