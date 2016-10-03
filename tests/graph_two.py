# jasmine Oliveira
# Date: 09/20/2016
import matplotlib.pyplot as plot
from tables.get import get_peaks
from config import conn

print "Enter first graph MID:"
mid1 = raw_input()

print "Enter second graph MID:"
mid2 = raw_input()

print "Graphing..."

freq1, inte1 = get_peaks.get_frequency_intensity_list(conn, mid1)
freq2, inte2 = get_peaks.get_frequency_intensity_list(conn, mid2)

subplot2 = plot.subplot(212)
subplot1 = plot.subplot(211,  sharex=subplot2)


subplot1.bar(freq1, inte1)
subplot2.bar(freq2, inte2)

# Set Labels
rects = subplot2.patches
labels = ["%d" % i for i in xrange(len(rects))]

for rect, label in zip(rects, labels):
    height = rect.get_height()
    subplot2.text(rect.get_x() + rect.get_width()/2, height + 0.02, label, ha='center', va='bottom')



plot.show()