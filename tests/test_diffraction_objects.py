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

params = [
    (  # Default
        [
            "",
            None,
            "",
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            {},
        ],
        [
            "",
            None,
            "",
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            {},
        ],
        True,
    ),
    (  # Compare same attributes
        [
            "test",
            0.71,
            "x-ray",
            [np.array([1, 2]), np.array([3, 4])],
            [np.array([1, 2]), np.array([3, 4])],
            [np.array([1, 2]), np.array([3, 4])],
            {"thing1": 1, "thing2": "thing2"},
        ],
        [
            "test",
            0.7100001,
            "x-ray",
            [np.array([1.00001, 2.00001]), np.array([3.00001, 4.00001])],
            [np.array([1.00001, 2.00001]), np.array([3.00001, 4.00001])],
            [np.array([1.00001, 2.00001]), np.array([3.00001, 4.00001])],
            {"thing1": 1, "thing2": "thing2"},
        ],
        True,
    ),
    (  # Different names
        [
            "test1",
            None,
            "",
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            {},
        ],
        [
            "test2",
            None,
            "",
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            {},
        ],
        False,
    ),
    (  # Different wavelengths
        [
            "",
            0.71,
            "",
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            {},
        ],
        [
            "",
            0.711,
            "",
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            {},
        ],
        False,
    ),
    (  # Different wavelengths
        [
            "",
            0.71,
            "",
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            {},
        ],
        [
            "",
            None,
            "",
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            {},
        ],
        False,
    ),
    (  # Different scat_quantity
        [
            "",
            None,
            "",
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            {},
        ],
        [
            "",
            None,
            "x-ray",
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            {},
        ],
        False,
    ),
    (  # Different on_q
        [
            "",
            None,
            "",
            [np.array([1, 2]), np.array([3, 4])],
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            {},
        ],
        [
            "",
            None,
            "",
            [np.array([1.01, 2]), np.array([3, 4])],
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            {},
        ],
        False,
    ),
    (  # Different on_tth
        [
            "",
            None,
            "",
            [np.empty(0), np.empty(0)],
            [np.array([1, 2]), np.array([3, 4])],
            [np.empty(0), np.empty(0)],
            {},
        ],
        [
            "",
            None,
            "",
            [np.empty(0), np.empty(0)],
            [np.array([1.01, 2]), np.array([3, 4])],
            [np.empty(0), np.empty(0)],
            {},
        ],
        False,
    ),
    (  # Different on_d
        [
            "",
            None,
            "",
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            [np.array([1, 2]), np.array([3, 4])],
            {},
        ],
        [
            "",
            None,
            "",
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            [np.array([1.01, 2]), np.array([3, 4])],
            {},
        ],
        False,
    ),
    (  # Different metadata
        [
            "",
            None,
            "",
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            {"thing1": 0, "thing2": "thing2"},
        ],
        [
            "",
            None,
            "",
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            [np.empty(0), np.empty(0)],
            {"thing1": 1, "thing2": "thing2"},
        ],
        False,
    ),
]


@pytest.mark.parametrize("inputs1, inputs2, expected", params)
def test_diffraction_objects_equality(inputs1, inputs2, expected):
    diffraction_object1 = DiffractionObject()
    diffraction_object2 = DiffractionObject()
    diffraction_object1_attributes = [key for key in diffraction_object1.__dict__ if not key.startswith("_")]
    for i, attribute in enumerate(diffraction_object1_attributes):
        setattr(diffraction_object1, attribute, inputs1[i])
        setattr(diffraction_object2, attribute, inputs2[i])
    assert (diffraction_object1 == diffraction_object2) == expected


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
    test = DiffractionObject()
    test.wavelength = 1.54
    test.name = "test"
    test.scat_quantity = "x-ray"
    test.insert_scattering_quantity(
        np.array(x),
        np.array(y),
        "q",
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
