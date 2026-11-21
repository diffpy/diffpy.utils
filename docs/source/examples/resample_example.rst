.. _Resample Example:

:tocdepth: -1

Resampling Example
##################

This example compares two nickel pair distribution functions sampled on different grids.
We will interpolate the coarser dataset onto the reference grid and plot the difference.

1) Unzip :download:`parser_data<./example_data/parser_data.zip>` and run the
   example from the directory containing ``Nickel.gr`` and ``NiTarget.gr``.
   These datasets are based on data from `Atomic Pair Distribution Function Analysis: A Primer
   <https://global.oup.com/academic/product/atomic-pair-distribution-function-analysis-9780198885801?cc=us&lang=en&>`_.
   The first column is the distance grid and the second is the function value.

.. code-block:: python

    from diffpy.utils.parsers import load_data

    nickel_grid, nickel_func = load_data("Nickel.gr").T
    target_grid, target_func = load_data("NiTarget.gr").T

2) Plot both functions on their native grids. Both span 0 to 60 Å.
   The nickel file has 601 points spaced by 0.1 Å, and the reference has
   6001 points spaced by 0.01 Å. Every tenth reference point coincides
   with a sample in the nickel file.

.. code-block:: python

    import matplotlib.pyplot as plt
    import numpy as np

    plt.plot(target_grid, target_func, label="Reference")
    plt.plot(nickel_grid, nickel_func, ".", label="Nickel samples")
    plt.legend()

3) To compare the functions point by point, use ``wsinterp`` to evaluate the
   nickel samples at the reference distances. The residual is close to zero at
   the original sample positions. Between those positions, the maximum absolute
   difference is about 0.0063 for these files.

.. code-block:: python

    from diffpy.utils.resampler import wsinterp

    nickel_resample = wsinterp(target_grid, nickel_grid, nickel_func)
    residual = target_func - nickel_resample
    print(np.max(np.abs(residual)))

    plt.figure()
    plt.plot(target_grid, residual)
    plt.xlabel("Distance (Å)")
    plt.ylabel("Reference − interpolated nickel")

4) For a signal band-limited to :math:`Q_\mathrm{max}`, the Nyquist sampling
   interval in real space is :math:`\pi / Q_\mathrm{max}`. Here
   :math:`Q_\mathrm{max} = 25` Å⁻¹ gives an interval of about
   0.126 Å. The nickel grid samples more finely than that. Its finite range
   still limits the accuracy of sinc interpolation between samples.

   To evaluate the same data on the grid chosen by ``nsinterp``, use both
   returned arrays as the new distances and function values.

.. code-block:: python

    from diffpy.utils.resampler import nsinterp

    ns_grid, ns_func = nsinterp(nickel_grid, nickel_func, qmin=0, qmax=25)
