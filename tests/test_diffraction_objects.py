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


def test_q_to_tth():
    actual = Diffraction_object(wavelength=4 * np.pi)
    setattr(actual, "on_q", [[0, 0.2, 0.4, 0.6, 0.8, 1], [1, 2, 3, 4, 5, 6]])
    actual_tth = actual.q_to_tth()
    # expected tth values are 2 * arcsin(q)
    expected_tth = [0, 23.07392, 47.15636, 73.73980, 106.26020, 180]
    assert np.allclose(actual_tth, expected_tth)


def test_tth_to_q():
    actual = Diffraction_object(wavelength=4 * np.pi)
    setattr(actual, "on_tth", [[0, 30, 60, 90, 120, 180], [1, 2, 3, 4, 5, 6]])
    actual_q = actual.tth_to_q()
    # expected q vales are sin15, sin30, sin45, sin60, sin90
    expected_q = [0, 0.258819, 0.5, 0.707107, 0.866025, 1]
    assert np.allclose(actual_q, expected_q)


def test_q_to_d():
    actual = Diffraction_object(wavelength=0.71)
    setattr(actual, "on_q", [[0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi, 5 * np.pi], [1, 2, 3, 4, 5, 6]])
    actual_d = actual.q_to_d()
    # expected d values are DMAX=100, 2/1, 2/2, 2/3, 2/4, 2/5, and in reverse order
    expected_d = [0.4, 0.5, 0.66667, 1, 2, 100]
    assert np.allclose(actual_d, expected_d)


def test_d_to_q():
    actual = Diffraction_object(wavelength=1)
    setattr(actual, "on_d", [[0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi, 5 * np.pi], [1, 2, 3, 4, 5, 6]])
    actual_q = actual.d_to_q()
    # expected q values are QMAX=40, 2/1, 2/2, 2/3, 2/4, 2/5, and in reverse order
    expected_q = [0.4, 0.5, 0.66667, 1, 2, 40]
    assert np.allclose(actual_q, expected_q)


def test_tth_to_d():
    actual = Diffraction_object(wavelength=0.71)
    setattr(actual, "on_tth", [[0, 30], [1, 1]])
    actual_d = actual.tth_to_d()
    expected_d = [3550000000, 1.37161]
    assert np.allclose(actual_d, expected_d)


def test_d_to_tth():
    actual = Diffraction_object(wavelength=0.71)
    setattr(actual, "on_d", [[1e10, 1.37161], [1, 1]])
    actual_tth = actual.d_to_tth()
    expected_tth = [0, 30]
    assert np.allclose(actual_tth, expected_tth)


params_array = [
    (["q", "on_q", [4.58087, 8.84956], [1, 2]]),
    (["tth", "on_tth", [30, 60], [1, 2]]),
    (["d", "on_d", [1.37161, 0.71], [1, 2]]),
]


@pytest.mark.parametrize("inputs", params_array)
def test_set_all_arrays(inputs):
    input_xtype, on_xtype, xarray, yarray = inputs
    expected_values = {
        "on_tth": [np.array([30, 60]), np.array([1, 2])],
        "on_q": [np.array([4.58087, 8.84956]), np.array([1, 2])],
        "on_d": [np.array([1.37161, 0.71]), np.array([1, 2])],
        "tthmin": 30,
        "tthmax": 60,
        "qmin": 4.58087,
        "qmax": 8.84956,
        "dmin": 1.37161,
        "dmax": 0.71,
    }

    actual = Diffraction_object(wavelength=0.71)
    setattr(actual, "input_xtype", input_xtype)
    setattr(actual, on_xtype, [xarray, yarray])
    actual.set_all_arrays()
    for attr, expected in expected_values.items():
        actual_value = getattr(actual, attr)
        assert np.allclose(actual_value, expected)


def test_dump(tmp_path, mocker):
    x, y = np.linspace(0, 5, 6), np.linspace(0, 5, 6)
    directory = Path(tmp_path)
    file = directory / "testfile"
    test = Diffraction_object()
    test.wavelength = 1.54
    test.name = "test"
    test.scat_quantity = "x-ray"
    test.insert_scattering_quantity(
        x, y, "q", metadata={"thing1": 1, "thing2": "thing2", "package_info": {"package2": "3.4.5"}}
    )

    mocker.patch("importlib.metadata.version", return_value="3.3.0")

    with freeze_time("2012-01-14"):
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
    )

    assert actual == expected
