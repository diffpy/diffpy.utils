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

"""Various utilities related to data parsing and manipulation.
"""

from .loaddata import loadData
from .serialization import serialize_data, deserialize_data
from .resample import wsinterp, resample

# silence the pyflakes syntax checker
assert loadData or resample or True
assert serialize_data or deserialize_data or True

# End of file
