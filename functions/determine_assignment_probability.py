# Author: Jasmine Oliveira
# Date: 8/2/2016
# Test Assignment Probability

from experiment import *
import sqlite3
from config import *
from tables.get import get_molecules

# Get Experiment Data
#print "Enter Experiment MID: "
experiment_mid = 157
experiment_name = get_molecules.getName(conn,experiment_mid)


# Create New Experiment Obj for analysis
print "Created New Experiment: " + experiment_name
experiment = Experiment(experiment_name, experiment_mid)

# Analyse Experiment
print "Analysing Experiment...  "
experiment.get_assigned_molecules()

# Print Results
print "Analysis Complete. "
print "\n------RESULTS------"
experiment.print_matches()