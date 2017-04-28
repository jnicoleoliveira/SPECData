# string = "940.00149,0.01069"
#
#
# point = string.split(',')
#
# print float(point[0])
# print float(point[1])
import re

line = "ftmfreq:16843.000 shots:100 dipole:1.00 #intensity 2.683e-01"
delimiters = ["ftmfreq:", "shots:", "dipole:", " ", "#intensity ", ""]
regex = '|'.join((map(re.escape, delimiters)))
point = re.split(regex, line.strip())
print point
