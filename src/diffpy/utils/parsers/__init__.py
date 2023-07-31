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
from .loadmetafile import load_PDF_into_db, markup_PDF, apply_schema
from .resample import resample

# silence the pyflakes syntax checker
assert loadData or load_PDF_into_db or markup_PDF or apply_schema or resample or True

# End of file
