|Icon| |title|_
===============

.. |title| replace:: diffpy.utils
.. _title: https://diffpy.github.io/diffpy.utils

.. |Icon| image:: https://avatars.githubusercontent.com/diffpy
        :target: https://diffpy.github.io/diffpy.utils
        :height: 100px

|PyPi| |Forge| |PythonVersion| |PR|

|CI| |Codecov| |Black| |Tracking|

.. |Black| image:: https://img.shields.io/badge/code_style-black-black
        :target: https://github.com/psf/black

.. |CI| image:: https://github.com/diffpy/diffpy.utils/actions/workflows/matrix-and-codecov-on-merge-to-main.yml/badge.svg
        :target: https://github.com/diffpy/diffpy.utils/actions/workflows/matrix-and-codecov-on-merge-to-main.yml

.. |Codecov| image:: https://codecov.io/gh/diffpy/diffpy.utils/branch/main/graph/badge.svg
        :target: https://codecov.io/gh/diffpy/diffpy.utils

.. |Forge| image:: https://img.shields.io/conda/vn/conda-forge/diffpy.utils
        :target: https://anaconda.org/conda-forge/diffpy.utils

.. |PR| image:: https://img.shields.io/badge/PR-Welcome-29ab47ff

.. |PyPi| image:: https://img.shields.io/pypi/v/diffpy.utils
        :target: https://pypi.org/project/diffpy.utils/

.. |PythonVersion| image:: https://img.shields.io/pypi/pyversions/diffpy.utils
        :target: https://pypi.org/project/diffpy.utils/

.. |Tracking| image:: https://img.shields.io/badge/issue_tracking-github-blue
        :target: https://github.com/diffpy/diffpy.utils/issues

diffpy.utils Package
========================================================================

General purpose shared utilities for the diffpy libraries.

The diffpy.utils package provides functions for extracting array data from
variously formatted text files, an interpolation function based on the
Whittaker-Shannon formula that can be used to resample a PDF or other profile
function over a new grid, `Diffraction_objects` for conveniently manipulating
diffraction data, and some wx GUI utilities used by the PDFgui
program.

Citation
--------

If you use this program for a scientific research that leads
to publication, we ask that you acknowledge use of the program
by citing the following paper in your publication:

   P. Juhás, C. L. Farrow, X. Yang, K. R. Knox and S. J. L. Billinge,
   `Complex modeling: a strategy and software program for combining
   multiple information sources to solve ill posed structure and
   nanostructure inverse problems
   <http://dx.doi.org/10.1107/S2053273315014473>`__,
   *Acta Crystallogr. A* **71**, 562-568 (2015).

Documentation
-------------

Documentation may be found at, https://diffpy.github.io/diffpy.utils

Installation
------------

The preferred method is to use `Miniconda Python
<https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html>`_
and install from the "conda-forge" channel of Conda packages.

To add "conda-forge" to the conda channels, run the following in a terminal. ::

        conda config --add channels conda-forge

We want to install our packages in a suitable conda environment.
The following creates and activates a new environment named ``diffpy.utils_env`` ::

        conda create -n diffpy.utils_env diffpy.utils
        conda activate diffpy.utils_env

To confirm that the installation was successful, type ::

        python -c "import diffpy.utils; print(diffpy.utils.__version__)"

The output should print the latest version displayed on the badges above.

If the above does not work, you can use ``pip`` to download and install the latest release from
`Python Package Index <https://pypi.python.org>`_.
To install using ``pip`` into your ``diffpy.utils_env`` environment, type ::

        pip install diffpy.utils

If you prefer to install from sources, after installing the dependencies, obtain the source archive from
`GitHub <https://github.com/diffpy/diffpy.utils/>`_. Once installed, ``cd`` into your ``diffpy.utils`` directory
and run the following ::

        pip install .

Getting Started
---------------

You may consult our `online documentation <https://diffpy.github.io/diffpy.utils>`_ for tutorials and API references.

Support and Contribute
----------------------

`Diffpy user group <https://groups.google.com/g/diffpy-users>`_ is the discussion forum for general questions and discussions about the use of diffpy.utils. Please join the diffpy.utils users community by joining the Google group. The diffpy.utils project welcomes your expertise and enthusiasm!

If you see a bug or want to request a feature, please `report it as an issue <https://github.com/diffpy/diffpy.utils/issues>`_ and/or `submit a fix as a PR <https://github.com/diffpy/diffpy.utils/pulls>`_. You can also post it to the `Diffpy user group <https://groups.google.com/g/diffpy-users>`_.

Feel free to fork the project and contribute. To install diffpy.utils
in a development mode, with its sources being directly used by Python
rather than copied to a package directory, use the following in the root
directory ::

        pip install -e .

To ensure code quality and to prevent accidental commits into the default branch, please set up the use of our pre-commit
hooks.

1. Install pre-commit in your working environment by running ``conda install pre-commit``.

2. Initialize pre-commit (one time only) ``pre-commit install``.

Thereafter your code will be linted by black and isort and checked against flake8 before you can commit.
If it fails by black or isort, just rerun and it should pass (black and isort will modify the files so should
pass after they are modified). If the flake8 test fails please see the error messages and fix them manually before
trying to commit again.

Improvements and fixes are always appreciated.

Before contribuing, please read our `Code of Conduct <https://github.com/diffpy/diffpy.utils/blob/main/CODE_OF_CONDUCT.rst>`_.

Contact
-------

For more information on diffpy.utils please visit the project `web-page <https://diffpy.github.io/>`_ or email Prof. Simon Billinge at sb2896@columbia.edu.
