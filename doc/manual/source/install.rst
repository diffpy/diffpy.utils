Installation
========================================================================

.. index:: Requirements

The diffpy.utils package requires Python 2.6 or 2.7 and the following software:

    setuptools   -- tools for installing Python packages
    NumPy        -- library for scientific computing with Python
    wxPython     -- GUI toolkit for the Python language

Some of the required software packages may be available in the system package
manager, for example, on Ubuntu Linux the dependencies can be installed as:

    sudo apt-get install
        python-setuptools python-numpy python-wxgtk2.8

For Mac OS X systems with the MacPorts package manager one could do

    sudo port install \
        python27 py27-setuptools py27-numpy

When installing for MacPorts, make sure the MacPorts bin directory is the
first in the system PATH and that python27 is selected as the default
Python version in MacPorts:

    sudo port select --set python python27

For other required packages see their respective web pages for installation
instructions.

.. index:: Installation

Installation
------------------------------------------------------------------------

To install from sources, make sure all required software
packages are in place and then run

    sudo python setup.py install

This installs diffpy.util for all users in the default system location.
If administrator (root) access is not available, see the usage info from
"python setup.py install --help" for options to install to user-writable
directories.  The installation integrity can be verified by changing to
the HOME directory and running

    python -m diffpy.utils.tests.run


.. index:: Contribution

Contribution
------------------------------------------------------------------------

diffpy.utils is an open-source software developed as a part of the
DiffPy-CMI complex modeling initiative at the Brookhaven National
Laboratory.  The diffpy.utils sources are hosted at

    https://github.com/diffpy/diffpy.utils/,

Feel free to fork the project and contribute.  To install diffpy.utils
in a development mode, with its sources being directly used by Python
rather than copied to a package directory, use

    python setup.py develop --user
