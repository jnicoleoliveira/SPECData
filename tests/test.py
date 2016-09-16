# Author: Jasmine Oliveira
# Date: 07/01/2016
# Tests scripts of SPECdata

import sqlite3

import config
from queries import view_query

# Database Functions
import tables.entry.entry_info as info_entry
import tables.remove.remove_info as info_rem
import tables.entry.entry_molecules as mol_entry
import tables.entry.entry_peaks as p_entry


def main():

    # Connect to sqlite database
    conn = sqlite3.connect(config.db_filepath)
    cursor = conn.cursor()

    ########### PROMPT USER ###########
    print "Enter molecule name, category:"
    input = raw_input().split()
    name = input[0]
    category = input[1]
    print "Enter peak data filename: "
    filename = raw_input()
    print "Enter info (vibration, notes): "
    input = raw_input().split()
    vibration = input[0]
    notes = input[1]

    filepath = "C:\Users\Jasmine\PycharmProjects\PeakDetection\Known" + "\\" + filename

    ###############################################
    #### BEGIN TEST ####
    print "************ BEGINNING TEST ************"

    # CREATE MOLECULE #############################
    ["Creating Molecule Entry."]
    mid = mol_entry.new_molecule_entry(conn, name, category)

    # If Creation unsuccessfull STOP
    if(mid is None):
        mid = mol_entry.get_mid(conn, name, category)
        print "[Molecule already exists.. continuing test]"
        if(mid is None):
            print "[CREATION UNSUCCESSFUL] [STOPPING TEST]"
            return
    else:
        print ["SUCCESS: Created new molecule entry! "]

    # ADD INFO #############################
    print "\n"
    print "[Adding Info Entry]"
    iid = info_entry.new_info_entry(conn, mid, vibration, notes)
    if (iid is None):
        iid = info_entry.get_iid(conn, mid)
        if iid is not None:
            print "[INFO ENTRY ALREADY EXISTS. Removing, and creating new entry]"
            info_rem.remove_info(conn, iid)
            info_entry.new_info_entry(conn, mid, vibration, notes)
        else:
            print "[ADD INFO UNSUCCESSFUL] [STOPPING TEST]"
            return
    print ["SUCCESS: Created new info entry! "]

    # IMPORT PEAKS #############################
    print "\n"
    print ["Importing Peaks Entry."]
    p_entry.import_file(conn, filepath, mid)
    print ["SUCCESS: Imported PEAKS! "]

    # OUTPUT NEW TABLE ENTRY
    # OUTPUT PEAKS LIST
    print "\n"
    printData(conn, mid)

    print "TESTING REMOVE FUNCTION"
    print "BEFORE REMOVAL: "
    print "Molecule table ---------------------"
    print view_query.table_view("molecules")
    print "Info table -------------------------"
    print view_query.table_view("info")
    # REMOVE ENTRY #############################
    #mol_rem.remove_molecule(conn, mid)
    #print "\nAFTER REMOVAL:"
    #print "Molecule table ---------------------"
    #print view_query.table_view("molecules")
    #print "Info table -------------------------"
    #print view_query.table_view("info")

    print "************ END OF TESTING ************"


def printData(conn, mid):
    # Get full joined entry
    cursor = conn.execute('SELECT molecules.mid, molecules.name, molecules.category, info.iid, info.vibration, info.notes FROM info JOIN molecules WHERE molecules.mid=?', (mid,))
    mid, name, category, iid, vibration, notes = cursor.fetchone()
    print "MID  NAME    CATEGORY    IID     VIBRATION   INFO"
    print str(mid) + "  " + str(name) + "    " + str(category) + "    " + str(iid) + "     " + str(vibration) + "   " + str(notes)
    #Get peaks list
    cursor = conn.execute('SELECT frequency, intensity FROM peaks WHERE mid=?', (mid,))
    print "FREQUENCY    INTENSITY"
    string = ""
    for row in cursor.fetchall():
        for column in row:
            string = string + "     " + str(column)
        string = string + "\n"
    print string

if __name__ == '__main__':
    main()