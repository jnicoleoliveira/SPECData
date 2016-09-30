# Author: Jasmine Oliveira
# Date: 09/19/2016


from dtw import dtw
import matplotlib.pyplot as plt
from config import conn, db_dir
import numpy as np
from analysis import peak_finder
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from tables.get import get_peaks

# Get data from file
frequencies = []
intensities = []
with open("/home/joli/PycharmProjects/SPECData/data/experiments/145.sp") as f:
    for line in f:
        point = str.split((line.strip()))
        frequencies.append(float(point[0]))  # get frequency
        intensities.append(float(point[1]))  # get actual intensity (logx ^ x)
print "Got Experiment Data: " + str(len(frequencies))
# Determine Peaks
#frequencies, intensities = peak_finder.peak_finder(frequencies, intensities, 0.2)
frequencies, intensities = get_peaks.get_frequency_intensity_list(conn, 145)

print "     .....determined peaks."

all = get_peaks.get_all_known_frequencies(conn)
mids, all = get_peaks.get_all_known_freqencies_with_mids(conn)

print "Got Known Data: " + str(len(all))



#x = np.array([0, 0, 1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)
#y = np.array([1, 1, 1, 2, 2, 2, 2, 3, 2, 0]).reshape(-1, 1)
#x = frequencies
#y = all
x = np.array(frequencies)
y = np.array(all)


def my_custom_norm(x, y):
    return (x-y)

print "Determining DTW.."
#dist, cost, path = dtw(x, y, dist=my_custom_norm(x, y))
distance, path = fastdtw(x, y, dist=euclidean)
#distance, path = fastdtw(x, y, dist=euclidean)

print "Done."

print " Distance = " + str(distance)

print "     ..... plotting."


'''
Plotting
'''
#plt.xticks(np.arange(min(x), max(x)))
#plt.plot(path, color='red')

matches = {}

for i in range(0, len(path)):

    mid = mids[path[i][1]]

    if(matches.get(mid) is None):
        matches[mid] = 1
    else:
        matches[mid] += 1

print len(matches)
#plt.show()
from tables.get import get_molecules

for key, value in matches.iteritems():
    name = get_molecules.getName(conn, key)
    print str(key) + " " + name + " " + str(value)
