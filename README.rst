diffpy.utils
========================================================================

General purpose shared utilities for the diffpy libraries.

The diffpy.utils package provides functions for extracting array data from
variously formatted text files and wx GUI utilities used by the PDFgui
program.  The package also includes interpolation function based on the
Whittaker-Shannon formula that can be used to resample a PDF or other profile
function over a new grid.

For more information about the diffpy.utils library, see the users manual at
http://diffpy.github.io/diffpy.utils.


REQUIREMENTS
------------------------------------------------------------------------

The diffpy.utils package requires Python 2.6 or 2.7 and the following software:

* ``setuptools``   - tools for installing Python packages
* ``NumPy``        - library for scientific computing with Python

The functions in diffpy.utils.wx module require

* ``wxPython``     - GUI toolkit for the Python language

Some of the required software packages may be available in the system package
manager, for example, on Ubuntu Linux the dependencies can be installed as::

   sudo apt-get install python-setuptools python-numpy

For Mac OS X systems with the MacPorts package manager one could do ::

   sudo port install python27 py27-setuptools py27-numpy

When installing for MacPorts, make sure the MacPorts bin directory is the
first in the system PATH and that python27 is selected as the default
Python version in MacPorts::

   sudo port select --set python python27

For other required packages see their respective web pages for installation
instructions.


INSTALLATION
------------------------------------------------------------------------

Use ``easy_install`` to download and install the latest release from
`Python Package Index <https://pypi.python.org>`_ ::

   sudo easy_install diffpy.utils

If you prefer to install from sources, make sure all required software
packages are in place and then run ::

   sudo python setup.py install

This installs diffpy.util for all users in the default system location.
If administrator (root) access is not available, see the usage info from
``python setup.py install --help`` for options to install to user-writable
directories.  The installation integrity can be verified by changing to
the HOME directory and running ::

   python -m diffpy.utils.tests.run


DEVELOPMENT
------------------------------------------------------------------------

diffpy.utils is an open-source software developed as a part of the
DiffPy-CMI complex modeling initiative at the Brookhaven National
Laboratory.  The diffpy.utils sources are hosted at
https://github.com/diffpy/diffpy.utils.

Feel free to fork the project and contribute.  To install diffpy.utils
in a development mode, with its sources being directly used by Python
rather than copied to a package directory, use ::

   python setup.py develop --user


CONTACTS
------------------------------------------------------------------------

For more information on diffpy.utils please visit the project web-page

http://www.diffpy.org/

or email Prof. Simon Billinge at sb2896@columbia.edu.
