from pathlib import Path

import numpy as np
import pytest
from freezegun import freeze_time

from diffpy.utils.scattering_objects.diffraction_objects import Diffraction_object

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
    diffraction_object1 = Diffraction_object()
    diffraction_object2 = Diffraction_object()
    diffraction_object1_attributes = [key for key in diffraction_object1.__dict__ if not key.startswith("_")]
    for i, attribute in enumerate(diffraction_object1_attributes):
        setattr(diffraction_object1, attribute, inputs1[i])
        setattr(diffraction_object2, attribute, inputs2[i])
    assert (diffraction_object1 == diffraction_object2) == expected


def test_dump(tmp_path, mocker):
    x, y = np.linspace(0, 10, 11), np.linspace(0, 10, 11)
    directory = Path(tmp_path)
    file = directory / "testfile"
    test = Diffraction_object()
    test.wavelength = 1.54
    test.name = "test"
    test.scat_quantity = "x-ray"
    test.insert_scattering_quantity(
        x, y, "q", metadata={"thing1": 1, "thing2": "thing2", "package_info": {"package2": "3.4.5"}}
    )
    with mocker.patch("importlib.metadata.version", return_value="3.3.0"), freeze_time("2012-01-14"):
        test.dump(file, "q")
    with open(file, "r") as f:
        actual = f.read()
    expected = (
        "[Diffraction_object]\nname = test\nwavelength = 1.54\nscat_quantity = x-ray\nthing1 = 1\n"
        "thing2 = thing2\npackage_info = {'package2': '3.4.5', 'diffpy.utils': '3.3.0'}\n"
        "creation_time = 2012-01-14 00:00:00\n\n"
        "#### start data\n0.000000000000000000e+00 0.000000000000000000e+00\n"
        "1.000000000000000000e+00 1.000000000000000000e+00\n"
        "2.000000000000000000e+00 2.000000000000000000e+00\n"
        "3.000000000000000000e+00 3.000000000000000000e+00\n"
        "4.000000000000000000e+00 4.000000000000000000e+00\n"
        "5.000000000000000000e+00 5.000000000000000000e+00\n"
        "6.000000000000000000e+00 6.000000000000000000e+00\n"
        "7.000000000000000000e+00 7.000000000000000000e+00\n"
        "8.000000000000000000e+00 8.000000000000000000e+00\n"
        "9.000000000000000000e+00 9.000000000000000000e+00\n"
        "1.000000000000000000e+01 1.000000000000000000e+01\n"
    )
    assert actual == expected
