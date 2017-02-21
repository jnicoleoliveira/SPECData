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
        threshold = 0.02
        frequencies, intensities = peaks_table.get_frequency_intensity_list(conn, mid)

        for i in range(0, len(frequencies)):
            low_freq = frequencies[i] - threshold
            high_freq = frequencies[i] + threshold

            columns = ['Species', 'Chemical Name', 'Freq-MHz',
                       'CDMS/JPL Intensity', 'Linelist']
            lines = Splatalogue.query_lines(low_freq * u.MHz, high_freq * u.MHz)

            added = []
            for row in lines:

                # print row,
                name = row[0]
                full_name = row[1]
                freq = row[2] * 1000  # NEED BETTER CONVERSION
                intensity = row[10]

                if str(freq) == "--":
                    freq = float(str(row[4])) * 1000.0

                line_list = row[3]

                if name in added:
                    continue

                line = Line(freq, line_list, intensity)

                if not self.chemicals.has_key(name):
                    chemical = Chemical(name, full_name)
                    self.chemicals[row[0]] = chemical

                self.chemicals[name].add_line(line, frequencies[i])
                added.append(name)

    def get_N_sorted_chemicals(self):

        import operator
        # Get Tuples
        sorted = self.chemicals.values()
        sorted.sort(key=operator.attrgetter('N'), reverse=True)

        return sorted

    def __determine_frequency_units(self):
        string = experimentinfo_table.get_units(conn, self.experiment.mid)

        if string is "MHz":
            return u.MHz
        elif string is "GHz":
            return u.GHz
        else:
            return u.MHz

    def get_likelihood_chemical_lists(self):
        chemicals = self.get_N_sorted_chemicals()
        most_likely = []
        likely = []
        least_likely = []

        n = 0
        total = 0
        for c in chemicals:
            n += 1
            total += c.N

        average = total / n
        total = 0
        n = 0
        a = []
        for c in chemicals:
            if c.N > average:
                a.append(c)
                n += 1
                total += c.N
            else:
                least_likely.append(c)

        if n is not 0:
            average = total / n
            for c in a:
                if c.N > average:
                    most_likely.append(c)
                else:
                    likely.append(c)

        return most_likely, likely, least_likely

class Chemical:
    def __init__(self, name, full_name):
        self.name = name
        self.full_name = full_name
        self.lines = []
        self.matched_lines = []
        self.N = 0

    def add_line(self, line, match):
        self.lines.append(line)
        self.matched_lines.append(match)
        self.N += 1


class Line:
    def __init__(self, frequency, linelist, intensity=None, units="MHz"):
        self.frequency = frequency
        self.linelist = linelist
        self.units = units
        self.intensity = intensity
