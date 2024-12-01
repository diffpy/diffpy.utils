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


def _validate_inputs(on_q, wavelength):
    if wavelength is None:
        warnings.warn(wavelength_warning_emsg, UserWarning)
        return np.empty(0)
    pre_factor = wavelength / (4 * np.pi)
    if np.any(np.abs(on_q[0] * pre_factor) > 1.0):
        raise ValueError(invalid_q_or_wavelength_emsg)


def q_to_tth(on_q, wavelength):
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
    on_q : 2D array
        The array of :math:`q` values and :math: 'i' intensity values, np.array([[qs], [is]]).
        This is the same format as, and so can accept, diffpy.utils.DiffractionOject.on_q
        The units of q must be reciprocal of the units of wavelength.

    wavelength : float
        Wavelength of the incoming x-rays/neutrons/electrons

    Returns
    -------
    on_tth : 2D array
        The array of :math:`2\theta` values in degrees and :math: 'i' intensity values unchanged,
        np.array([[tths], [is]]).
        This is the correct format for loading into diffpy.utils.DiffractionOject.on_tth
    """
    _validate_inputs(on_q, wavelength)
    on_q.astype(np.float64)
    on_tth = copy(on_q)  # initialize output array of same shape
    if wavelength is not None:
        on_tth[0] = np.rad2deg(2.0 * np.arcsin(on_q[0] * wavelength / (4 * np.pi)))
    else:  # return intensities vs. an x-array that is just the index
        for i, _ in enumerate(on_q[0]):
            on_tth[0][i] = i
    return on_tth


def tth_to_q(on_tth, wavelength):
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
    on_tth : 2D array
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
    on_tth.astype(np.float64)
    if np.any(np.deg2rad(on_tth[0]) > np.pi):
        raise ValueError(invalid_tth_emsg)
    on_q = copy(on_tth)
    if wavelength is not None:
        pre_factor = (4.0 * np.pi) / wavelength
        on_q[0] = pre_factor * np.sin(np.deg2rad(on_tth[0] / 2))
    else:  # return intensities vs. an x-array that is just the index
        for i, _ in enumerate(on_q[0]):
            on_q[0][i] = i
    return on_q
