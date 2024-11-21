from pathlib import Path

import numpy as np
import pytest
from freezegun import freeze_time

from diffpy.utils.scattering_objects.diffraction_objects import DiffractionObject

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


def test_q_to_tth():
    # Valid q values that should result in 0-180 tth values after conversion
    # expected tth values are 2*arcsin(q) in degrees
    actual = DiffractionObject(wavelength=4 * np.pi)
    setattr(actual, "on_q", [[0, 0.2, 0.4, 0.6, 0.8, 1], [1, 2, 3, 4, 5, 6]])
    actual_tth = actual.q_to_tth()
    expected_tth = [0, 23.07392, 47.15636, 73.73980, 106.26020, 180]
    assert np.allclose(actual_tth, expected_tth)


params_q_to_tth_bad = [
    # UC1: user did not specify wavelength
    (
        [None, [0, 0.2, 0.4, 0.6, 0.8, 1]],
        "Wavelength is not specified. Please provide a valid wavelength, "
        "e.g., DiffractionObject(wavelength=0.71).",
    ),
    # UC2: user specified invalid q values that result in tth > 180 degrees
    (
        [4 * np.pi, [0.2, 0.4, 0.6, 0.8, 1, 1.2]],
        "Wavelength * q > 4 * pi. Please check if you entered an incorrect wavelength or q value.",
    ),
    # UC3: user specified a wrong wavelength that result in tth > 180 degrees
    (
        [100, [0, 0.2, 0.4, 0.6, 0.8, 1]],
        "Wavelength * q > 4 * pi. Please check if you entered an incorrect wavelength or q value.",
    ),
    # UC4: user specified an empty q array
    ([4 * np.pi, []], "Q array is empty. Please provide valid q values."),
    # UC5: user specified a non-numeric value in q array
    (
        [4 * np.pi, [0, 0.2, 0.4, 0.6, 0.8, "invalid"]],
        "Invalid value found in q array. Please ensure all values are numeric.",
    ),
]


@pytest.mark.parametrize("inputs, expected", params_q_to_tth_bad)
def test_q_to_tth_bad(inputs, expected):
    actual = DiffractionObject(wavelength=inputs[0])
    setattr(actual, "on_q", [inputs[1], [1, 2, 3, 4, 5, 6]])
    with pytest.raises(ValueError):
        actual.q_to_tth()


def test_tth_to_q():
    # Valid tth values between 0-180 degrees
    # expected q vales are sin15, sin30, sin45, sin60, sin90
    actual = DiffractionObject(wavelength=4 * np.pi)
    setattr(actual, "on_tth", [[0, 30, 60, 90, 120, 180], [1, 2, 3, 4, 5, 6]])
    actual_q = actual.tth_to_q()
    expected_q = [0, 0.258819, 0.5, 0.707107, 0.866025, 1]
    assert np.allclose(actual_q, expected_q)


params_tth_to_q_bad = [
    # UC1: user did not specify wavelength
    (
        [None, [0, 30, 60, 90, 120, 180]],
        "Wavelength is not specified. Please provide a valid wavelength, "
        "e.g., DiffractionObject(wavelength=0.71).",
    ),
    # UC2: user specified an invalid tth value of > 180 degrees
    (
        [4 * np.pi, [0, 30, 60, 90, 120, 181]],
        "Two theta exceeds 180 degrees. Please check the input values for errors.",
    ),
    # UC3: user did not specify wavelength and specified invalid tth values
    (
        [None, [0, 30, 60, 90, 120, 181]],
        "Wavelength is not specified. Please provide a valid wavelength, "
        "e.g., DiffractionObject(wavelength=0.71).",
    ),
    # UC4: user specified an empty two theta array
    ([4 * np.pi, []], "Two theta array is empty. Please provide valid two theta values."),
    # UC5: user specified a non-numeric value in two theta array
    (
        [4 * np.pi, [0, 30, 60, 90, 120, "invalid"]],
        "Invalid value found in two theta array. Please ensure all values are numeric.",
    ),
]


@pytest.mark.parametrize("inputs, expected", params_tth_to_q_bad)
def test_tth_to_q_bad(inputs, expected):
    actual = DiffractionObject(wavelength=inputs[0])
    setattr(actual, "on_tth", [inputs[1], [1, 2, 3, 4, 5, 6]])
    with pytest.raises(ValueError, match=expected):
        actual.tth_to_q()


def test_dump(tmp_path, mocker):
    x, y = np.linspace(0, 5, 6), np.linspace(0, 5, 6)
    directory = Path(tmp_path)
    file = directory / "testfile"
    test = DiffractionObject()
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
