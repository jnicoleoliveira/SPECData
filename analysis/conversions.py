# -----------------------------------------------------------------------------
# Author: Jasmine Oliveira
# Date:   11/21/2016
# -----------------------------------------------------------------------------
# conversions.py
# -----------------------------------------------------------------------------
# Module designed to hold conversion functions needed for SPECdata.
#
#       Public Functions:
#           * fahrenheit_to_kelvin(t)
#           * celsius_to_kelvin(t)
#


def fahrenheit_to_kelvin(t):
    return ((t - 32) * 5/9) + 273.15


def celsius_to_kelvin(t):
    return t + 273
