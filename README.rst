.. image:: https://github.com/diffpy/diffpy.utils/actions/workflows/main.yml/badge.svg
   :target: https://github.com/diffpy/diffpy.utils/actions/workflows/main.yml

.. image:: https://codecov.io/gh/diffpy/diffpy.utils/branch/main/graph/badge.svg
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

INSTALLATION
------------------------------------------------------------------------

The preferred method is to use `Miniconda Python
<https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html>`_
and install from the "conda-forge" channel of Conda packages.

To add "conda-forge" to the conda channels, run the following in a terminal. ::

   conda config --add channels conda-forge

We want to install our packages in a suitable conda environment.
The following creates and activates a new environment named ``diffpy-utils`` ::

    conda create -n diffpy-utils python=3
    conda activate diffpy-utils

Then, to fully install ``diffpy.utils`` in our active environment, run ::

    conda install diffpy.utils

Another option is to use ``pip`` to download and install the latest release from
`Python Package Index <https://pypi.python.org>`_.
To install using ``pip`` into your ``diffpy-utils`` environment, we will also have to install dependencies ::

   pip install numpy
   pip install diffpy.utils

For those planning to use functions in the ``diffpy.utils.wx`` module, you will also need to install ``wxPython``.
Both of the following lines will install this package. ::

    conda install wxPython
    pip install wxPython

If you prefer to install from sources, after installing the dependencies, obtain the source archive from
`GitHub <https://github.com/diffpy/diffpy.utils/>`_. Once installed, ``cd`` into your ``diffpy.utils`` directory
and run the following ::

   pip install .

To check the installation integrity, if the following passes all checks, you are good! ::

   pip install pytest
   python -m diffpy.utils.tests.run


DEVELOPMENT
------------------------------------------------------------------------

diffpy.utils is an open-source software developed as a part of the
DiffPy-CMI complex modeling initiative at the Brookhaven National
Laboratory.  The diffpy.utils sources are hosted at
https://github.com/diffpy/diffpy.utils.

Feel free to fork the project and contribute.  To install diffpy.utils
in a development mode, with its sources being directly used by Python
rather than copied to a package directory, use the following in the root
directory ::

   pip install -e .

Note that this is only supported for `setuptools` version 62.0 and above.


CONTACTS
------------------------------------------------------------------------

For more information on diffpy.utils please visit the project web-page

http://www.diffpy.org/

or email Prof. Simon Billinge at sb2896@columbia.edu.
