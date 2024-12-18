.. _Transforms Example:

:tocdepth: -1

Transforms Example
##################

This example will demonstrate how to use the functions in the
``diffpy.utils.transforms`` module to process and analyze diffraction data.

1) Converting from ``q`` to ``2theta`` or ``d``:
   If you have a 1D ``q``-array, you can use the ``q_to_tth`` and ``q_to_d`` functions
   to convert it to ``2theta`` or ``d``.

.. code-block:: python

    # Example: convert q to 2theta
    from diffpy.utils.transforms import q_to_tth
    wavelength = 0.71
    q = np.array([0, 0.2, 0.4, 0.6, 0.8, 1])
    tth = q_to_tth(q, wavelength)

    # Example: convert q to d
    from diffpy.utils.transforms import q_to_d
    q = np.array([0, 0.2, 0.4, 0.6, 0.8, 1])
    d = q_to_d(q)

(2) Converting from ``2theta`` to ``q`` or ``d``:
    For a 1D ``2theta`` array, you can convert it to ``q`` or ``d`` in a similar way.

.. code-block:: python

    # Example: convert 2theta to q
    from diffpy.utils.transforms import tth_to_q
    wavelength = 0.71
    tth = np.array([0, 30, 60, 90, 120, 180])
    q = tth_to_q(tth, wavelength)

    # Example: convert 2theta to d
    from diffpy.utils.transforms import tth_to_d
    wavelength = 0.71
    tth = np.array([0, 30, 60, 90, 120, 180])
    d = tth_to_d(tth, wavelength)

(3) Converting from ``d`` to ``q`` or ``2theta``:
    For a 1D ``d`` array, you can convert it to ``q`` or ``2theta``.

.. code-block:: python

    # Example: convert d to q
    from diffpy.utils.transforms import d_to_q
    d = np.array([1.0, 0.8, 0.6, 0.4, 0.2])
    q = d_to_q(d)

    # Example: convert d to 2theta
    from diffpy.utils.transforms import d_to_tth
    wavelength = 0.71
    d = np.array([1.0, 0.8, 0.6, 0.4, 0.2])
    tth = d_to_tth(d, wavelength)
