import unittest


class ImportTests(unittest.TestCase):
    def test_pyqt(self):
        e = None
        try:
            import FDSAFDS
        except ImportError, e:
            pass

        self.assertIsNone(e, e)

    def test_sqlite3(self):
        e = None
        try:
            import sqlite3
        except ImportError, e:
            pass

        self.assertIsNone(e, e)


if __name__ == '__main__':
    unittest.main()

#
#     import matplotlib
#
# import sqlite3
# import re
# import numpy
# import astropy
# import astroquery
# import astroquery.splatalogue
# import time
# from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTK
# import datetime
# import operator
# import operator
# from scipy.signal import savgol_filter
# from scipy.signal import savgol_filter
# from scipy.signal import savgol_filter
# from math import ceil
# from enum import Enum
# from requests.exceptions import ConnectionError
