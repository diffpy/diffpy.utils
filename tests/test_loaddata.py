#!/usr/bin/env python

"""Unit tests for diffpy.utils.parsers.loaddata."""

import numpy as np
import pytest

from diffpy.utils.parsers.loaddata import loadData


def test_loadData_default(datafile):
    """Check loadData() with default options."""
    loaddata01 = datafile("loaddata01.txt")
    d2c = np.array([[3, 31], [4, 32], [5, 33]])

    with pytest.raises(IOError) as err:
        loadData("doesnotexist.txt")
    assert str(err.value) == (
        "File doesnotexist.txt cannot be found. "
        "Please rerun the program specifying a valid filename."
    )

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
    """Check loading of one-column data."""
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
    """Check loadData() with headers options enabled."""
    expected = {
        "wavelength": 0.1,
        "dataformat": "Qnm",
        "inputfile": "darkSub_rh20_C_01.chi",
        "mode": "xray",
        "bgscale": 1.2998929285,
        "composition": "0.800.20",
        "outputtype": "gr",
        "qmaxinst": 25.0,
        "qmin": 0.1,
        "qmax": 25.0,
        "rmax": "100.0r",
        "rmin": "0.0r",
        "rstep": "0.01r",
        "rpoly": "0.9r",
    }

    loaddatawithheaders = datafile("loaddatawithheaders.txt")
    hignore = ["# ", "// ", "["]  # ignore lines beginning with these strings
    delimiter = ": "  # what our data should be separated by

    # Load data with headers
    hdata = loadData(
        loaddatawithheaders, headers=True, hdel=delimiter, hignore=hignore
    )
    assert hdata == expected
