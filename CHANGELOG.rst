=============
Release Notes
=============

.. current developments

3.6.0
=====

**Added:**

* unit tests for initializing DiffractionObject with empty array in xarray and yarray
* function to return the index of the closest value to the specified value in an array.
* functions to convert between d and q
* catch division by zero warning messages in tests
* functionality to raise useful warning and error messages during angular conversion between two theta and q
* Improved API documentation in `DiffractionObject` methods and properties using the NumPy docstring format and PEP 256
* validate xtype belongs to XQUANTITIES during DiffractionObject init
* Group's Pytest practices for using @pytest.mark.parametrize in test_diffraction_objects.py
* unit tests for __add__ operation for DiffractionObject
* Better wording on the capture user info functionality
* Spelling check via Codespell in pre-commit
* prettier pre-commit hook for automatic linting of .yml, .json, and .md files
* Function that can be used to compute muD (absorption coefficient) from a file containing an absorption profile
from a line-scan through the sample
* sbillinge username as the authorized admin for GitHub release workflow in `build-wheel-release-upload.yml`
* function to compute x-ray attenuation coefficient (mu) using XrayDB
* class docstring for `DiffractionObject`
* docforamtter in pre-commit for automatic formatting of docstrings to PEP 257
* Function nsinterp for automatic interpolation onto the Nyquist-Shannon grid.
* functionality to return the 2D array based on the specified xtype
* functionality in dump to allow writing data on dspace
* addition, multiplication, subtraction, and division operators between two DiffractionObject instances or a scalar value with another DiffractionObject for modifying yarray (intensity) values.
* functionality to rescale diffraction objects, placing one on top of another at a specified point
* new feature in `scale_to()`: default scaling is based on the max q-value in each diffraction object.
* functions to convert between d and tth
* unit test for expected warning when no wavelength is provided for DiffractionObject init
* copy() method for DiffractionObject instance
* docstrings for `on_q`, `on_tth`, `on_d`, and `dump` in `diffraction_objects.py`.
* prevent direct modification of `all_arrays` using `@property`
* Information on how to update the default user information
* Example docs for basic DiffractionObject usage
* deploy github pages documentation on pre-release
* Gettable `id` property to `DiffractionObject`

**Changed:**

* Refactor get_user_info to separate the tasks of getting the info from config files
and creating config files when they are missing.
* test comment format with compact style without extra line for each comment
* Rename `input_scattering_quantity` to `input_data` in `DiffractionObject` init
* refactor `q_to_tth()` and `tth_to_q()` into `diffpy.utils.transforms` to make them available outside
DiffractionObject
* Moved resampler out of parsers, new path is diffpy.utils.resampler
* Rename the `isfloat` function to `is_number`, and move it to the `diffpy/utils/utilsvalidators.py` directory
* arrays and attributes now can be inserted when a DiffractionObject is instantiated
* data are now stored as a (len(x),4) numpy array with intensity in column 0, the q, then tth, then d
* `DiffractionObject.on_q`, `...on_tth` and `...on_d` are now methods and called as `DiffractionObject.on_q()` etc.`
* \tests directory tree to match \src
* DiffractionObject's "id" property renamed to "uuid"
* `DiffractionObject` requires 3 input parameters of `xarray`, `yarray`, `xtype`, to be instantiated.  It can be instantiated with empty arrays.
* Paths in our documentation reflect changes made in code.
* Enumerated list for the different ways to set user information

**Deprecated:**

* `resample` function in resampler. Replaced with `wsinterp` with better functionality.
* Diffraction_object class, renamed to DiffractionObject

**Fixed:**

* additional information to users to relieve frustration in finding how to update global config
* Unittest to Pytest migration for test_loaddata.py
* file paths of the test files according to new \tests directory tree
* Typo for get_package_info example
* return type of `get_array_index` method in `DiffractionObject` to return integer instead of list

**Removed:**

* scattering_objects layer in importing diffraction_objects
* `user_config.py`. Replaced by `_load_config` and `check_and_build_global_config` in `tools.py`.
* Relative imports in parser's __init__.py
* `set_angles_from_list`, `set_angles_from`, `set_qs_from_range` methods in `DiffractionObject`


3.5.0
=====

**Added:**

* Support for Python 3.13

**Removed:**

* Support for Python 3.10


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

* Compatibility with Python 3.12.0rc3, 3.11.
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
