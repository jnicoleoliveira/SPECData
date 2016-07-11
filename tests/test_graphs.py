import sqlite3
from config import *

from functions import graph_peaks

# Connect to sqlite database
conn = sqlite3.connect(db_filepath)
cursor = conn.cursor()


print "Enter Experiment MID: "
exp_mid = 155
#exp_mid = raw_input()
print "Enter assigned MID: "
assigned_mid = 3
#assigned_mid = raw_input()

graph_peaks.graph_experiment_and_assignment(conn, exp_mid, assigned_mid, False)