#!/usr/bin/env python
##############################################################################
#
# diffpy.utils      by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2010 The Trustees of Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE_DANSE.txt for license information.
#
##############################################################################


class UnsupportedTypeError(Exception):
    """For file types not supported by our parsers.

    Parameters
    ----------
    file
        Name of file triggering the error.
    supported_types: list
        Supported file types.
    message: str
        Overwrites default message.
    """

    def __init__(self, file, supported_types=None, message=None):
        if message is None:
            self.message = f"The file {file} is not supported."
            if supported_types is not None:
                self.message += " Supported file types include: "
            for t in supported_types:
                self.message += t + ", "
            self.message = self.message[:-2] + "."
        super().__init__(self.message)


class ImproperSizeError(Exception):
    """When the size of an object does not match expectations.

    Parameters
    ----------
    bad_object
        Object with improper size.
    message: str
        Overwrites default message.
    """

    def __init__(self, bad_object, message=None):
        if message is None:
            self.message = f"The size of {bad_object} is different than expected."
        super().__init__(self.message)
