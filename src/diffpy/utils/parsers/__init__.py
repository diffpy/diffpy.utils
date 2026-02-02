#!/usr/bin/env python
##############################################################################
#
# diffpy.utils      by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2010 The Trustees of Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Simon Billinge
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE_DANSE.txt for license information.
#
##############################################################################
"""Various utilities related to data parsing and manipulation."""

# this  allows load_data to be imported from diffpy.utils.parsers
# it is needed during deprecation of the old loadData structure
# when we remove loadData we can move all the parser functionality
# a parsers.py module (like tools.py) and remove this if we want
from .loaddata import load_data

__all__ = ["load_data"]
