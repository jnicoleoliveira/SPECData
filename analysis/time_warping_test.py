# Author: Jasmine Oliveira
# Date: 09/19/2016


from dtw import dtw
import matplotlib.pyplot as plt
from numpy.linalg import norm

from config import conn, db_dir
import numpy
from analysis import peak_finder

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
frequencies, intensities = peak_finder.peak_finder(frequencies, intensities, 0.2)
print "     .....determined peaks."

from tables.get import get_peaks
all = get_peaks.get_all_known_frequencies(conn)
print "Got Known Data: " + str(len(all))


x = numpy.array(frequencies)
y = numpy.array(all)
def my_custom_norm(x, y):
    return (x-y)
print "Determining DTW.."
dist, cost, acc, path = dtw(x, y, dist=lambda x, y: my_custom_norm(x,y))
print "Done."

print "     ..... plotting."
plt.imshow(acc.T, origin='lower', interpolation='nearest')
plt.plot(path[0], path[1], 'w')
plt.xlim((-0.5, acc.shape[0]-0.5))
plt.ylim((-0.5, acc.shape[1]-0.5))

