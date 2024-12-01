import numpy as np
import pytest

from diffpy.utils.transforms import q_to_tth, tth_to_q

params_q_to_tth = [
    # UC1: Empty q values, no wavelength, return empty arrays
    ([None, np.empty((2, 0))], np.empty((2, 0))),
    # UC2: Empty q values, wavelength specified, return empty arrays
    ([4 * np.pi, np.empty((2, 0))], np.empty((2, 0))),
    # UC3: User specified valid q values, no wavelength, return empty arrays
    (
        [None, np.array([[0, 0.2, 0.4, 0.6, 0.8, 1], [1, 2, 3, 4, 5, 6]])],
        np.array([[0, 1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]]),
    ),
    # UC4: User specified valid q values (with wavelength)
    # expected tth values are 2*arcsin(q) in degrees
    ([4 * np.pi, np.array([[0, 1 / np.sqrt(2), 1.0], [1, 2, 3]])], np.array([[0, 90.0, 180.0], [1, 2, 3]])),
]


@pytest.mark.parametrize("inputs, expected", params_q_to_tth)
def test_q_to_tth(inputs, expected):
    actual = q_to_tth(inputs[1], inputs[0])
    assert np.allclose(expected[0], actual[0])
    assert np.allclose(expected[1], actual[1])


params_q_to_tth_bad = [
    # UC1: user specified invalid q values that result in tth > 180 degrees
    (
        [4 * np.pi, np.array([[0.2, 0.4, 0.6, 0.8, 1, 1.2], [1, 2, 3, 4, 5, 6]])],
        [
            ValueError,
            "The supplied q-array and wavelength will result in an impossible two-theta. "
            "Please check these values and re-instantiate the DiffractionObject with correct values.",
        ],
    ),
    # UC2: user specified a wrong wavelength that result in tth > 180 degrees
    (
        [100, np.array([[0, 0.2, 0.4, 0.6, 0.8, 1], [1, 2, 3, 4, 5, 6]])],
        [
            ValueError,
            "The supplied q-array and wavelength will result in an impossible two-theta. "
            "Please check these values and re-instantiate the DiffractionObject with correct values.",
        ],
    ),
]


@pytest.mark.parametrize("inputs, expected", params_q_to_tth_bad)
def test_q_to_tth_bad(inputs, expected):
    with pytest.raises(expected[0], match=expected[1]):
        q_to_tth(inputs[1], inputs[0])


params_tth_to_q = [
    # UC0: User specified empty tth values (without wavelength)
    ([None, np.array([[], []])], np.array([[], []])),
    # UC1: User specified empty tth values (with wavelength)
    ([4 * np.pi, np.array([[], []])], np.array([[], []])),
    # UC2: User specified valid tth values between 0-180 degrees (without wavelength)
    (
        [None, np.array([[0, 30, 60, 90, 120, 180], [1, 2, 3, 4, 5, 6]])],
        np.array([[0, 1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]]),
    ),
    # UC3: User specified valid tth values between 0-180 degrees (with wavelength)
    # expected q vales are sin15, sin30, sin45, sin60, sin90
    (
        [4 * np.pi, np.array([[0, 30.0, 60.0, 90.0, 120.0, 180.0], [1, 2, 3, 4, 5, 6]])],
        np.array([[0, 0.258819, 0.5, 0.707107, 0.866025, 1], [1, 2, 3, 4, 5, 6]]),
    ),
]


@pytest.mark.parametrize("inputs, expected", params_tth_to_q)
def test_tth_to_q(inputs, expected):
    actual = tth_to_q(inputs[1], inputs[0])
    assert np.allclose(actual, expected)


params_tth_to_q_bad = [
    # UC0: user specified an invalid tth value of > 180 degrees (without wavelength)
    (
        [None, np.array([[0, 30, 60, 90, 120, 181], [1, 2, 3, 4, 5, 6]])],
        [ValueError, "Two theta exceeds 180 degrees. Please check the input values for errors."],
    ),
    # UC1: user specified an invalid tth value of > 180 degrees (with wavelength)
    (
        [4 * np.pi, np.array([[0, 30, 60, 90, 120, 181], [1, 2, 3, 4, 5, 6]])],
        [ValueError, "Two theta exceeds 180 degrees. Please check the input values for errors."],
    ),
]


@pytest.mark.parametrize("inputs, expected", params_tth_to_q_bad)
def test_tth_to_q_bad(inputs, expected):
    with pytest.raises(expected[0], match=expected[1]):
        tth_to_q(inputs[1], inputs[0])
