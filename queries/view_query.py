import sqlite3

import config


def table_view(tablename):

    # Connect to database
    conn = sqlite3.connect(config.db_filepath)
    cursor = conn.cursor()

    # get rows from table
    cursor = conn.execute("SELECT * FROM {tn};".format(tn=tablename))

    string = ""
    for row in cursor.fetchall():
        for column in row:
            string = string + "\t" + str(column)
        string = string + "\n"

    return string

def row_view(table_name, id):

    # Determine identifier
    if table_name is "molecules":
        id_name = "mid"
    elif table_name is "peaks":
        id_name = "pid"
    elif table_name is "info":
        id_name = "iid"
    else:
        return

    # Connect to database
    conn = sqlite3.connect(config.db_filepath)
    cursor = conn.cursor()

    # get row from table
    cursor = conn.execute("SELECT * FROM {tn} WHERE {idn}={idv}".format(tn=table_name, idn=id_name, idv=id))

    string = ""
    for row in cursor.fetchall():
        for column in row:
            string = string + "\t" + str(column)
        string = string + "\n"

    return string