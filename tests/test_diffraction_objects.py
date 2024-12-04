import re
from pathlib import Path

import numpy as np
import pytest
from freezegun import freeze_time

from diffpy.utils.diffraction_objects import (
    ANGLEQUANTITIES,
    DQUANTITIES,
    QQUANTITIES,
    XQUANTITIES,
    DiffractionObject,
)


def compare_dicts(dict1, dict2):
    assert dict1.keys() == dict2.keys(), "Keys mismatch"
    for key in dict1:
        val1, val2 = dict1[key], dict2[key]
        if isinstance(val1, np.ndarray) and isinstance(val2, np.ndarray):
            assert np.allclose(val1, val2), f"Arrays for key '{key}' differ"
        elif isinstance(val1, np.float64) and isinstance(val2, np.float64):
            assert np.isclose(val1, val2), f"Float64 values for key '{key}' differ"
        else:
            assert val1 == val2, f"Values for key '{key}' differ: {val1} != {val2}"


def dicts_equal(dict1, dict2):
    equal = True
    print("")
    print(dict1)
    print(dict2)
    if not dict1.keys() == dict2.keys():
        equal = False
    for key in dict1:
        val1, val2 = dict1[key], dict2[key]
        if isinstance(val1, np.ndarray) and isinstance(val2, np.ndarray):
            if not np.allclose(val1, val2):
                equal = False
        elif isinstance(val1, list) and isinstance(val2, list):
            if not val1.all() == val2.all():
                equal = False
        elif isinstance(val1, np.float64) and isinstance(val2, np.float64):
            if not np.isclose(val1, val2):
                equal = False
        else:
            if not val1 == val2:
                equal = False
    return equal


params = [
    (  # Default
        {},
        {},
        True,
    ),
    (  # Compare same attributes
        {
            "name": "same",
            "scat_quantity": "x-ray",
            "wavelength": 0.71,
            "xtype": "q",
            "xarray": np.array([1.0, 2.0]),
            "yarray": np.array([100.0, 200.0]),
            "metadata": {"thing1": 1},
        },
        {
            "name": "same",
            "scat_quantity": "x-ray",
            "wavelength": 0.71,
            "xtype": "q",
            "xarray": np.array([1.0, 2.0]),
            "yarray": np.array([100.0, 200.0]),
            "metadata": {"thing1": 1},
        },
        True,
    ),
    (  # Different names
        {
            "name": "something",
            "scat_quantity": "",
            "wavelength": None,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        {
            "name": "something else",
            "scat_quantity": "",
            "wavelength": None,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        False,
    ),
    (  # Different wavelengths
        {
            "scat_quantity": "",
            "wavelength": 0.71,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        {
            "scat_quantity": "",
            "wavelength": None,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        False,
    ),
    (  # Different wavelengths
        {
            "scat_quantity": "",
            "wavelength": 0.71,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        {
            "scat_quantity": "",
            "wavelength": 0.711,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        False,
    ),
    (  # Different scat_quantity
        {
            "scat_quantity": "x-ray",
            "wavelength": None,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        {
            "scat_quantity": "neutron",
            "wavelength": None,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        False,
    ),
    (  # Different on_q
        {
            "scat_quantity": "",
            "wavelength": None,
            "xtype": "q",
            "xarray": np.array([1.0, 2.0]),
            "yarray": np.array([100.0, 200.0]),
            "metadata": {},
        },
        {
            "scat_quantity": "",
            "wavelength": None,
            "xtype": "q",
            "xarray": np.array([3.0, 4.0]),
            "yarray": np.array([100.0, 200.0]),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        False,
    ),
    (  # Different metadata
        {
            "scat_quantity": "",
            "wavelength": None,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 0, "thing2": "thing2"},
        },
        {
            "scat_quantity": "",
            "wavelength": None,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        False,
    ),
]


@pytest.mark.parametrize("inputs1, inputs2, expected", params)
def test_diffraction_objects_equality(inputs1, inputs2, expected):
    diffraction_object1 = DiffractionObject(**inputs1)
    diffraction_object2 = DiffractionObject(**inputs2)
    # diffraction_object1_attributes = [key for key in diffraction_object1.__dict__ if not key.startswith("_")]
    # for i, attribute in enumerate(diffraction_object1_attributes):
    #     setattr(diffraction_object1, attribute, inputs1[i])
    #     setattr(diffraction_object2, attribute, inputs2[i])
    print(dicts_equal(diffraction_object1.__dict__, diffraction_object2.__dict__), expected)
    assert dicts_equal(diffraction_object1.__dict__, diffraction_object2.__dict__) == expected


params_on_xtype = [
    (
        [
            np.array([100, 200, 300, 400, 500, 600]),  # intensity array
            np.array([0, 30, 60, 90, 120, 180]),  # tth array
            np.array([1, 2, 3, 4, 5, 6]),  # q array
            np.array([10, 20, 30, 40, 50, 60]),  # d array
        ],
        [
            np.array([[0, 30, 60, 90, 120, 180], [100, 200, 300, 400, 500, 600]]),  # expected on_tth
            np.array([[1, 2, 3, 4, 5, 6], [100, 200, 300, 400, 500, 600]]),  # expected on_q
            np.array([[10, 20, 30, 40, 50, 60], [100, 200, 300, 400, 500, 600]]),  # expected on_d
        ],
    )
]


@pytest.mark.parametrize("inputs, expected", params_on_xtype)
def test_on_xtype(inputs, expected):
    test = DiffractionObject()
    test.on_tth = np.array([inputs[1], inputs[0]])
    test.on_q = np.array([inputs[2], inputs[0]])
    test.on_d = np.array([inputs[3], inputs[0]])
    for xtype_list, expected_value in zip([ANGLEQUANTITIES, QQUANTITIES, DQUANTITIES], expected):
        for xtype in xtype_list:
            assert np.allclose(test.on_xtype(xtype), expected_value)


def test_on_xtype_bad():
    test = DiffractionObject()
    with pytest.raises(
        ValueError, match=re.escape(f"Unknown xtype: invalid. Allowed xtypes are {*XQUANTITIES, }.")
    ):
        test.on_xtype("invalid")


def test_dump(tmp_path, mocker):
    x, y = np.linspace(0, 5, 6), np.linspace(0, 5, 6)
    directory = Path(tmp_path)
    file = directory / "testfile"
    test = DiffractionObject(
        wavelength=1.54,
        name="test",
        scat_quantity="x-ray",
        xarray=np.array(x),
        yarray=np.array(y),
        xtype="q",
        metadata={"thing1": 1, "thing2": "thing2", "package_info": {"package2": "3.4.5"}},
    )
    mocker.patch("importlib.metadata.version", return_value="3.3.0")
    with freeze_time("2012-01-14"):
        test.dump(file, "q")
    with open(file, "r") as f:
        actual = f.read()
    expected = (
        "[DiffractionObject]\nname = test\nwavelength = 1.54\nscat_quantity = x-ray\nthing1 = 1\n"
        "thing2 = thing2\npackage_info = {'package2': '3.4.5', 'diffpy.utils': '3.3.0'}\n"
        "creation_time = 2012-01-14 00:00:00\n\n"
        "#### start data\n0.000000000000000000e+00 0.000000000000000000e+00\n"
        "1.000000000000000000e+00 1.000000000000000000e+00\n"
        "2.000000000000000000e+00 2.000000000000000000e+00\n"
        "3.000000000000000000e+00 3.000000000000000000e+00\n"
        "4.000000000000000000e+00 4.000000000000000000e+00\n"
        "5.000000000000000000e+00 5.000000000000000000e+00\n"
    )

    assert actual == expected


tc_params = [
    (
        {},
        {
            "all_arrays": np.empty(shape=(0, 4)),  # instantiate empty
            "metadata": {},
            "input_xtype": "",
            "name": "",
            "scat_quantity": None,
            "qmin": np.float64(np.inf),
            "qmax": np.float64(0.0),
            "tthmin": np.float64(np.inf),
            "tthmax": np.float64(0.0),
            "dmin": np.float64(np.inf),
            "dmax": np.float64(0.0),
            "wavelength": None,
        },
    ),
    (  # instantiate just non-array attributes
        {"name": "test", "scat_quantity": "x-ray", "metadata": {"thing": "1", "another": "2"}},
        {
            "all_arrays": np.empty(shape=(0, 4)),
            "metadata": {"thing": "1", "another": "2"},
            "input_xtype": "",
            "name": "test",
            "scat_quantity": "x-ray",
            "qmin": np.float64(np.inf),
            "qmax": np.float64(0.0),
            "tthmin": np.float64(np.inf),
            "tthmax": np.float64(0.0),
            "dmin": np.float64(np.inf),
            "dmax": np.float64(0.0),
            "wavelength": None,
        },
    ),
    (  # instantiate just array attributes
        {
            "xarray": np.array([0.0, 90.0, 180.0]),
            "yarray": np.array([1.0, 2.0, 3.0]),
            "xtype": "tth",
            "wavelength": 4.0 * np.pi,
        },
        {
            "all_arrays": np.array(
                [
                    [1.0, 0.0, 0.0, np.float64(np.inf)],
                    [2.0, 1.0 / np.sqrt(2), 90.0, np.sqrt(2) * 2 * np.pi],
                    [3.0, 1.0, 180.0, 1.0 * 2 * np.pi],
                ]
            ),
            "metadata": {},
            "input_xtype": "tth",
            "name": "",
            "scat_quantity": None,
            "qmin": np.float64(0.0),
            "qmax": np.float64(1.0),
            "tthmin": np.float64(0.0),
            "tthmax": np.float64(180.0),
            "dmin": np.float64(2 * np.pi),
            "dmax": np.float64(np.inf),
            "wavelength": 4.0 * np.pi,
        },
    ),
    (  # instantiate just array attributes
        {
            "xarray": np.array([np.inf, 2 * np.sqrt(2) * np.pi, 2 * np.pi]),
            "yarray": np.array([1.0, 2.0, 3.0]),
            "xtype": "d",
            "wavelength": 4.0 * np.pi,
            "scat_quantity": "x-ray",
        },
        {
            "all_arrays": np.array(
                [
                    [1.0, 0.0, 0.0, np.float64(np.inf)],
                    [2.0, 1.0 / np.sqrt(2), 90.0, np.sqrt(2) * 2 * np.pi],
                    [3.0, 1.0, 180.0, 1.0 * 2 * np.pi],
                ]
            ),
            "metadata": {},
            "input_xtype": "d",
            "name": "",
            "scat_quantity": "x-ray",
            "qmin": np.float64(0.0),
            "qmax": np.float64(1.0),
            "tthmin": np.float64(0.0),
            "tthmax": np.float64(180.0),
            "dmin": np.float64(2 * np.pi),
            "dmax": np.float64(np.inf),
            "wavelength": 4.0 * np.pi,
        },
    ),
]


@pytest.mark.parametrize("inputs, expected", tc_params)
def test_constructor(inputs, expected):
    actualdo = DiffractionObject(**inputs)
    compare_dicts(actualdo.__dict__, expected)
