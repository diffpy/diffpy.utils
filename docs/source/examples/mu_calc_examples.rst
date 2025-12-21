.. _mu calc Example:

:tocdepth: -1

Lab-collected PDF Correction Examples
######################################

These examples will demonstrate how to correct X-ray diffraction data
to compute pair distribution functions (PDFs) from lab-collected X-ray
diffraction experiments.

When calculating PDFs using ``diffpy.pdfgetx``,
a key assumption is that the X-ray absorption is negligible.
This is frequently the case for high-energy X-rays.
However, this must be corrected for when using low energy
X-rays, such as those from a laboratory source.
To correct for X-ray absorption, the X-ray absorption coefficient, μ,
must be known.

.. admonition:: Correction methods for X-ray absorption

   Correcting your diffraction data can be done in **three
   different ways** using ``diffpy.utils``.

   1. **Using a known μ value**: If the X-ray absorption coefficient μ
      is already known for your sample, supply this value along with the capillary diameter
      to directly correct the diffraction data.
   2. **Using a "z-scan" measurement**: Perform a z-scan measurement
      on the sample to measure X-ray absorption and extract
      the corresponding μ value, which is then used to correct the data.
   3. **Using tabulated values**: Find μ using tabulated absorption coefficients based on the sample
      composition, density, and X-ray energy, and use this value to apply the
      absorption correction.

Using a known μ value
---------------------

example here

Using a "z-scan" measurement
----------------------------

Example here

Using tabulated values
----------------------------

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
   print(f"Calculated mu from sample_mass_density: {mu_density} cm^-1")
