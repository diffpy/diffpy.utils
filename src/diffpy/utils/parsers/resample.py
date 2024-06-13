#!/usr/bin/env python
##############################################################################
#
# diffpy.utils      by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2010 The Trustees of Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE_DANSE.txt for license information.
#
##############################################################################

"""Various utilities related to data parsing and manipulation."""

import numpy


# NOTE - this should be faster than resample below and conforms more closely to
# numpy.interp. I'm keeping resample for legacy reasons.
def wsinterp(x, xp, fp, left=None, right=None):
    """One-dimensional Whittaker-Shannon interpolation.

    This uses the Whittaker-Shannon interpolation formula to interpolate the value of fp (array),
    which is defined over xp (array), at x (array or float).

    Parameters
    ----------
    x: ndarray
        Desired range for interpolation.
    xp: ndarray
        Defined range for fp.
    fp: ndarray
        Function to be interpolated.
    left: float
        If given, set fp for x < xp[0] to left. Otherwise, if left is None (default) or not given,
        set fp for x < xp[0] to fp evaluated at xp[-1].
    right: float
        If given, set fp for x > xp[-1] to right. Otherwise, if right is None (default) or not given, set fp for
        x > xp[-1] to fp evaluated at xp[-1].

    Returns
    -------
    float:
        If input x is a scalar (not an array), return the interpolated value at x.
    ndarray:
        If input x is an array, return the interpolated array with dimensions of x.
    """
    scalar = numpy.isscalar(x)
    if scalar:
        x = numpy.array(x)
        x.resize(1)
    # shape = (nxp, nx), nxp copies of x data span axis 1
    u = numpy.resize(x, (len(xp), len(x)))
    # Must take transpose of u for proper broadcasting with xp.
    # shape = (nx, nxp), v(xp) data spans axis 1
    v = (xp - u.T) / (xp[1] - xp[0])
    # shape = (nx, nxp), m(v) data spans axis 1
    m = fp * numpy.sinc(v)
    # Sum over m(v) (axis 1)
    fp_at_x = numpy.sum(m, axis=1)

    # Enforce left and right
    if left is None:
        left = fp[0]
    fp_at_x[x < xp[0]] = left
    if right is None:
        right = fp[-1]
    fp_at_x[x > xp[-1]] = right

    # Return a float if we got a float
    if scalar:
        return float(fp_at_x[0])

    return fp_at_x


def resample(r, s, dr):
    """Resample a PDF on a new grid.

    This uses the Whittaker-Shannon interpolation formula to put s1 on a new grid if dr is less than the sampling
    interval of r1, or linear interpolation if dr is greater than the sampling interval of r1.

    Parameters
    ----------
    r
        The r-grid used for s1.
    s
        The signal to be resampled.
    dr
        The new sampling interval.

    Returns
    -------
    Returns resampled (r, s).
    """

    dr0 = r[1] - r[0]  # Constant timestep

    if dr0 < dr:
        rnew = numpy.arange(r[0], r[-1] + 0.5 * dr, dr)
        snew = numpy.interp(rnew, r, s)
        return rnew, snew

    elif dr0 > dr:
        # Tried to pad the end of s to dampen, but nothing works.
        # m = (s[-1] - s[-2]) / dr0
        # b = (s[-2] * r[-1] - s[-1] * r[-2]) / dr0
        # rpad = r[-1] + numpy.arange(1, len(s))*dr0
        # spad = rpad * m + b
        # spad = numpy.concatenate([s,spad])
        # rnew = numpy.arange(0, rpad[-1], dr)
        # snew = numpy.zeros_like(rnew)
        # Accomodate for the fact that r[0] might not be 0
        # u = (rnew-r[0]) / dr0
        # for n in range(len(spad)):
        #    snew += spad[n] * numpy.sinc(u - n)

        # sel = numpy.logical_and(rnew >= r[0], rnew <= r[-1])

        rnew = numpy.arange(0, r[-1], dr)
        snew = numpy.zeros_like(rnew)
        u = (rnew - r[0]) / dr0
        for n in range(len(s)):
            snew += s[n] * numpy.sinc(u - n)
        sel = numpy.logical_and(rnew >= r[0], rnew <= r[-1])
        return rnew[sel], snew[sel]

    # If we got here, then no resampling is required
    return r.copy(), s.copy()


# End of file
