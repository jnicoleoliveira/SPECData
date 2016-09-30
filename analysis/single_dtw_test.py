# Author: Jasmine Oliveira
# Date: 09/23/2016
# Testing of a single known vs experiment using DTW

import matplotlib.pyplot as plt
from config import conn, db_dir
import numpy as np
from analysis import peak_finder
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from tables.get import get_peaks

experiment_mid = 145
known_mid = 75

max_freq = get_peaks.get_max_frequency(conn, experiment_mid)
min_freq = get_peaks.get_min_frequency(conn, experiment_mid)

exp_frequencies, exp_intensities = get_peaks.get_frequency_intensity_list(conn, experiment_mid)
from experiment import Experiment
#exp = Experiment("168-175-pzf1", 145, 0.4)
#exp.get_assigned_molecules()
#assignment_mids = exp.get_assigned_mids()
#frequencies = get_peaks.get_frequencies_in_midlist(conn, assignment_mids)
frequencies, intensities = get_peaks.get_frequency_intensity_list(conn, known_mid,max=max_freq, min=min_freq)


print "Got Experiment Data: " + str(len(exp_frequencies))
print "Got Known Data: " + str(len(frequencies))

x = np.array(exp_frequencies)
y = np.array(frequencies)

print "Determining DTW.."
distance, path = fastdtw(x, y, dist=euclidean)
print "Done."

print " Distance = " + str(distance)

'''
PLOT DTW
'''
for point in path:
    #if(point[0] > 1 and point[0]<270):
    plt.scatter(point[0], point[1], marker='o')

plt.grid()
plt.show()

'''
PLOT LINE SEGMENTS ONLY
'''


def get_linear_segments(path):
    def get_slope(a, b):
        """
        Rise over Run (b_y - a_y/ b_x - a_x)
        :param a:
        :param b:
        :return:
        """
        if b[1] == a[1] or b[0] == a[0]:
            return -1

        return ((b[1] - a[1]) / (b[0] - a[0]))

    segments = []
    current_segment = []

    i = 0
    for i in range(0, len(path)-1):
        if get_slope(path[i], path[i+1]) is 1:
            current_segment.append(path[i])
            current_segment.append(path[i+1])
        else:
            if len(current_segment) is not 0:
                segments.extend(current_segment)
                current_segment = []

    return segments

# get line segments
linear_segments_path = get_linear_segments(path)
for point in linear_segments_path:
    #if(point[0] > 1 and point[0]<270):
    plt.scatter(point[0], point[1], marker='o')

plt.grid()
plt.show()


'''
Display matched line segments!
'''

plt.bar(exp_frequencies, exp_intensities, color='black')

for point in linear_segments_path:
    ki = point[1]    # known index
    plt.bar(frequencies[ki], intensities[ki], edgecolor='red', bottom=0.5)

plt.grid()
plt.show()