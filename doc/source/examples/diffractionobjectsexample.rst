.. _Diffraction Objects Example:

:tocdepth: -1

Diffraction Objects Example
###########################

This example will demonstrate how to use the ``DiffractionObject`` class in the
``diffpy.utils.scattering_objects.diffraction_objects`` module to process and analyze diffraction data.

1) We have the function ``q_to_tth`` to convert q to two theta values in degrees, and ``tth_to_q`` to do the reverse.
   You can use these functions with a pre-defined ``DiffractionObject``. ::

    # convert q to tth
    from diffpy.utils.scattering_objects.diffraction_objects import DiffractionObject
    test = DiffractionObject(wavelength=1.54)
    test.on_q = [[0, 0.2, 0.4, 0.6, 0.8, 1], [1, 2, 3, 4, 5, 6]]
    test.q_to_tth()

   This function will convert your provided q array and return a two theta array in degrees.
   To load the converted array, you can either call ``test.q_to_tth()`` or ``test.on_q[0]``.

   Similarly, use the function ``tth_to_q`` to convert two theta values in degrees to q values. ::

    # convert tth to q
    from diffpy.utils.scattering_objects.diffraction_objects import DiffractionObject
    test = DiffractionObject(wavelength=1.54)
    test.on_tth = [[0, 30, 60, 90, 120, 180], [1, 2, 3, 4, 5, 6]]
    test.tth_to_q()

   To load the converted array, you can either call ``test.tth_to_q()`` or ``test.on_tth[0]``.

2) You can use these functions without specifying a wavelength. However, if so, the function will return an empty array,
   so we strongly encourage you to specify a wavelength when using these functions. ::

    from diffpy.utils.scattering_objects.diffraction_objects import DiffractionObject
    test = DiffractionObject()
    test.on_q = [[0, 0.2, 0.4, 0.6, 0.8, 1], [1, 2, 3, 4, 5, 6]]
    test.q_to_tth()

   In this case, the function will return an empty array on two theta.
