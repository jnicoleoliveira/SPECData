# Author: Jasmine Oliveira
# Date: 8/2/2016
# Test Assignment Probability
import matplotlib
matplotlib.use('TkAgg')
from analysis.experiment import *
import matplotlib.pyplot as plt
from config import *
from temp.get import get_molecules
from temp.remove import remove_assignments
from tables.entry import entry_assignments
from temp.get import get_peaks

# Get Experiment Data
print "Enter Experiment MID: "
experiment_mid = 145
experiment_name = get_molecules.getName(conn, experiment_mid)


# Create New Experiment Obj for analysis
print "Created New Experiment: " + experiment_name
experiment = Experiment(experiment_name, experiment_mid)

# Analyse Experiment
print "Analysing Experiment...  "
experiment.get_assigned_molecules()

# Print Results
print "Analysis Complete. \n"
print "------------------------------------------\n" \
      "------RESULTS-----------------------------\n" \
      "------------------------------------------\n"
experiment.print_matches()


# Store new assignments in database
remove_assignments.remove_all(conn, experiment_mid)   # Remove all existing assignments
for key, value in experiment.molecule_matches.iteritems():
      for match in value.matches:
            entry_assignments.add_assignment(conn, match.exp_pid, experiment_mid, match.mid, match.pid)     # add new assigments

# Graph Results
#assigned_mids = experiment.get_assigned_mids()  # GET ASSIGNED MIDS
#for assigned_mid in assigned_mids:
#    graph_peaks.graph_experiment_and_assignment(conn, experiment_mid, assigned_mid, subplot=True, show_exp_peaks=False,show_assigned_lines=True)
lower_limit = 0.2
colors = ['green', 'blue', 'yellow', '#ff6500', 'cyan', 'magenta', '#008B8B', '#8B0000','#FA8072', '#FF69B4','#BDB76B', '#663399','#7cfc00',  ]
color_index = 0

experiment_peaks, experiment_intensities = get_peaks.get_frequency_intensity_list(conn, experiment_mid)
# Determine Axes
# Axes are determined my maximum values of experiment freq/inte values
x_axis = get_peaks.get_max_frequency(conn, experiment_mid)
y_axis = get_peaks.get_max_intensity(conn, experiment_mid)

f, axarr = plt.subplots(2, sharex=True) # Create subplot
#plt.axis(x_axis,y_axis)
#plt.axis([0, x_axis,0, y_axis])  # set axis
plt.xlabel("Frequency")
plt.ylabel("Intensity")

# Plot experiment
axarr[0].set_title('Experiment Peaks')
axarr[0].bar(experiment_peaks, experiment_intensities, edgecolor='black')

### Plot assignments ###
axarr[1].set_title('Molecule Matches')
print "\n\n -------COLOR KEY-------\nNAME            COLOR"
for key, value in experiment.molecule_matches.iteritems():
    frequencies = []
    intensities = []
    for match in value.matches:
        frequencies.append(get_peaks.get_frequency(conn, match.pid))
        intensities.append(get_peaks.get_intensity(conn, match.pid))

    axarr[1].bar(frequencies, intensities, width=0.02, edgecolor=colors[color_index])
    print value.name + "\t" + colors[color_index]   # Print KEY
    color_index += 1

plt.show()
