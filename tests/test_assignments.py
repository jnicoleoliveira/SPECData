# Author: Jasmine Oliveira
# Date: 7/5/2016
# Test Peak Assignment

from config import *
from functions.assign_peaks import *
from tables.remove import remove_assignments


#print "Enter pid: "
#pid = raw_input()

# Connect to sqlite database
conn = sqlite3.connect(db_filepath)
cursor = conn.cursor()

mid = 157 # EXP 168-1
# 75

# Remove all assignments
remove_assignments.remove_all(conn, mid)
print "REMOVED ASSIGNMENTS. Press enter to continue, and re-assign."
balfsa = raw_input()

# Try
#assign_peaks.get_candidates(conn, 496.799)
list = assign_peaks(conn, 155)
#midlist = [3, 7, 13, 10, 13]
#assign_from_list(conn, 153, midlist)

distinct = []
freq = []
for name in list:
    if(distinct.__contains__(name) is False):
        distinct.append(str(name))
        freq.append(1)
    else:
        index = distinct.index(name)
        freq[index] += 1
i=0
for d in distinct:
    print str(freq[i]) + "   " + str(d)
    i+=1

print len(distinct)