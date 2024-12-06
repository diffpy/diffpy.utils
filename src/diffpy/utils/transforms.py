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
invalid_q_or_wavelength_emsg = (
    "The supplied q-array and wavelength will result in an impossible two-theta. "
    "Please check these values and re-instantiate the DiffractionObject with correct values."
)
inf_output_wmsg = "WARNING: The largest output is infinite and cannot be plotted."


def _validate_inputs(q, wavelength):
    if wavelength is None:
        warnings.warn(wavelength_warning_emsg, UserWarning)
        return np.empty(0)
    pre_factor = wavelength / (4 * np.pi)
    if np.any(np.abs(q * pre_factor) > 1.0):
        raise ValueError(invalid_q_or_wavelength_emsg)


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
        This is the correct format for loading into diffpy.utils.DiffractionOject.on_tth
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
    tth : 2D array
        The array of :math:`2\theta` values and :math: 'i' intensity values, np.array([[tths], [is]]).
        This is the same format as, and so can accept, diffpy.utils.DiffractionOject.on_tth
        The units of tth are expected in degrees.

    wavelength : float
        Wavelength of the incoming x-rays/neutrons/electrons

    Returns
    -------
    on_q : 2D array
        The array of :math:`q` values and :math: 'i' intensity values unchanged,
        np.array([[qs], [is]]).
        The units for the q-values are the inverse of the units of the provided wavelength.
        This is the correct format for loading into diffpy.utils.DiffractionOject.on_q
    """
    tth.astype(float)
    if np.any(np.deg2rad(tth) > np.pi):
        raise ValueError(invalid_tth_emsg)
    q = copy(tth)
    if wavelength is not None:
        pre_factor = (4.0 * np.pi) / wavelength
        q = pre_factor * np.sin(np.deg2rad(tth / 2))
    else:  # return intensities vs. an x-array that is just the index
        for i, _ in enumerate(q):
            q[i] = i
    return q


def q_to_d(qarray):
    return 2.0 * np.pi / copy(qarray)


def tth_to_d(tth, wavelength):
    r"""
    Helper function to convert two-theta to d on independent variable axis.

    Uses the formula .. math:: d = \frac{\lambda}{2 \sin\left(\frac{2\theta}{2}\right)}.

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
    tth = np.deg2rad(tth)
    if 0 in tth:
        warnings.warn(inf_output_wmsg)
    qarray = tth_to_q(tth, wavelength)
    return 2.0 * np.pi / copy(qarray)


def d_to_q(darray):
    return 2.0 * np.pi / copy(darray)


def d_to_tth(darray, wavelength):
    qarray = d_to_q(darray)
    return q_to_tth(qarray, wavelength)
