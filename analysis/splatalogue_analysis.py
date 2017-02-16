from astropy import units as u
from astroquery.splatalogue import Splatalogue

from config import conn
from tables import peaks_table

line_ids = Splatalogue.get_species_ids()

# --- Find species that have CO --- #
CO_containing_species = Splatalogue.get_species_ids('CHS')
print CO_containing_species

# -- Find Species within lines -- #
CO1to0 = Splatalogue.query_lines(115.271 * u.GHz, 115.273 * u.GHz, top20='top20')
CO1to0.pprint()
row = CO1to0[0]
# print row[1]

mid = 122
threshold = 0.02
frequencies, intensities = peaks_table.get_frequency_intensity_list(conn, mid)


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


chemicals = {}
for i in range(0, len(frequencies)):
    low_freq = frequencies[i] - threshold
    high_freq = frequencies[i] + threshold

    lines = Splatalogue.query_lines(low_freq * u.MHz, high_freq * u.MHz)
    print "FREQUENCY==========" + str(frequencies[i])
    for row in lines:
        print row
        name = row[0]
        freq = row[2]
        if str(freq) == "--":  # or abs(frequencies[0]-freq)>threshold:
            freq = float(row[4]) * 1000.0

        line_list = row[7]

        line = Line(freq, line_list)

        if not chemicals.has_key(name):
            chemical = Chemical(name)
            chemicals[row[0]] = chemical

        chemicals[name].add_line(line, frequencies[i])

for key, value in chemicals.iteritems():
    print "Name: " + value.name + "\nN=" + str(len(value.lines))
    for i in range(0, len(value.lines)):
        print "L: " + str(value.lines[i].frequency) + " M:" + str(value.matched_lines[i])

    print "----------------------------"
