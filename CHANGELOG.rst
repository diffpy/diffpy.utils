=============
Release Notes
=============

.. current developments

v3.3.0
====================

**Added:**

* Diffraction_objects for easier manipulations of diffraction objects
* dump method to Diffraction_object



v3.2.7
====================



v3.2.6
====================



v3.2.5
====================

**Fixed:**

* Added a wx import to fix module not found error.



v3.2.4
====================

**Added:**

* New documentation build.
* Added examples for file parsers and resampling.
* Tested for Jupyter Notebook compatibility.

**Changed:**

* Theme changed from `sphinx_py3doc_enhanced_theme` to `sphinx_rtd_theme`.
* User now warned when data_table data overwrites hdata (header) data.



v3.2.3
====================

**Added:**

* Compatability with Python 3.12.0rc3, 3.11.
* CI Coverage.
* New tests for loadData function.
* loadData function now toggleable. Can return either (a) data read from data blocks or (b) header information stored
  above the data block.

**Removed:**

* Remove use of pkg_resources (deprecated).
* No longer use Travis.



v3.1.0
====================

**Added:**

* Compatibility with Python 3.10, 3.9, 3.8.

**Removed:**

* Remove the support for Python 3.5, 3.6.



v3.0.0
====================

**Added:**

* Compatibility with Python 3.7, 3.6, 3.5 in addition to 2.7.

**Changed:**

* Switch to platform-independent "noarch" Anaconda package.

**Deprecated:**

* Variable `__gitsha__` in the `version` module which was renamed to `__git_commit__`.
