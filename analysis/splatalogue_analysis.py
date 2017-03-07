# Author: Jasmine Oliveira
# Date: 02/16/2017

from math import isnan

from astropy import units as u
from astroquery.splatalogue import Splatalogue

from config import conn
from tables import experimentinfo_table


class LineList:
    LOVAS = "Lovas"
    SLAIM = "SLAIM"
    JPL = "JPL"
    CDMS = "CDMS"
    TOYO_MA = "ToyoMA"
    OSU = "OSU"
    RECOMB = "Recomb"
    LISA = "Lisa"
    RFI = "RFI"


class SplatalogueAnalysis:
    def __init__(self, experiment):
        self.experiment = experiment
        self.chemicals = {}
        self.units = self.__determine_frequency_units()

    def find_matches(self, threshold=0.2):
        mid = self.experiment.mid
        if len(self.chemicals) > 0:
            self.chemicals.clear()
        frequencies, intensities = self.experiment.get_unvalidated_experiment_intensities_list()  # peaks_table.get_frequency_intensity_list(conn, mid)

        for i in range(0, len(frequencies)):

            ''' Query for Matches '''
            lines = self.query(frequencies[i] - threshold, frequencies[i] + threshold)

            added = []
            for row in lines:

                # Get row data
                name, full_name, freq, intensity, line_list = self.get_row_data(row)

                # If line already matched to chemical, skip
                if name in added:
                    continue

                # Create Line Object
                line = Line(freq, line_list, intensity)

                # If first time adding chemical, create a new Chemical object
                if not self.chemicals.has_key(name):
                    chemical = Chemical(name, full_name)
                    self.chemicals[row[0]] = chemical

                # Add Line to corresponding chemical
                self.chemicals[name].add_line(line, frequencies[i])

                added.append(name)  # add to 'added', to keep track of matches on this frequency

    def get_N_sorted_chemicals(self):

        import operator
        # Get Tuples
        sorted = self.chemicals.values()
        sorted.sort(key=operator.attrgetter('N'), reverse=True)

        return sorted

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

        if n == 0:
            return [], [], []

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

    def __determine_frequency_units(self):
        string = experimentinfo_table.get_units(conn, self.experiment.mid)

        if string is "MHz":
            return u.MHz
        elif string is "GHz":
            return u.GHz
        else:
            return u.MHz

    @staticmethod
    def query(low_freq, high_freq, chemical_name=None, line_list=[LineList.JPL, LineList.CDMS]):
        columns = ('Species', 'Chemical Name', 'Freq-GHz', 'Meas Freq-GHz', 'CDMS/JPL Intensity', 'Lovas/AST Intensity',
                   'Linelist')
        if chemical_name is not None:
            lines = Splatalogue.query_lines(low_freq * u.MHz, high_freq * u.MHz, chemical_name=chemical_name)[columns]
        else:
            lines = Splatalogue.query_lines(low_freq * u.MHz, high_freq * u.MHz, line_lists=line_list)[columns]

        return lines

    @staticmethod
    def get_row_data(row):
        """
        Parses and returns the values of a Splatalogue table row.
        The columns have the following:
            [Species] [Chemical Name] [Freq-GHz] [Meas Freq-GHz] [CDMS/JPL Intensity] [Lovas/AST Intensity] [Linelist]
        :param row: Splatalogue table tow
        :return string, string, float, float, string
        :return: name, full_name, freq, intensity, line_list
        """

        # Get Values #
        name = row[0]
        full_name = row[1]
        freq = row[2]
        intensity = row[4]
        line_list = row[6]

        # Determine Correct Frequency #
        if str(freq) == "--":
            if str(row[3]) == "--":
                freq = 0
            else:
                freq = float(str(row[3]))  # what is difference? meas freq-ghz vs freq-ghz
        freq = float(freq)  # Cast to Float
        freq *= 1000  # Convert to MHz (TEMPORARY)

        # Determine Correct Intensity #
        if str(intensity) == "--":
            intensity = row[5]

        if isnan(intensity):
            intensity = None
        else:
            intensity = float(intensity)  # Cast to Float
            if intensity < 0:
                intensity = abs(intensity) ** intensity  # |x|^x for actual value

        # Return Values
        return name, full_name, freq, intensity, line_list


class Chemical:
    """
    Representation of a 'matched' chemical in splatalogue
    """
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

    def get_all_lines(self, min_freq, max_freq, line_list=[LineList.JPL, LineList.CDMS]):
        columns = ('Species', 'Chemical Name', 'Freq-GHz', 'Meas Freq-GHz',
                   'CDMS/JPL Intensity', 'Lovas/AST Intensity', 'Linelist')

        rows = Splatalogue.query_lines(min_freq * u.MHz, max_freq * u.MHz, chemical_name=self.full_name,
                                       line_lists=line_list)[columns]
        lines = []
        for row in rows:
            name, full_name, frequency, intensity, line_list = SplatalogueAnalysis.get_row_data(row)
            if min_freq < frequency < max_freq:
                line = Line(frequency, line_list, intensity)
                print frequency
                lines.append(line)

        return lines


class Line:
    def __init__(self, frequency, linelist, intensity=None, units="MHz"):
        self.frequency = frequency
        self.linelist = linelist
        self.units = units
        self.intensity = intensity


class Columns(object):
    SPECIES = 'Species'
    CHEMICAL_NAME = 'Chemical Name'
    FREQ_GHZ = 'Freq-GHz'
    MEAS_FREQ_GHZ = 'Meas Freq-GHz',
    CDMS_JPL_INTENSITY = 'CDMS/JPL Intensity'
    LOVAS_AST_INTENSITY = 'Lovas/AST Intensity'
    LINE_LIST = 'Linelist'
