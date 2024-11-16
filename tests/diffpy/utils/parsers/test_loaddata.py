#!/usr/bin/env python

"""Unit tests for diffpy.utils.parsers.loaddata
"""

import numpy as np
import pytest

from diffpy.utils.parsers.loaddata import loadData


def test_loadData_default(datafile):
    """check loadData() with default options"""
    loaddata01 = datafile("loaddata01.txt")
    d2c = np.array([[3, 31], [4, 32], [5, 33]])

    with pytest.raises(IOError):
        loadData("doesnotexist")

    # The default minrows=10 makes it read from the third line
    d = loadData(loaddata01)
    assert np.array_equal(d2c, d)

    # The usecols=(0, 1) would make it read from the third line
    d = loadData(loaddata01, minrows=1, usecols=(0, 1))
    assert np.array_equal(d2c, d)

    # Check the effect of usecols effect
    d = loadData(loaddata01, usecols=(0,))
    assert np.array_equal(d2c[:, 0], d)

    d = loadData(loaddata01, usecols=(1,))
    assert np.array_equal(d2c[:, 1], d)


def test_loadData_1column(datafile):
    """check loading of one-column data."""
    loaddata01 = datafile("loaddata01.txt")
    d1c = np.arange(1, 6)

    # Assertions using pytest's assert
    d = loadData(loaddata01, usecols=[0], minrows=1)
    assert np.array_equal(d1c, d)

    d = loadData(loaddata01, usecols=[0], minrows=2)
    assert np.array_equal(d1c, d)

    d = loadData(loaddata01, usecols=[0], minrows=3)
    assert not np.array_equal(d1c, d)


def test_loadData_headers(datafile):
    """check loadData() with headers options enabled"""
    loaddatawithheaders = datafile("loaddatawithheaders.txt")
    hignore = ["# ", "// ", "["]  # ignore lines beginning with these strings
    delimiter = ": "  # what our data should be separated by

    # Load data with headers
    hdata = loadData(loaddatawithheaders, headers=True, hdel=delimiter, hignore=hignore)

    # Only fourteen lines of data are formatted properly
    assert len(hdata) == 14

    # Check the following are floats
    vfloats = ["wavelength", "qmaxinst", "qmin", "qmax", "bgscale"]
    for name in vfloats:
        assert isinstance(hdata.get(name), float)

    # Check the following are NOT floats
    vnfloats = ["composition", "rmax", "rmin", "rstep", "rpoly"]
    for name in vnfloats:
        assert not isinstance(hdata.get(name), float)
