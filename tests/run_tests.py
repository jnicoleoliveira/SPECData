import unittest

from tests.unit import test___user_imports

suite = unittest.TestLoader().loadTestsFromModule(test___user_imports)
results = unittest.TextTestRunner(verbosity=2).run(suite)
