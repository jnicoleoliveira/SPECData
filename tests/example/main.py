from queries import view_query
from tables.entry import entry_info, entry_molecules, entry_peaks

from config import *

init = "python init/init.py"

def main():
    #subprocess.call(init)   # Initialize / Create Database
    # Testing import entry

    # Connect to sqlite database
    conn = sqlite3.connect(db_filepath)
    cursor = conn.cursor()

    while True:

        print "Would you like to delete (d) or add (a)?"
        choice = raw_input()

        if choice is "a":
        ## Add
            print "Enter molecule name:"
            name = raw_input()
            print "Enter category: "
            category = raw_input()

            # Check if molecule exists
            mid = entry_molecules.get_mid(conn, name, category)
            if(mid is None):
                # Does not exist
                # Create new entry
                print("[ Molecule entry does not exist. Creating new entry.]")
                mid = entry_molecules.new_molecule_entry(conn, name, category)

                print "Please enter file name: "
                filename = raw_input()
                path = "C:\Users\Jasmine\PycharmProjects\PeakDetection\Known" + "\\" + filename
                print "[Importing: " + path + " ]"
                entry_peaks.import_file(conn, path, mid)
            else:
                print "[ ERROR: Molecule entry already exists.]"
                print view_query.row_view("molecules", mid)

            ########### INFO ##############
            print "INFO------------------------"
            print "Enter molecule vibration: "
            vibration = raw_input()
            print "Enter notes about this molecule: "
            notes = raw_input()
            entry_info.new_info_entry(conn, mid, vibration, notes)            # create new info entry

        elif choice is "d":
        ## Delete
            print "Enter mid: "
            # Test dele

        print "\nMolecule Table\n--------------------------------"
        print view_query.table_view("molecules")

if __name__ == '__main__':
    main()