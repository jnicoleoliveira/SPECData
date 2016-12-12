
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
