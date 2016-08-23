# Author: Jasmine Oliveira
# Date: 07/05/2016
# Imports all local files to database

import os.path
import sqlite3

from config import *
from queries import view_query

# Database Functions
import tables.get.get_molecules as mol_get
import tables.entry.entry_molecules as mol_entry
import tables.remove.remove_molecules as mol_rem
import tables.entry.entry_peaks as p_entry
import tables.remove.remove_peaks as p_rem

# Connect to sqlite database
conn = sqlite3.connect(db_filepath)
cursor = conn.cursor()

while True:
    print "Choose an option: \n (a) Import all files in path\n (b) Import individual file\n (c) Remove a molecule entry \n (d) Remove all peaks \n (e) View a row"
    input = raw_input()


    if input == 'a':
        print "Enter category: "
        category = raw_input()
        print "Enter file directory : "
        path = raw_input()
        imported = 0

        # Insert known values
        for i in os.listdir(path):
            if i.endswith('.cat') or i.endswith('.lines'):
                name = (i.split("."))[0]
                filepath = os.path.join(path, i)
                # New Molecule entry
                #mid = mol_entry.get_mid(conn,name, category)
                #p_rem.remove_all(conn,mid)
                mid = mol_entry.new_molecule_entry(conn, name, category)
                # New Peaks entry
                try:
                    print "Importing: " + name
                    p_entry.import_file(conn,filepath, mid)
                    imported += 1
                except ImportError:
                    print "Error importing: " + name
    elif input == "b":
        print "Enter molecule name: "
        name = raw_input()
        print "Enter category: "
        category = raw_input()
        print "Enter filepath: "
        filepath = raw_input()

        # New molecule entry
        mid = mol_entry.new_molecule_entry(conn, name, category)
        # New Peaks entry
        try:
            print "Importing: " + name
            p_entry.import_file(conn, filepath, mid)
        except ImportError:
            print "Error importing: " + name
    elif input == "c":
        print "Enter mid: "
        mid = raw_input()
        name = mol_get.getName(conn, mid)
        mol_rem.remove_molecule(conn,mid)
        print "[ Removed molecule: " + name + " ]"

    elif input == "d":
        print "Enter mid: "
        name = mol_get.getName(conn, mid)
        p_rem.remove_all(conn, mid)
        print "[ Removed all peaks for: " + name + " ]"

    elif input == "e":
        print "Enter tablename: "
        table = raw_input()
        print "Enter appropriate id: "
        id = raw_input()
        print view_query.row_view(table,id)
    else:
        print "Error. Incorrect input."