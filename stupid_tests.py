# Author: Jasmine Oliveira
# Date: 7/7/2016
# Test Peak Assignment


import sqlite3
from config import *

# Connect to sqlite database
conn = sqlite3.connect(db_filepath)
cursor = conn.cursor()

cursor.execute("SELECT frequency FROM peaks WHERE mid=153")
rows = cursor.fetchall()

integers = []
for row in rows:
    #freq = int(round(row[0],-1))
    
    if integers.__contains__(freq) is False:
        integers.append(freq)
        print freq

print "COUNT: " + str(len(integers))


