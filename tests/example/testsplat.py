from astropy import units as u
from astroquery.splatalogue import Splatalogue

name = "2,4-Pentadiynylidyne"

columns = ('Species', 'Chemical Name')

freq = 11935.48
# freq *= 1000
max_freq = 11936.0
min_freq = 11935.0

rows = Splatalogue.query_lines(min_freq * u.GHz,
                               max_freq * u.GHz,
                               chemical_name=name)

rows.pprint()
for row in rows:
    print str(row[0]) + "  " + str(row[2])
