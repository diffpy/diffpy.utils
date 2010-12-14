##############################################################################
#
# diffpy.util       by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2010 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

"""Various utilities related to data parsing and manipulation."""

import numpy

def resample(r, s, dr):
    """Resample a PDF on a new grid.

    This uses the Whittaker-Shannon interpolation formula to put s1 on a new
    grid if dr is less than the sampling interval of r1, or linear
    interpolation if dr is greater than the sampling interval of r1.

    r       --  The r-grid used for s1
    s       --  The signal to be resampled
    dr      --  The new sampling interval

    Returns resampled (r, s)

    """

    dr0 = r[1] - r[0]

    if dr0 < dr:
        rnew = numpy.arange(r[0], r[-1]+0.5*dr, dr)
        snew = numpy.interp(rnew, r, s)
        return rnew, snew

    elif dr0 > dr:

        # Tried to pad the end of s to dampen, but nothing works.
        #m = (s[-1] - s[-2]) / dr0
        #b = (s[-2] * r[-1] - s[-1] * r[-2]) / dr0
        #rpad = r[-1] + numpy.arange(1, len(s))*dr0
        #spad = rpad * m + b
        #spad = numpy.concatenate([s,spad])
        #rnew = numpy.arange(0, rpad[-1], dr)
        #snew = numpy.zeros_like(rnew)
        ## Accomodate for the fact that r[0] might not be 0
        #u = (rnew-r[0]) / dr0
        #for n in range(len(spad)):
        #    snew += spad[n] * numpy.sinc(u - n)

        #sel = numpy.logical_and(rnew >= r[0], rnew <= r[-1])

        rnew = numpy.arange(0, r[-1], dr)
        snew = numpy.zeros_like(rnew)
        u = (rnew-r[0]) / dr0
        for n in range(len(s)):
            snew += s[n] * numpy.sinc(u - n)
        sel = numpy.logical_and(rnew >= r[0], rnew <= r[-1])
        return rnew[sel], snew[sel]

    # If we got here, then no resampling is required
    return r.copy(), s.copy()

__id__ = "$Id$"
# End of file
