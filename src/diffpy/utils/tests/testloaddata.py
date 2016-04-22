#!/usr/bin/env python

"""Unit tests for diffpy.utils.parsers.loaddata
"""

import unittest
import numpy
from diffpy.utils.parsers import loadData
from diffpy.utils.tests.testhelpers import datafile

loaddata01 = datafile('loaddata01.txt')

##############################################################################
class TestLoadData(unittest.TestCase):

    def test_loadData_default(self):
        """check loadData() with default options
        """
        d2c = numpy.array([[3, 31], [4, 32], [5, 33]])
        self.assertRaises(IOError, loadData, 'doesnotexist')
        # the default minrows=10 makes it read from the third line
        d = loadData(loaddata01)
        self.failUnless(numpy.array_equal(d2c, d))
        # the usecols=(0, 1) would make it read from the third line
        d = loadData(loaddata01, minrows=1, usecols=(0, 1))
        self.failUnless(numpy.array_equal(d2c, d))
        # check the effect of usecols effect
        d = loadData(loaddata01, usecols=(0,))
        self.failUnless(numpy.array_equal(d2c[:,0], d))
        d = loadData(loaddata01, usecols=(1,))
        self.failUnless(numpy.array_equal(d2c[:,1], d))
        return


    def test_loadData_1column(self):
        """check loading of one-column data.
        """
        d1c = numpy.arange(1, 6)
        d = loadData(loaddata01, usecols=[0], minrows=1)
        self.failUnless(numpy.array_equal(d1c, d))
        d = loadData(loaddata01, usecols=[0], minrows=2)
        self.failUnless(numpy.array_equal(d1c, d))
        d = loadData(loaddata01, usecols=[0], minrows=3)
        self.failIf(numpy.array_equal(d1c, d))
        return

# End of class TestRoutines

if __name__ == '__main__':
    unittest.main()

# End of file
