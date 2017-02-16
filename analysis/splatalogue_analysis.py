# Author: Jasmine Oliveira
# Date: 02/16/2017

from astropy import units as u
from astroquery.splatalogue import Splatalogue

from config import conn
from tables import peaks_table, experimentinfo_table


class SplatalogueAnalysis():
    def __init__(self, experiment):
        self.experiment = experiment
        self.chemicals = {}
        self.units = self.__determine_frequency_units()

    def find_matches(self):
        mid = self.experiment.mid
        threshold = self.experiment.match_threshold
        frequencies, intensities = peaks_table.get_frequency_intensity_list(conn, mid)

        for i in range(0, len(frequencies)):
            low_freq = frequencies[i] - threshold
            high_freq = frequencies[i] + threshold

            lines = Splatalogue.query_lines(low_freq * u.MHz, high_freq * u.MHz)

            added = []
            for row in lines:
                # print row
                name = row[0]
                freq = row[2] * 1000  ### NEED BETTER CONVERSION HERE
                if str(freq) == "--":
                    freq = float(str(row[4])) * 1000.0

                line_list = row[7]

                if name in added: continue

                line = Line(freq, line_list)

                if not self.chemicals.has_key(name):
                    chemical = Chemical(name)
                    self.chemicals[row[0]] = chemical

                self.chemicals[name].add_line(line, frequencies[i])
                added.append(name)

    def __determine_frequency_units(self):
        string = experimentinfo_table.get_units(conn, self.experiment.mid)

        if string is "MHz":
            return u.MHz
        elif string is "GHz":
            return u.GHz
        else:
            print "SHOULD THROW ERROR HERE. UNSUPPORTED UNIT TYPE!"


class Chemical:
    def __init__(self, name):
        self.name = name
        self.lines = []
        self.matched_lines = []

    def add_line(self, line, match):
        self.lines.append(line)
        self.matched_lines.append(match)


class Line:
    def __init__(self, frequency, linelist, units="MHz"):
        self.frequency = frequency
        self.linelist = linelist
        self.units = units
