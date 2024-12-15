import re

import numpy as np
import pytest

from diffpy.utils.transforms import d_to_q, d_to_tth, q_to_d, q_to_tth, tth_to_d, tth_to_q

params_q_to_tth = [
    # UC1: Empty q values, no wavelength, return empty arrays
    (None, np.empty((0)), np.empty((0))),
    # UC2: Empty q values, wavelength specified, return empty arrays
    (4 * np.pi, np.empty((0)), np.empty(0)),
    # UC3: User specified valid q values, no wavelength, return empty arrays
    (
        None,
        np.array([0, 0.2, 0.4, 0.6, 0.8, 1]),
        np.array([0, 1, 2, 3, 4, 5]),
    ),
    # UC4: User specified valid q values (with wavelength)
    # expected tth values are 2*arcsin(q) in degrees
    (4 * np.pi, np.array([0, 1 / np.sqrt(2), 1.0]), np.array([0, 90.0, 180.0])),
]


@pytest.mark.parametrize("wavelength, q, expected_tth", params_q_to_tth)
def test_q_to_tth(wavelength, q, expected_tth, wavelength_warning_msg):

    if wavelength is None:
        with pytest.warns(UserWarning, match=re.escape(wavelength_warning_msg)):
            actual_tth = q_to_tth(q, wavelength)
    else:
        actual_tth = q_to_tth(q, wavelength)

    assert np.allclose(expected_tth, actual_tth)


test_q_to_tth_bad_params = [
    # UC1: user specified invalid q values that result in tth > 180 degrees
    (
        4 * np.pi,
        np.array([0.2, 0.4, 0.6, 0.8, 1, 1.2]),
        ValueError,
        "The supplied input array and wavelength will result in an impossible two-theta. "
        "Please check these values and re-instantiate the DiffractionObject with correct values.",
    ),
    # UC2: user specified a wrong wavelength that result in tth > 180 degrees
    (
        100,
        np.array([0, 0.2, 0.4, 0.6, 0.8, 1]),
        ValueError,
        "The supplied input array and wavelength will result in an impossible two-theta. "
        "Please check these values and re-instantiate the DiffractionObject with correct values.",
    ),
]


@pytest.mark.parametrize("q, wavelength, expected_error_type, expected_error_msg", test_q_to_tth_bad_params)
def test_q_to_tth_bad(q, wavelength, expected_error_type, expected_error_msg):
    with pytest.raises(expected_error_type, match=expected_error_msg):
        q_to_tth(wavelength, q)


test_tth_t_q_params = [
    # UC0: User specified empty tth values (without wavelength)
    (None, np.array([]), np.array([])),
    # UC1: User specified empty tth values (with wavelength)
    (4 * np.pi, np.array([]), np.array([])),
    # UC2: User specified valid tth values between 0-180 degrees (without wavelength)
    (
        None,
        np.array([0, 30, 60, 90, 120, 180]),
        np.array([0, 1, 2, 3, 4, 5]),
    ),
    # UC3: User specified valid tth values between 0-180 degrees (with wavelength)
    # expected q values are sin15, sin30, sin45, sin60, sin90
    (
        4 * np.pi,
        np.array([0, 30.0, 60.0, 90.0, 120.0, 180.0]),
        np.array([0, 0.258819, 0.5, 0.707107, 0.866025, 1]),
    ),
]


@pytest.mark.parametrize("wavelength, tth, expected_q", test_tth_t_q_params)
def test_tth_to_q(wavelength, tth, expected_q, wavelength_warning_msg):
    if wavelength is None:
        with pytest.warns(UserWarning, match=re.escape(wavelength_warning_msg)):
            actual_q = tth_to_q(tth, wavelength)
    else:
        actual_q = tth_to_q(tth, wavelength)

    assert np.allclose(actual_q, expected_q)


test_tth_to_q_bad_params = [
    # UC0: user specified an invalid tth value of > 180 degrees (without wavelength)
    (
        None,
        np.array([0, 30, 60, 90, 120, 181]),
        ValueError,
        "Two theta exceeds 180 degrees. Please check the input values for errors.",
    ),
    # UC1: user specified an invalid tth value of > 180 degrees (with wavelength)
    (
        4 * np.pi,
        np.array([0, 30, 60, 90, 120, 181]),
        ValueError,
        "Two theta exceeds 180 degrees. Please check the input values for errors.",
    ),
]


@pytest.mark.parametrize("wavelength, tth, expected_error_type, expected_error_msg", test_tth_to_q_bad_params)
def test_tth_to_q_bad(wavelength, tth, expected_error_type, expected_error_msg):
    with pytest.raises(expected_error_type, match=expected_error_msg):
        tth_to_q(tth, wavelength)


test_q_to_d_params = [
    # UC1: User specified empty q values
    (np.array([]), np.array([])),
    # UC2: User specified valid q values
    (
        np.array([0, 1 * np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi, 5 * np.pi]),
        np.array([np.inf, 2, 1, 0.66667, 0.5, 0.4]),
    ),
]


@pytest.mark.parametrize("q, expected_d", test_q_to_d_params)
def test_q_to_d(q, expected_d):
    actual_d = q_to_d(q)
    assert np.allclose(actual_d, expected_d)


test_d_to_q_params = [
    # UC1: User specified empty d values
    (np.array([]), np.array([])),
    # UC2: User specified valid d values
    (
        np.array([5 * np.pi, 4 * np.pi, 3 * np.pi, 2 * np.pi, np.pi, 0]),
        np.array([0.4, 0.5, 0.66667, 1, 2, np.inf]),
    ),
]


@pytest.mark.parametrize("d, expected_q", test_d_to_q_params)
def test_d_to_q(d, expected_q):
    actual_q = d_to_q(d)
    assert np.allclose(actual_q, expected_q)


test_tth_to_d_params = [
    # UC0: User specified empty tth values (without wavelength)
    (None, np.array([]), np.array([])),
    # UC1: User specified empty tth values (with wavelength)
    (4 * np.pi, np.array([]), np.array([])),
    # UC2: User specified valid tth values between 0-180 degrees (without wavelength)
    (
        None,
        np.array([0, 30, 60, 90, 120, 180]),
        np.array([0, 1, 2, 3, 4, 5]),
    ),
    # UC3: User specified valid tth values between 0-180 degrees (with wavelength)
    (
        4 * np.pi,
        np.array([0, 30.0, 60.0, 90.0, 120.0, 180.0]),
        np.array([np.inf, 24.27636, 12.56637, 8.88577, 7.25520, 6.28319]),
    ),
]


@pytest.mark.parametrize("wavelength, tth, expected_d", test_tth_to_d_params)
def test_tth_to_d(wavelength, tth, expected_d):
    actual_d = tth_to_d(tth, wavelength)
    assert np.allclose(actual_d, expected_d)


test_tth_to_d_invalid_params = [
    # UC1: user specified an invalid tth value of > 180 degrees (without wavelength)
    (
        None,
        np.array([0, 30, 60, 90, 120, 181]),
        ValueError,
        "Two theta exceeds 180 degrees. Please check the input values for errors.",
    ),
    # UC2: user specified an invalid tth value of > 180 degrees (with wavelength)
    (
        4 * np.pi,
        np.array([0, 30, 60, 90, 120, 181]),
        ValueError,
        "Two theta exceeds 180 degrees. Please check the input values for errors.",
    ),
]


@pytest.mark.parametrize("wavelength, tth, expected_error_type, expected_error_msg", test_tth_to_d_invalid_params)
def test_tth_to_d_invalid(wavelength, tth, expected_error_type, expected_error_msg):
    with pytest.raises(expected_error_type, match=expected_error_msg):
        tth_to_d(tth, wavelength)


test_d_to_tth_params = [
    # UC1: Empty d values, no wavelength, return empty arrays
    (None, np.empty((0)), np.empty((0))),
    # UC2: Empty d values, wavelength specified, return empty arrays
    (4 * np.pi, np.empty((0)), np.empty(0)),
    # UC3: User specified valid d values, no wavelength, return empty arrays
    (
        None,
        np.array([1, 0.8, 0.6, 0.4, 0.2, 0]),
        np.array([0, 1, 2, 3, 4, 5]),
    ),
    # UC4: User specified valid d values (with wavelength)
    (
        4 * np.pi,
        np.array([4 * np.pi, 4 / np.sqrt(2) * np.pi, 4 / np.sqrt(3) * np.pi]),
        np.array([60.0, 90.0, 120.0]),
    ),
]


@pytest.mark.parametrize("wavelength, d, expected_tth", test_d_to_tth_params)
def test_d_to_tth(wavelength, d, expected_tth):
    actual_tth = d_to_tth(d, wavelength)
    assert np.allclose(actual_tth, expected_tth)


test_d_to_tth_bad_params = [
    # UC1: user specified invalid d values that result in tth > 180 degrees
    (
        4 * np.pi,
        np.array([1.2, 1, 0.8, 0.6, 0.4, 0.2]),
        ValueError,
        "The supplied input array and wavelength will result in an impossible two-theta. "
        "Please check these values and re-instantiate the DiffractionObject with correct values.",
    ),
    # UC2: user specified a wrong wavelength that result in tth > 180 degrees
    (
        100,
        np.array([1, 0.8, 0.6, 0.4, 0.2, 0]),
        ValueError,
        "The supplied input array and wavelength will result in an impossible two-theta. "
        "Please check these values and re-instantiate the DiffractionObject with correct values.",
    ),
]


@pytest.mark.parametrize("wavelength, d, expected_error_type, expected_error_msg", test_d_to_tth_bad_params)
def test_d_to_tth_bad(wavelength, d, expected_error_type, expected_error_msg):
    with pytest.raises(expected_error_type, match=expected_error_msg):
        d_to_tth(d, wavelength)
