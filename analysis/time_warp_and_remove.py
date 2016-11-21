# Author: Jasmine Oliveira
# Date: 09/30/2016
# Testing following algorithm:
"""
(1) Find DTW path with the smallest distance
(2) Get line segments of the DTW path
(3) Remove all associated peaks in this path.
(4) Repeat 1-3 until the closest path has NO linear segments!
"""

import matplotlib.pyplot as plt
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

from config import conn
from temp.get import get_peaks, get_molecules


class TimeWarpRemove():
    def __init__(self, mid):
        # Experiment Data
        self.mid = mid
        self.efreqlist = []
        self.eintelist = []
        self.max_frequency = None
        self.min_frequency = None

        # Candidate Data
        self.candidates = []
        self.f = []

        # Best fit Data
        self.min_distance = None
        self.min_path = None
        self.min_mid_list = None
        self.combination_list = None

        # Assigned mids
        self.assigned_mids = []
        self.full_path = []

    def __get_data__(self):
        # Get Experiment Frequencies
        self.efreqlist, self.eintelist = \
            get_peaks.get_frequency_intensity_list(conn, self.mid)

        # Get MAX and MIN
        self.max_frequency = get_peaks.get_max_frequency(conn, self.mid)
        self.min_frequency = get_peaks.get_min_frequency(conn, self.mid)

        # Get Candidates
        self.candidates = get_molecules.get_mid_list(conn)
        #self.get_candidates()

        print "Candidates: "
        print self.candidates
        print "\n"

    def get_optimal_path(self):
        self.__get_data__()

        # (1) Find molecule with shortest distance
        min_mid, min_distance, min_path = self.find_lowest()

        # Remove
        self.remove_candidate(min_mid)

        # (2) Get Line Segments
        linear_segments = self.get_linear_segments(min_path)

        # (3) Determine associated peaks, and remove
        self.remove_assigned_from_frequencies(linear_segments)

        # Repeat 1-3 until the closest has no linear segments
        assignable = True
        while assignable is True:

            self.full_path.extend(linear_segments) # add segments to full path

            # (1) Find molecule with shortest distance
            min_mid, min_distance, min_path = self.find_lowest()

            self.remove_candidate(min_mid)

            # (2) Get Line Segments
            linear_segments = self.get_linear_segments(min_path)

            # (3) Determine associated peaks, and remove
            self.remove_assigned_from_frequencies(linear_segments)

            if len(linear_segments) is 0:
                assignable = False

    def remove_candidate(self, mid):
        self.candidates.remove(mid)
        print "Removed Candidate"

    def display_path(self):
        for point in self.full_path:
            plt.scatter(point[0], point[1], marker='o')

        plt.grid()
        plt.show()

    def remove_assigned_from_frequencies(self, linear_segments):

        if len(linear_segments) is 0:
            return

        new_list=[]
        indexes =[]
        for point in linear_segments:
            indexes.append(point[0])

        for i in range(0, len(self.efreqlist)):
            if i not in indexes:
                new_list.append(self.efreqlist[i])

        self.efreqlist = new_list

    def find_lowest(self):
        """
        :return: mid, distance, path
        """
        min_distance = 0
        min_path = None
        min_mid = None
        candidates = self.candidates #get_molecules.get_mid_list(conn)

        i = 0
        for mid in candidates:

            frequencies, intensities = get_peaks.get_frequency_intensity_list(conn,
                                                                              mid,
                                                                              max=self.max_frequency,
                                                                              min=0)  # ,

            try:
                distance, path = fastdtw(self.efreqlist, frequencies, dist=euclidean)
            except IndexError:
                continue

            if min_path is None:
                min_path = path
                min_distance = distance
                min_mid = mid
            elif distance < min_distance:
                min_distance = distance
                min_path = path
                min_mid = mid

        print min_distance
        print min_mid
        print get_molecules.getName(conn, min_mid)

        return min_mid, min_distance, min_path

    def get_linear_segments(self, path):
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
        for i in range(0, len(path) - 1):
            if get_slope(path[i], path[i + 1]) is 1:
                current_segment.append(path[i])
                current_segment.append(path[i + 1])
            else:
                if len(current_segment) is not 0:
                    segments.extend(current_segment)
                    current_segment = []

        return segments


if __name__ == "__main__":
    T = TimeWarpRemove(145)
    T.get_optimal_path()
    T.display_path()