#!/usr/bin/env python

"""Unit tests for diffpy.utils.parsers.loaddata
"""

import unittest

import numpy
import pytest

from diffpy.utils.parsers import loadData


##############################################################################
class TestLoadData(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def prepare_fixture(self, datafile):
        self.datafile = datafile

    def test_loadData_default(self):
        """check loadData() with default options"""
        loaddata01 = self.datafile("loaddata01.txt")
        d2c = numpy.array([[3, 31], [4, 32], [5, 33]])
        self.assertRaises(IOError, loadData, "doesnotexist")
        # the default minrows=10 makes it read from the third line
        d = loadData(loaddata01)
        self.assertTrue(numpy.array_equal(d2c, d))
        # the usecols=(0, 1) would make it read from the third line
        d = loadData(loaddata01, minrows=1, usecols=(0, 1))
        self.assertTrue(numpy.array_equal(d2c, d))
        # check the effect of usecols effect
        d = loadData(loaddata01, usecols=(0,))
        self.assertTrue(numpy.array_equal(d2c[:, 0], d))
        d = loadData(loaddata01, usecols=(1,))
        self.assertTrue(numpy.array_equal(d2c[:, 1], d))
        return

    def test_loadData_1column(self):
        """check loading of one-column data."""
        loaddata01 = self.datafile("loaddata01.txt")
        d1c = numpy.arange(1, 6)
        d = loadData(loaddata01, usecols=[0], minrows=1)
        self.assertTrue(numpy.array_equal(d1c, d))
        d = loadData(loaddata01, usecols=[0], minrows=2)
        self.assertTrue(numpy.array_equal(d1c, d))
        d = loadData(loaddata01, usecols=[0], minrows=3)
        self.assertFalse(numpy.array_equal(d1c, d))
        return

    def test_loadData_headers(self):
        """check loadData() with headers options enabled"""
        loaddatawithheaders = self.datafile("loaddatawithheaders.txt")
        hignore = ["# ", "// ", "["]  # ignore lines beginning with these strings
        delimiter = ": "  # what our data should be separated by
        hdata = loadData(loaddatawithheaders, headers=True, hdel=delimiter, hignore=hignore)
        # only fourteen lines of data are formatted properly
        assert len(hdata) == 14
        # check the following are floats
        vfloats = ["wavelength", "qmaxinst", "qmin", "qmax", "bgscale"]
        for name in vfloats:
            assert isinstance(hdata.get(name), float)
        # check the following are NOT floats
        vnfloats = ["composition", "rmax", "rmin", "rstep", "rpoly"]
        for name in vnfloats:
            assert not isinstance(hdata.get(name), float)


# End of class TestRoutines

if __name__ == "__main__":
    unittest.main()

# End of file
