.. image:: https://travis-ci.org/diffpy/diffpy.utils.svg?branch=master
   :target: https://travis-ci.org/diffpy/diffpy.utils

.. image:: https://codecov.io/gh/diffpy/diffpy.utils/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/diffpy/diffpy.utils


diffpy.utils
========================================================================

General purpose shared utilities for the diffpy libraries.

The diffpy.utils package provides functions for extracting array data from
variously formatted text files and wx GUI utilities used by the PDFgui
program.  The package also includes an interpolation function based on the
Whittaker-Shannon formula that can be used to resample a PDF or other profile
function over a new grid.

For more information about the diffpy.utils library, see the users manual at
http://diffpy.github.io/diffpy.utils.


REQUIREMENTS
------------------------------------------------------------------------

The diffpy.utils package requires Python 3.4 or later or 2.7 and
the following software:

* ``setuptools``   - tools for installing Python packages
* ``NumPy``        - library for scientific computing with Python

The functions in diffpy.utils.wx module require

* ``wxPython``     - GUI toolkit for the Python language

We recommend to use `Anaconda Python <https://www.anaconda.com/download>`_
as it allows to install the software dependencies together with
diffpy.utils.  For other Python distributions it is necessary to install
the required software separately.  As an example, on Ubuntu Linux the
required software can be installed with ::

   sudo apt-get install python-setuptools python-numpy


INSTALLATION
------------------------------------------------------------------------

The preferred method is to use Anaconda Python and install from the
"diffpy" channel of Anaconda packages ::

   conda config --add channels diffpy
   conda install diffpy.utils

Another option is to use ``easy_install`` to download and install the
latest release from `Python Package Index <https://pypi.python.org>`_ ::

   easy_install diffpy.utils

If you prefer to install from sources, obtain the source archive and
run ::

   python setup.py install

You may need to use ``sudo`` with system Python as it attempts to
install to standard system directories.  If sudo is not available, check
the usage info from ``python setup.py install --help`` for options to
install to user-writable locations.  The installation integrity can be
verified by changing to the HOME directory and running ::

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
