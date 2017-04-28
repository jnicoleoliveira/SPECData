import re
import time

import matplotlib.pyplot as plot
import pyclustering.cluster.xmeans as xmeans
from pyclustering.utils import read_sample

from analysis.peak_finder import *


def main():
    file_path = "/home/joli/Downloads/Av_CP343-CP348_ft.sp"
    frequencies, intensities = read_data(file_path)
    max_x = max(frequencies)
    max_y = (max(intensities))
    avg = sum(intensities) / len(intensities)

    # Marie's Function
    plot.plot(frequencies, intensities, color='grey')
    # test(peak_finder, frequencies, intensities, 0.2)
    #
    # # Kyle's Function
    # plot.plot(frequencies, intensities, color='grey')
    # test(k_peak_finder, frequencies, intensities, 3)
    # # Using Peak Utils
    # plot.axhline(linewidth=4,y=avg, color='green', xmin=0, xmax=max_x)
    # plot.plot(frequencies, intensities, 'bo', color='grey')
    # plot.plot(frequencies, intensities, 'bo', color='grey')
    # test(peak_finder_peakutils, frequencies, intensities, 0.0001)

    # Optimized
    # test(optimized_peak_finder, frequencies, intensities)


    # Test Difference
    # f1,i1 = peak_finder(frequencies, intensities, 1)
    f2, i2 = k_peak_finder(frequencies, intensities, 5)
    sample = read_sample("/home/joli/PycharmProjects/Experiments/168-175_pzf1.sp")
    instance = xmeans.xmeans(sample, [3.7, 5.5])
    instance.process()
    clusters = instance.get_clusters()
    print clusters
    # A = set(f1)
    # B = set(f2)
    # C = A&B
    #
    # print len(f1)
    # print len(f2)
    # print len(C)
    # plot.bar(f1, i1, color="purple")
    plot.bar(f2, i2, color="green", width=1)
    # plot.bar(C, [1] * len(C), color="yellow", bottom=-1)
    plot.show()


def test(function, *args):
    start = time.time()
    frequencies, intensities = function(*args)
    stop = time.time()

    duration = stop - start

    print function.__name__
    print "Peaks: " + str(len(frequencies))
    print "Duration: " + str(duration)
    print "\n"

    #plot.plot((0, avg), (max_x, avg), 'k-green', )
    plot.bar(frequencies, intensities, color='red')
    plot.show()

def read_data(file_path):
    delimiters = [" ", "\t", ",", ", "]
    regex = '|'.join((map(re.escape, delimiters)))

    # Get data from file
    frequencies = []
    intensities = []
    with open(file_path) as f:
        for line in f:
            if line is not None or line is not "":
                try:
                    point = re.split(regex, line.strip())
                    frequencies.append(float(point[0]))  # get frequency
                    intensities.append(float(point[1]))  # get actual intensity (logx ^ x)
                except ValueError:
                    continue

    return frequencies, intensities


if __name__ == '__main__':
    main()
