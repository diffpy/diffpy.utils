=============
Release Notes
=============

.. current developments

3.4.3
=====

**Added:**

* Diffraction_objects mentioned in the README

**Fixed:**

* Recut to group's package standard, fix installation, add GitHub release workflow
* setuptools-git-versioning from <2.0 to >= 2.0 in pyproject.toml
* Two Pytest warnings due to numpy and pytest mocker in test_dump function
* Add pip dependencies under pip.txt and conda dependencies under conda.txt


3.4.2
=====

**Added:**

* link docs in the README

**Changed:**

* removed need to install requirements separately when pip installing.

**Fixed:**

* Updated package structure to new group standard




3.4.0
=====

**Added:**

* utility for handling the capture of username and email for diffpy applications
* __eq__ method into Diffraction_object so we can equation two instances of a diffraction object

**Changed:**

* diffraction_object.dump now adds creation time and diffpy.utils version number to the output file

**Fixed:**

* fixed inadvertent overwrite of attributes on self.insert_scattering_quantity()



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
