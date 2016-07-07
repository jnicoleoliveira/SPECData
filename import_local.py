# Author: Jasmine Oliveira
# Date: 07/05/2016
# Imports all local files to database

from config import *
import sqlite3
import os, os.path
from queries import view_query

# Database Functions
import tables.info.info_edit as in_edit
import tables.info.info_entry as info_entry
import tables.info.info_removal as info_rem
import tables.molecules.molecules_entry as mol_entry
import tables.molecules.molecules_edit as mol_edit
import tables.molecules.molecules_removal as mol_rem
import tables.peaks.peaks_entry as p_entry
import tables.peaks.peaks_removal as p_rem

# Connect to sqlite database
conn = sqlite3.connect(db_filepath)
cursor = conn.cursor()

print "Choose an option: \n (a) Import all files in path\n (b) Import individual file\n (c) Remove a molecule entry \n (d) Remove all peaks"
input = raw_input()

print "Enter molecule name: "
name = raw_input()
print "Enter category: "
category = raw_input()

if input == 'a':
    print "Enter file directory : "
    path = raw_input()
    imported = 0

    # Insert known values
    for i in os.listdir(path):
        if i.endswith('.cat'):
            name = (i.split("."))[0]
            filepath = path + "\\" + i
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
elif input == "d":
    print "Enter filepath: "
    filepath = raw_input()
else:
    print "Error. Incorrect input."