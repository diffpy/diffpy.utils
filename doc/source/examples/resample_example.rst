.. _Resample Example:

:tocdepth: -1

Resampling Example
##################

This example will demonstrate how we can use diffpy.utils functions to resample a function on a denser grid.
Specifically, we will resample the grid of one function to match another for us to easily compare the two.
Then we will show how this resampling method lets us create a perfect reconstruction of certain functions
given enough datapoints.

1) To start, unzip :download:`parser_data<./example_data/parser_data.zip>`. Then, load the data table from ``Nickel.gr``
   and ``NiTarget.gr``. These datasets are based on data from `Atomic Pair Distribution Function Analysis: A Primer
   <https://global.oup.com/academic/product/atomic-pair-distribution-function-analysis-9780198885801?cc=us&lang=en&>`_.
   ::

     from diffpy.utils.parsers.loaddata import loadData
     nickel_datatable = loadData('<PATH to Nickel.gr>')
     nitarget_datatable = loadData('<PATH to NiTarget.gr>')

   Each data table has two columns: first is the grid and second is the function value.
   To extract the columns, we can utilize the serialize function ... ::

     from diffpy.utils.parsers.serialization import serialize_data
     nickel_data = serialize_data('Nickel.gr', {}, nickel_datatable, dt_colnames=['grid', 'func'])
     nickel_grid = nickel_data['Nickel.gr']['grid']
     nickel_func = nickel_data['Nickel.gr']['func']
     target_data = serialize_data('NiTarget.gr', {}, nitarget_datatable, dt_colnames=['grid', 'function'])
     target_grid = nickel_data['Nickel.gr']['grid']
     target_func = nickel_data['Nickel.gr']['func']

   ... or you can use any other column extracting method you prefer.

2) If we plot the two on top of each other ::

     import matplotlib.pyplot as plt
     plt.plot(target_grid, target_func, linewidth=3)
     plt.plot(nickel_grid, nickel_func, linewidth=1)

   they look pretty similar, but to truly see the difference, we should plot the difference between the two.
   We may want to run something like ... ::

     import numpy as np
     difference = np.subtract(target_func, nickel_func)

   ... but this will only produce the right result if the ``target_func`` and ``nickel_func`` are on the same grid.
   Checking the lengths of ``target_grid`` and ``nickel_grid`` shows that these grids are clearly distinct.

3) However, we can resample the two functions to be on the same grid. Since both functions have grids spanning
   ``[0, 60]``, let us define a new grid ... ::

     grid = np.linspace(0, 60, 6001)

   ... and use the diffpy.utils ``wsinterp`` function to resample on this grid.::

     from diffpy.utils.resampler import wsinterp
     nickel_resample = wsinterp(grid, nickel_grid, nickel_func)
     target_resample = wsinterp(grid, target_grid, target_func)

   We can now plot the difference to see that these two functions are quite similar.::

     plt.plot(grid, target_resample)
     plt.plot(grid, nickel_resample)
     plt.plot(grid, target_resample - nickel_resample)

   This is the desired result as the data in ``Nickel.gr`` is every tenth data point in ``NiTarget.gr``.
   This also shows us that ``wsinterp`` can help us reconstruct a function from incomplete data.

4) In order for our function reconstruction to be perfect up to a truncation error, we require that (a) the function is
   a Fourier transform of a band-limited dataset and (b) the original grid has enough equally-spaced datapoints based on
   the Nyquist sampling theorem.

     * If our function :math:`F(r)` is of the form :math:`F(r) = \int_0^{qmax} f(q)e^{-iqr}dq` where :math:`qmax` is
       the bandlimit, then for a grid spanning :math:`r \in [rmin, rmax]`, the Nyquist sampling theorem tells us we
       require at least :math:`qmax * (rmin - rmax) / \pi` equally-spaced datapoints.

   In the case of our dataset, our band-limit is ``qmax=25.0`` and our function spans :math:`r \in (0.0, 60.0)`.
   Thus, our original grid requires :math:`25.0 * 60.0 / \pi < 478`. Since our grid has :math:`601` datapoints, our
   reconstruction was perfect as shown from the comparison between ``Nickel.gr`` and ``NiTarget.gr``.

   This computation is implemented in the function ``nsinterp``.::

     from diffpy.utils.resampler import nsinterp
     qmin = 0
     qmax = 25
     nickel_resample = (nickel_grid, nickel_func, qmin, qmax)
