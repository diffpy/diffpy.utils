import numpy as np
import pytest

from diffpy.utils.transforms import d_to_q, q_to_d, q_to_tth, tth_to_q

params_q_to_tth = [
    # UC1: Empty q values, no wavelength, return empty arrays
    ([None, np.empty((0))], np.empty((0))),
    # UC2: Empty q values, wavelength specified, return empty arrays
    ([4 * np.pi, np.empty((0))], np.empty(0)),
    # UC3: User specified valid q values, no wavelength, return empty arrays
    (
        [None, np.array([0, 0.2, 0.4, 0.6, 0.8, 1])],
        np.array([0, 1, 2, 3, 4, 5]),
    ),
    # UC4: User specified valid q values (with wavelength)
    # expected tth values are 2*arcsin(q) in degrees
    ([4 * np.pi, np.array([0, 1 / np.sqrt(2), 1.0])], np.array([0, 90.0, 180.0])),
]


@pytest.mark.parametrize("inputs, expected", params_q_to_tth)
def test_q_to_tth(inputs, expected):
    actual = q_to_tth(inputs[1], inputs[0])
    assert np.allclose(expected, actual)


params_q_to_tth_bad = [
    # UC1: user specified invalid q values that result in tth > 180 degrees
    (
        [4 * np.pi, np.array([0.2, 0.4, 0.6, 0.8, 1, 1.2])],
        [
            ValueError,
            "The supplied q-array and wavelength will result in an impossible two-theta. "
            "Please check these values and re-instantiate the DiffractionObject with correct values.",
        ],
    ),
    # UC2: user specified a wrong wavelength that result in tth > 180 degrees
    (
        [100, np.array([0, 0.2, 0.4, 0.6, 0.8, 1])],
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
    ([None, np.array([])], np.array([])),
    # UC1: User specified empty tth values (with wavelength)
    ([4 * np.pi, np.array([])], np.array([])),
    # UC2: User specified valid tth values between 0-180 degrees (without wavelength)
    (
        [None, np.array([0, 30, 60, 90, 120, 180])],
        np.array([0, 1, 2, 3, 4, 5]),
    ),
    # UC3: User specified valid tth values between 0-180 degrees (with wavelength)
    # expected q values are sin15, sin30, sin45, sin60, sin90
    (
        [4 * np.pi, np.array([0, 30.0, 60.0, 90.0, 120.0, 180.0])],
        np.array([0, 0.258819, 0.5, 0.707107, 0.866025, 1]),
    ),
]


@pytest.mark.parametrize("inputs, expected", params_tth_to_q)
def test_tth_to_q(inputs, expected):
    actual = tth_to_q(inputs[1], inputs[0])
    assert np.allclose(actual, expected)


params_tth_to_q_bad = [
    # UC0: user specified an invalid tth value of > 180 degrees (without wavelength)
    (
        [None, np.array([0, 30, 60, 90, 120, 181])],
        [ValueError, "Two theta exceeds 180 degrees. Please check the input values for errors."],
    ),
    # UC1: user specified an invalid tth value of > 180 degrees (with wavelength)
    (
        [4 * np.pi, np.array([0, 30, 60, 90, 120, 181])],
        [ValueError, "Two theta exceeds 180 degrees. Please check the input values for errors."],
    ),
]


@pytest.mark.parametrize("inputs, expected", params_tth_to_q_bad)
def test_tth_to_q_bad(inputs, expected):
    with pytest.raises(expected[0], match=expected[1]):
        tth_to_q(inputs[1], inputs[0])


params_q_to_d = [
    # UC1: User specified empty q values
    ([np.array([])], np.array([])),
    # UC2: User specified valid q values
    (
        [np.array([5 * np.pi, 4 * np.pi, 3 * np.pi, 2 * np.pi, np.pi, 0])],
        np.array([0.4, 0.5, 0.66667, 1, 2, np.inf]),
    ),
]


@pytest.mark.parametrize("inputs, expected", params_q_to_d)
def test_q_to_d(inputs, expected):
    actual = q_to_d(inputs[0])
    assert np.allclose(actual, expected)


params_d_to_q = [
    # UC1: User specified empty d values
    ([np.array([])], np.array([])),
    # UC2: User specified valid d values
    (
        [np.array([0, 1 * np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi, 5 * np.pi])],
        np.array([np.inf, 2, 1, 0.66667, 0.5, 0.4]),
    ),
]


@pytest.mark.parametrize("inputs, expected", params_d_to_q)
def test_d_to_q(inputs, expected):
    actual = d_to_q(inputs[0])
    assert np.allclose(actual, expected)
