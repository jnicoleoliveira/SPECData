from config import conn
from tables import molecules_table


def main():

    print molecules_table.get_mids_where_category_in(conn, ['known'])
    print "-----------------------"
    print molecules_table.get_mids_where_units_in(conn, ['MHz'], 'known')
    print molecules_table.get_mids_where_units_in(conn, ['MHz'], 'experiment')
    print molecules_table.get_mids_where_units_in(conn, ['MHz'])

    print "-----------------------"
    print molecules_table.get_mids_in_temperature_range(conn, 0, 6)
    print molecules_table.get_mids_in_temperature_range(conn, None, 3)

    print "-----------------------"
    print molecules_table.get_mids_where_types_in(conn, ['Discharge'])

    print "-----------------------"
    print molecules_table.get_mids_where_is_isotope(conn, True)

    print "-----------------------"
    print molecules_table.get_mids_where_is_vibrational(conn, True)


if __name__ == '__main__':
    main()