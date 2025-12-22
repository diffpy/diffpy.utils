.. _mu calc Example:

:tocdepth: -1

X-ray Absorption Coefficient (μ) Examples
#########################################

These examples will demonstrate how to calculate the X-ray absorption
coefficient, μ, using different methods provided in ``diffpy.utils``.


.. admonition:: Methods for obtaining X-ray absorption coefficient

   Obtaining μ can be done in **two
   different ways** using ``diffpy.utils``.

   1. **Using a "z-scan" measurement**: Perform a z-scan measurement
      on the sample and use ``diffpy.utils.tools.compute_mud`` to calculate
      μ.
   2. **Using tabulated values**: Given composition, density, and X-ray energy,
      use ``diffpy.utils.tools.compute_mu_using_xraydb`` to calculate μ from
      tabulated values.

Why is μ Important?
-----------------------

The X-ray absorption coefficient, μ, quantifies how much X-ray
radiation is absorbed by a material per unit length. It is a critical
parameter in many scientific techniques.

For example, when calculating pair distribution functions (PDFs)
using ``diffpy.pdfgetx``,
a key assumption is that the X-ray absorption is negligible.
This is frequently the case for high-energy X-rays. However,
this must be corrected for when using low energy X-rays, such
as those from a laboratory source. To correct for X-ray absorption,
the X-ray absorption coefficient, μ, must be known.

.. admonition:: Correcting for X-ray Absorption with ``diffpy.labpdfproc``

   If your objective is to correct for X-ray absorption in PDF calculations,
   please refer to our package ``diffpy.labpdfproc``. This package is specifically
   designed to correct your laboratory X-ray PDF data for absorption effects.
   More information can be found in the
   `diffpy.labpdfproc documentation <https://www.diffpy.org/diffpy.labpdfproc//>`_.


Calculating μ from a "z-scan" Measurement
-----------------------------------------

.. note::

   The data we will be using for this example can be found here,
   `FIXME <https://www.diffpy.org/diffpy.utils/examples/zscan_example_data.txt>`_.

A "z-scan" measurement is the measured transmission of your X-ray incident beam
as a function of sample position. This is obtained by moving the sample
along the X-ray beam (z-direction) and recording the transmitted
intensity at each position. This measured data looks something like this,

.. image:: ../images/FIXME
   :alt: Example of a z-scan measurement.
   :align: center
   :width: 200px

Using this z-scan data, you can calculate **μ·d**, where d is the inner diameter of
your sample capillary. To do this, simply pass your z-scan measurement to the ``compute_mud``
function from the ``diffpy.utils.tools`` module.


First, import the ``compute_mud`` function,

.. code-block:: python

   from diffpy.utils.tools import compute_mud

Next, pass the filepath to the function,

.. code-block:: python

   filepath = "zscan_example_data.txt"
   capillary_diameter = 0.5 # mm
   mud = compute_mud(filepath)
   print(f"Calculated mu*d: {round(mud, 3)}")
   print(f"Calculated mu: {round(mud / capillary_diameter, 3)} mm^-1")

This will output the calculated value of μ·d, which is unitless, and μ in mm\ :sup:`-1`.

.. code-block:: console

   Calculated mu*d: FIXME
   Calculated mu: FIXME mm^-1

Calculating μ from Tabulated Values
-----------------------------------

The function to calculate μ from tabulated values is located
in the ``diffpy.utils.tools`` module. So first, import the function,

.. code-block:: python

   from diffpy.utils.tools import compute_mu_using_xraydb

To calculate μ, you need to know the sample composition, and X-ray energy, and sample mass density (g/cm\ :sup:`3`).

.. code-block:: python

   composition = "Fe2O3"
   energy_keV = 17.45 # Mo K-alpha energy
   sample_mass_density = 5.24 # g/cm^3

Now calculate μ using the ``compute_mu_using_xraydb`` function.

.. code-block:: python

   mu_density = compute_mu_using_xraydb(composition, energy_keV, sample_mass_density=sample_mass_density)
   print(f"Calculated mu from sample_mass_density: {round(mu_density, 3)} mm^-1")

This will output the calculated X-ray absorption coefficient, μ, in mm\ :sup:`-1`.

.. code-block:: console

   Calculated mu from sample_mass_density: 13.967 mm^-1
