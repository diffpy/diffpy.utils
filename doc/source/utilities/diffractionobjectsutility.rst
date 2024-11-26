.. _Diffraction Objects Utility:

Diffraction Objects Utility
===========================

The ``diffpy.utils.scattering_objects.diffraction_objects`` module provides functions
for managing and analyzing diffraction data, including angle-space conversions
and interactions between diffraction data.

- ``q_to_tth()``: Converts an array of q values to their corresponding two theta values, based on specified wavelength.
- ``tth_to_q()``: Converts an array of two theta values to their corresponding q values, based on specified wavelength.

  These functions help developers standardize diffraction data and update the arrays
  in the associated ``DiffractionObject``, enabling easier analysis and further processing.

For a more in-depth tutorial for how to use these functions, click :ref:`here <Diffraction Objects Example>`.
