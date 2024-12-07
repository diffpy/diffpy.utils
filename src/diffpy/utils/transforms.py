import warnings
from copy import copy

import numpy as np

wavelength_warning_emsg = (
    "INFO: no wavelength has been specified. You can continue "
    "to use the DiffractionObject but some of its powerful features "
    "will not be available. To specify a wavelength, set "
    "diffraction_object.wavelength = [number], "
    "where diffraction_object is the variable name of you Diffraction Object, "
    "and number is the wavelength in angstroms."
)
invalid_tth_emsg = "Two theta exceeds 180 degrees. Please check the input values for errors."
invalid_q_or_d_or_wavelength_emsg = (
    "The supplied input array and wavelength will result in an impossible two-theta. "
    "Please check these values and re-instantiate the DiffractionObject with correct values."
)
inf_output_wmsg = (
    "INFO: The largest output value in the array is infinite. This is allowed, but it will not be plotted."
)


def _validate_inputs(q, wavelength):
    if wavelength is None:
        warnings.warn(wavelength_warning_emsg, UserWarning)
        return np.empty(0)
    pre_factor = wavelength / (4 * np.pi)
    if np.any(np.abs(q * pre_factor) > 1.0):
        raise ValueError(invalid_q_or_d_or_wavelength_emsg)


def q_to_tth(q, wavelength):
    r"""
    Helper function to convert q to two-theta.

    If wavelength is missing, returns x-values that are integer indexes

    By definition the relationship is:

    .. math::

        \sin\left(\frac{2\theta}{2}\right) = \frac{\lambda q}{4 \pi}

    thus

    .. math::

        2\theta_n = 2 \arcsin\left(\frac{\lambda q}{4 \pi}\right)

    Parameters
    ----------
    q : 1D array
        The array of :math:`q` values numpy.array([qs]).
        The units of q must be reciprocal of the units of wavelength.

    wavelength : float
        Wavelength of the incoming x-rays/neutrons/electrons

    Returns
    -------
    tth : 1D array
        The array of :math:`2\theta` values in degrees numpy.array([tths]).
    """
    _validate_inputs(q, wavelength)
    q.astype(float)
    tth = copy(q)  # initialize output array of same shape
    if wavelength is not None:
        tth = np.rad2deg(2.0 * np.arcsin(q * wavelength / (4 * np.pi)))
    else:  # return intensities vs. an x-array that is just the index
        for i, _ in enumerate(q):
            tth[i] = i
    return tth


def tth_to_q(tth, wavelength):
    r"""

    Helper function to convert two-theta to q on independent variable axis.

    If wavelength is missing, returns independent variable axis as integer indexes.

    By definition the relationship is:

    .. math::

        \sin\left(\frac{2\theta}{2}\right) = \frac{\lambda q}{4 \pi}

    thus

    .. math::

        q = \frac{4 \pi \sin\left(\frac{2\theta}{2}\right)}{\lambda}

    Parameters
    ----------
    tth : 1D array
        The array of :math:`2\theta` values np.array([tths]).
        The units of tth are expected in degrees.

    wavelength : float
        Wavelength of the incoming x-rays/neutrons/electrons

    Returns
    -------
    q : 1D array
        The array of :math:`q` values np.array([qs]).
        The units for the q-values are the inverse of the units of the provided wavelength.
    """
    tth.astype(float)
    if np.any(np.deg2rad(tth) > np.pi):
        raise ValueError(invalid_tth_emsg)
    q = copy(tth)
    if wavelength is not None:
        pre_factor = (4.0 * np.pi) / wavelength
        q = pre_factor * np.sin(np.deg2rad(tth / 2))
    else:  # return intensities vs. an x-array that is just the index
        warnings.warn(wavelength_warning_emsg, UserWarning)
        for i, _ in enumerate(q):
            q[i] = i
    return q


def q_to_d(q):
    r"""
    Helper function to convert q to d on independent variable axis, using :math:`d = \frac{2 \pi}{q}`.

    Parameters
    ----------
    q : 1D array
        The array of :math:`q` values np.array([qs]).
        The units of q must be reciprocal of the units of wavelength.

    Returns
    -------
    d : 1D array
        The array of :math:`d` values np.array([ds]).
    """
    if 0 in q:
        print(inf_output_wmsg)
    return 2.0 * np.pi / copy(q)


def tth_to_d(tth, wavelength):
    r"""
    Helper function to convert two-theta to d on independent variable axis.

    The formula is .. math:: d = \frac{\lambda}{2 \sin\left(\frac{2\theta}{2}\right)}.

    Here we convert tth to q first, then to d.

    Parameters
    ----------
    tth : 1D array
        The array of :math:`2\theta` values np.array([tths]).
        The units of tth are expected in degrees.

    wavelength : float
        Wavelength of the incoming x-rays/neutrons/electrons

    Returns
    -------
    d : 1D array
        The array of :math:`d` values np.array([ds]).
    """
    q = tth_to_q(tth, wavelength)
    d = copy(tth)
    if wavelength is None:
        warnings.warn(wavelength_warning_emsg, UserWarning)
        for i, _ in enumerate(tth):
            d[i] = i
        return d
    if 0 in q:
        warnings.warn(inf_output_wmsg)
    return 2.0 * np.pi / copy(q)


def d_to_q(d):
    r"""
    Helper function to convert q to d using :math:`d = \frac{2 \pi}{q}`.

    Parameters
    ----------
    d : 1D array
        The array of :math:`d` values np.array([ds]).

    Returns
    -------
    q : 1D array
        The array of :math:`q` values np.array([qs]).
        The units of q must be reciprocal of the units of wavelength.
    """
    if 0 in d:
        warnings.warn(inf_output_wmsg)
    return 2.0 * np.pi / copy(d)


def d_to_tth(d, wavelength):
    r"""
    Helper function to convert d to two-theta on independent variable axis.

    The formula is .. math:: 2\theta = 2 \arcsin\left(\frac{\lambda}{2d}\right).

    Here we convert d to q first, then to tth.

    Parameters
    ----------
    d : 1D array
        The array of :math:`d` values np.array([ds]).

    wavelength : float
        Wavelength of the incoming x-rays/neutrons/electrons

    Returns
    -------
    tth : 1D array
        The array of :math:`2\theta` values np.array([tths]).
        The units of tth are expected in degrees.
    """
    q = d_to_q(d)
    return q_to_tth(q, wavelength)
