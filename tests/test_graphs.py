import sqlite3
from config import *

from scripts import graph_peaks
from scripts import assign_peaks
import tables.molecules_table as get_molecules
import tables.get.get_assignments as get_assignments
# Connect to sqlite database
conn = sqlite3.connect(db_filepath)
cursor = conn.cursor()


print "Enter Experiment MID: "
exp_mid = 156
#exp_mid = raw_input()
#assigned_mid = raw_input()

# If peaks are not assigned... assign peaks
if get_assignments.has_assignments(conn, exp_mid) is False:
    assignments = assign_peaks.assign_peaks(conn, exp_mid)
else:
    assignments = get_assignments.get_assigned_mids(conn, exp_mid)

# PRINT ASSIGNMENT MID  NAME    COUNT
print "Assignments...."
for a in assignments:
    print str(a) + " " + get_molecules.getName(conn, a) + " (" + str(get_assignments.get_assignment_count(conn,exp_mid,a)) + ")"

#assigned_mid = 3

while(True):
    print "Enter assigned MID: "
    assigned_mid = raw_input()
    graph_peaks.graph_experiment_and_assignment(conn,exp_mid,assigned_mid,True,True,True)
    graph_peaks.graph_experiment_and_assignment(conn,exp_mid,assigned_mid,False)

#graph_peaks.graph_experiment_and_assignment(conn, exp_mid, assigned_mid, False, False)
#graph_peaks.graph_experiment_and_assignment(conn, exp_mid, assigned_mid, True, False)
#graph_peaks.graph_experiment_and_assignment(conn, exp_mid, assigned_mid, False, True)
#graph_peaks.graph_experiment_and_assignment(conn, exp_mid, assigned_mid, True, True)