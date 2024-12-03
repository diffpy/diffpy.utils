.. _Diffraction Objects Example:

:tocdepth: -1

Diffraction Objects Example
###########################

This example will demonstrate how to use the ``DiffractionObject`` class in the
``diffpy.utils.diffraction_objects`` module to process and analyze diffraction data.

1) Assuming we have created a ``DiffractionObject`` called my_diffraction_pattern from a measured diffraction pattern,
   and we have specified the wavelength (see Section ??, to be added),
   we can use the ``q_to_tth`` and ``tth_to_q`` functions to convert between q and two-theta. ::

    # Example: convert q to tth
    my_diffraction_pattern.on_q = [[0, 0.2, 0.4, 0.6, 0.8, 1], [1, 2, 3, 4, 5, 6]]
    my_diffraction_pattern.q_to_tth()

   This function will convert your provided q array and return a two theta array in degrees.
   To load the converted array, you can either call ``test.q_to_tth()`` or ``test.on_q[0]``. ::

    # Example: convert tth to q
    from diffpy.utils.diffraction_objects import DiffractionObject
    my_diffraction_pattern.on_tth = [[0, 30, 60, 90, 120, 180], [1, 2, 3, 4, 5, 6]]
    my_diffraction_pattern.tth_to_q()

   Similarly, to load the converted array, you can either call ``test.tth_to_q()`` or ``test.on_tth[0]``.

2) Both functions require a wavelength to perform conversions. Without a wavelength, they will return empty arrays.
   Therefore, we strongly encourage you to specify a wavelength when using these functions. ::

    # Example: without wavelength specified
    my_diffraction_pattern.on_q = [[0, 0.2, 0.4, 0.6, 0.8, 1], [1, 2, 3, 4, 5, 6]]
    my_diffraction_pattern.q_to_tth()    # returns an empty array
