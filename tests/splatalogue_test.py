from astropy import units as u
from astroquery.splatalogue import Splatalogue

from config import conn
from tables import peaks_table

line_ids = Splatalogue.get_species_ids()

# --- Find species that have CO --- #
# CO_containing_species = Splatalogue.get_species_ids('CHS')
# print CO_containing_species

# -- Find Species within lines -- #
# CO1to0 = Splatalogue.query_lines(115.271 * u.GHz, 115.273 * u.GHz, top20='top20')
# CO1to0.pprint()
# row = CO1to0[0]
# print row[1]

mid = 122
threshold = 0.02
frequencies, intensities = peaks_table.get_frequency_intensity_list(conn, mid)


class Chemical:
    def __init__(self, name):
        self.name = name
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

chemicals = {}
for i in range(0, len(frequencies)):
    low_freq = frequencies[i] - threshold
    high_freq = frequencies[i] + threshold

    lines = Splatalogue.query_lines(low_freq * u.MHz, high_freq * u.MHz)
    lines.pprint(max_width=300)
    # if len(lines) > 0: print "\n\nFREQUENCY==========" + str(frequencies[i])

    added = []
    for row in lines:
        # print row
        name = row[0]
        freq = row[2] * 1000
        if str(freq) == "--":  # or abs(frequencies[0]-freq)>threshold:
            freq = float(str(row[4])) * 1000.0

        line_list = row[7]

        if name in added: continue

        line = Line(freq, line_list)

        if not chemicals.has_key(name):
            chemical = Chemical(name)
            chemicals[row[0]] = chemical

        chemicals[name].add_line(line, frequencies[i])
        added.append(name)

total = 0
n = 0
for key, value in chemicals.iteritems():
    print "Name: " + value.name + "\nN=" + str(len(value.lines))
    for i in range(0, len(value.lines)):
        print "L: " + str(value.lines[i].frequency) + " M:" + str(value.matched_lines[i])
    print "----------------------------"
    n += 1
    total += (len(value.lines))

average = total / n

above_average = []
below_average = []
median_average = []
print "AVERAGE # == " + str(average) + "************"
print "MATCHES == " + str(len(chemicals)) + "************"

for key, value in chemicals.iteritems():
    N = value.N
    if N > average:
        above_average.append(value)
    else:
        below_average.append(value)
n = 0
total = 0
for v in above_average:
    n += 1
    total += v.N
    # print str(v.N) + "   " + str(v.name)
average = total / n
most_likely = []
likely = []
for v in above_average:
    if v.N > average:
        most_likely.append(v)
    else:
        likely.append(v)

print "********* MOST LIKELY ***********"
for v in most_likely:
    print str(v.N) + "   " + str(v.name)
print "********* LIKELY ***********"
for v in likely:
    print str(v.N) + "   " + str(v.name)
print "********* LEAST LIKELY ***********"
for v in below_average:
    print str(v.N) + "   " + str(v.name)

# low_freq = peaks_table.get_min_frequency(conn, mid)
# high_freq = peaks_table.get_max_frequency(conn, mid)
# c = "Cyanomethyl"
#
# lines = Splatalogue.query_lines(low_freq * u.MHz, high_freq * u.MHz, chemical_name=c)
# lines.pprint()
#
# for row in lines:
#     print str(row[0]) + "  " + str(row[2])
