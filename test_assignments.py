# Author: Jasmine Oliveira
# Date: 7/5/2016
# Test Peak Assignment

from config import *
import sqlite3
from queries import view_query
from tables.assignments import assignments_remove
from assign_peaks import *

#print "Enter pid: "
#pid = raw_input()

# Connect to sqlite database
conn = sqlite3.connect(db_filepath)
cursor = conn.cursor()

mid = 153 # EXP 168-175

# Remove all assignments
assignments_remove.remove_all(conn, mid)

# Try
#assign_peaks.get_candidates(conn, 496.799)
#assign_peaks(conn, 153)
midlist = [3, 7, 13, 10, 13]
assign_from_list(conn, 153, midlist)