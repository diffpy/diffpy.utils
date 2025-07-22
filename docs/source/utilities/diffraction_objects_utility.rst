.. _Diffraction Objects Utility:

Diffraction Objects Utility
===========================

The ``diffpy.utils.diffraction_objects`` module provides a set of powerful functions for analyzing diffraction data.

- ``DiffractionObject()``: This function creates a diffraction object that stores your diffraction data
  and associated information. If a ``wavelength`` is specified, it can automatically populate data
  across different independent axes (e.g., ``q``, ``tth``, and ``d``).

- ``on_xtype()``: This function allows developers to access diffraction data on different independent axes
  (``q``, ``tth``, and ``d``).
  It is useful when you need to convert or view the data between axes,
  working with the axis that best fits your analysis.

- ``get_array_index()``: This function finds the closest index in the independent variable axis (``xarray``)
  to a targeted value. It simplifies the process of working with different spacing.

- ``scale_to()``: This function rescales one diffraction object to align with another at a specific value.
  This is helpful for comparing diffraction data with different intensity values or lengths,
  ensuring they are directly comparable and visually aligned.

- ``copy()``: This function creates a deep copy of a diffraction object,
  allowing you to preserve the original data while making modifications to a separate copy.

- ``dump()``: This function saves both diffraction data and all associated information to a file.
  It also automatically tracks the analysis time and software version you used.

For a more in-depth tutorial for how to use these tools, click :ref:`here <Diffraction Objects Example>`.
