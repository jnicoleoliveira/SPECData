# Author: Jasmine Oliveira
# Date: 09/23/2016
# Implement time warping with backtracking

from config import conn
from tables.get import get_peaks, get_molecules

import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

class TimeWarpExperiment:

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

    def find_lowest(self):
        self.__get_data__()
        min_distance = 0
        min_path = None
        min_mid = None
        candidates = get_molecules.get_mid_list(conn)

        i = 0
        for mid in candidates:
            if mid is 144:
                continue

            if mid in [3,4,94,35,34,49, 38, 37,36, 39, 92]:
                continue
            #if mid in [3, 1, 29, 48, 22, 76, 125, 24, 83, 46, 80, 82, 44]:
            #    continue
            #print mid
            frequencies, intensities = get_peaks.get_frequency_intensity_list(conn, mid)#,
                                                                              #max=self.max_frequency,
                                                                              #min=0)
            #frequencies, intensities = get_peaks.get_frequency_intensity_list(conn, mid)
            distance, path = fastdtw(self.efreqlist, frequencies, dist=euclidean)

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


    def do_the_time_warp(self):
        self.__get_data__()
        self.__time_warp__()

    def __get_data__(self):

        # Get Experiment Frequencies
        self.efreqlist, self.eintelist = \
            get_peaks.get_frequency_intensity_list(conn, self.mid)

        # Get MAX and MIN
        self.max_frequency = get_peaks.get_max_frequency(conn, self.mid)
        self.min_frequency = get_peaks.get_min_frequency(conn, self.mid)
        # Get Candidates
       #self.candidates = get_molecules.get_mid_list(conn)
        self.get_candidates()

        print "Candidates: "
        print self.candidates
        print "\n"

    def get_candidates(self):
        from experiment import Experiment
        exp = Experiment("168-175-pzf1", self.mid, 0.5)
        exp.get_assigned_molecules()
        self.candidates = exp.get_assigned_mids()

    def __time_warp__(self):
        self.evaluate(self.candidates, 0)

    def evaluate(self, mid_list, i):

        # Base Case: Reached end of list
        if i == len(self.candidates):
            return

        new_list = []

        for j in range(i, len(mid_list)):
            new_list.append(mid_list[j])

            # Get frequencies of midlist union
            frequencies = get_peaks.get_frequencies_in_midlist(conn, new_list,
                                                               self.max_frequency,
                                                               self.min_frequency,)
            #print len(frequencies)
            # get current distance
            self.check_max_distance(frequencies, new_list)

        #print str(i)
        #print new_list
        #print "\n"
        self.evaluate(mid_list, i+1)

    def check_max_distance(self, frequencies, list):
        distance, path = fastdtw(self.efreqlist, frequencies, dist=euclidean)

        if self.min_distance is None:
            self.min_distance = distance
            self.min_path = path
            self.combination_list = list
        elif distance < self.min_distance:
            self.min_distance = distance
            self.min_path = path
            self.combination_list = list