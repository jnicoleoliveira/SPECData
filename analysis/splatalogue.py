# Author: Jasmine Oliveira
# Date: 02/16/2017

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


