.. diffpy.utils documentation master file, created by
   sphinx-quickstart on Thu Jan 30 15:49:41 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


####################################################
diffpy.utils's documentation!
####################################################

Software version |release|.

Last updated |today|.

diffpy.utils - general purpose shared utilities for the diffpy libraries.

The diffpy.utils package provides functions to easily find and load data from
text files, various utilites related to data parsing and manipulation, and a set
of common functions for grid manipulation used by the GUI front-end
diffpy.pdfgui.

The data loading utilities can be used with most automatically generated powder
diffraction and PDF data files.  They work by searching for matrix blocks of
data containing a constant number of columns and a pre-set minimum number of
rows. By default all columns will be read and returned as a multi-dimensional
numpy array or as a tuple of individual columns; a sub-set of columns can also
be selected to be read and the rest ignored.

The data manipulation tools contains interpolation functions that can be used to
resample a PDF or other profile function over a new grid. Interpolation is based
on the Whittaker-Shannon formula.


===================
Disclaimer
===================

.. include:: ../../../LICENSE.txt

================
Acknowledgments
================

Developers
-----------

diffpy.Structure is developed and maintained by

.. literalinclude:: ../../../AUTHORS.txt

======================================
Installation
======================================

.. include:: install.rst

API and Index
==================

.. toctree::
   :maxdepth: 3

   api/diffpy.utils.rst

* :ref:`genindex`
* :ref:`search`
