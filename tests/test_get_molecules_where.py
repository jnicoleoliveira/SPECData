
def main():

    from tables import molecules_table
    from config import conn

    category = ['experiment', 'artifact']
    molecules_table.get_molecules_where(conn, category)

    print "-------------------------------"

    category = ['known', 'artifact']
    units = ["MHz"]
    vibrational = 1
    isotope = 1
    min_temp=3
    max_temp=6.5
    composition=None
    type=None

    molecules_table.get_molecules_where(conn, category, units, \
                                        min_temp, max_temp,
                                        composition, isotope,
                                        vibrational, type)

    print "-------------------------------"

    category = ['experiment', 'artifact']
    type = ["Discharge"]
    # min_temp = None
    # max_temp = None
    # isotope = None
    # vibrational = None
    # units = None

    molecules_table.get_molecules_where(conn, category, units, \
                                        min_temp, max_temp,
                                        composition, isotope,
                                        vibrational, type)
if __name__ == '__main__':
    main()


def get_molecules_where(conn, category, units=None, min_temp=None, max_temp=None, composition=None,  isotope=None, vibrational=None, type=None,):
    """
    Gets list of all
    """

    query = ""
    info_table = "ExperimentInfo"

    ''' Filter by Molecule '''
    if category is None:
        query = "SELECT mid FROM molecules"
    else:
        query = "SELECT mid FROM molecules WHERE category IN" + get_in_string(category)

    ''' Filter by KnownInfo '''
    if ("known" in category or "artifact" in category) and \
            len(filter(None, [units, min_temp, max_temp, composition, isotope, vibrational])) is not 0:

        query = "SELECT A.mid FROM (" + query + ") as A JOIN KnownInfo" \
                + " as B ON A.mid = B.mid WHERE "

        strings = []

        if units is not None:
            s = "units IN " + get_in_string(units)
            strings.append(s)

        if min_temp is not None:
            s = "temperature >= " + str(min_temp)
            strings.append(s)

        if max_temp is not None:
            s = "temperature <= " + str(max_temp)
            strings.append(s)

        if isotope is not None:
            s = "isotope = " + str(isotope)
            strings.append(s)

        if vibrational is not None:
            s = "vibrational = " + str(vibrational)
            strings.append(s)

        for i in range(0, len(strings)-1):
            query += strings[i] + " AND "

        query += strings[len(strings)-1]

    ''' Filter by Experiment '''
    if ("experiment" in category) and \
        len(filter(None, [units, type, composition])) is not 0:

        query = "SELECT A.mid FROM (" + query + ") as A JOIN ExperimentInfo" \
                + " as B ON A.mid = B.mid WHERE "

        strings = []

        if units is not None:
            s = "units IN " + get_in_string(units)
            strings.append(s)

        if type is not None:
            s = "type IN " + get_in_string(type)
            strings.append(s)

        for i in range(0, len(strings)-1):
            query += strings[i] + " AND "

        query += strings[len(strings)-1]

    print query
    cursor = conn.execute(query)

    mids = []
    rows = cursor.fetchall()
    for row in rows:
        mids.append(row[0])

    return mids
