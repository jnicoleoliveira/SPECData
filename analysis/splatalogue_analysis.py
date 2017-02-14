from astroquery.splatalogue import Splatalogue
from astropy import units as u
from tables import peaks_table
from config import conn

line_ids = Splatalogue.get_species_ids()

# --- Find species that have CO --- #
CO_containing_species = Splatalogue.get_species_ids('CHS')
print CO_containing_species

# -- Find Species within lines -- #
CO1to0 = Splatalogue.query_lines(115.271*u.GHz,115.273*u.GHz, top20='top20')
CO1to0.pprint()
row = CO1to0[0]
#print row[1]

mid = 122
threshold = 0.2
frequencies, intensities = peaks_table.get_frequency_intensity_list(conn, mid)


class Chemical:
    def __init__(self, name):
        self.name = name
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)

class Line:
    def __init__(self, frequency, linelist, units="MHz"):
        self.frequency = frequency
        self.linelist = linelist
        self.units = units


chemicals = {}
for i in range(0, len(frequencies)):
    low_freq = frequencies[i]-threshold
    high_freq = frequencies[i]+threshold

    lines = Splatalogue.query_lines(low_freq*u.MHz, high_freq*u.MHz)

    for row in lines:
        name = row[1]
        freq = row[2]
        line_list = row[7]

        line = Line(freq, line_list)

        if not chemicals.has_key(name):
            chemical = Chemical(name)
            chemicals[row[1]] = chemical
            print name

        chemicals[name].add_line(line)

for key, value in chemicals:
    print "Name: " + value.name + len(value.lines)
    print "----------------------------"
