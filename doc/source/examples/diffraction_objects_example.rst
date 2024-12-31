.. _Diffraction Objects Example:

:tocdepth: -1

Diffraction Objects Example
###########################

This example will demonstrate how to use the functions in the ``diffpy.utils.diffraction_objects`` module
to create a ``DiffractionObject`` instance and analyze your diffraction data using relevant functions.

To create a ``DiffractionObject``, you need to specify the type of the independent variable
(referred to as ``xtype``, e.g., one of ``q``, ``tth``, or ``d``),
the ``xarray`` of the ``x`` values, and a ``yarray`` of the corresponding intensity values.
It is strongly encouraged to specify the ``wavelength`` in order to access
most of the other functionalities in the class.
Additionally, you can specify the type of your scattering experiment using the ``scat_quantity`` parameter,
the name of your diffraction object using the ``name`` parameter,
and a ``metadata`` dictionary containing relevant information about the data. Here's an example:

.. code-block:: python

    import numpy as np
    from diffpy.utils.diffraction_objects import DiffractionObject

    x = np.array([0.12, 0.24, 0.31, 0.4])  # independent variable (e.g., q)
    y = np.array([10, 20, 40, 60])  # intensity values
    metadata = {
        "sample": "rock salt from the beach",
        "composition": "NaCl",
        "temperature": "300 K,",
        "experimenters": ["Phil", "Sally"]
    }

    my_do = DiffractionObject(
         xarray=x,
         yarray=y,
         xtype="q",
         wavelength=1.54,
         scat_quantity="x-ray",
         name="beach_rock_salt_1",
         metadata=metadata
    )

By creating a ``DiffractionObject`` instance, you store not only the diffraction data
but also all the associated information for analysis.

``DiffractionObject`` automatically populates the ``xarray`` onto each of ``q``, ``tth``, and ``d``-spacing.
Let's say you want to plot your data vs. Q.  To do this you would type

.. code-block:: python

    import matplotlib.pyplot as plt

    plt.plot(my_do.on_q()[0], my_do.on_q()[1])

and to plot the same data vs. two-theta type

.. code-block:: python

    plt.plot(my_do.on_tth()[0], my_do.on_tth()[1])

These `on_q()`, `on_tth()`, etc., methods return a list with the x-array as the first element
and the intensity array as the second element.

We can also accomplish the same thing by passing the xtype as a string to the ``on_xtype()`` method,
i.e.,

.. code-block:: python

    data_on_q = my_do.on_xtype("q")
    data_on_tth = my_do.on_xtype("tth")
    data_on_d = my_do.on_xtype("d")
    plt.plot(data_on_d[0], data_on_d[1])

This makes it very easy to compare a diffraction pattern that was measured or calculated
on one ``xtype`` with one that was measured or calculated on another.  E.g., suppose that you
have a calculated powder pattern from a CIF file that was calculated on a d-spacing grid using
some software package, and
you want to know if a diffraction pattern you have measured on a Q-grid is the same material.
You could simply load them both as diffraction objects and plot them together on the same grid.

.. code-block:: python

    calculated = DiffractionObject(xcalc, ycalc, "d")
    measured = DiffractionObject(xmeas, ymeas, "tth", wavelength=0.717)
    plt.plot(calculated.on_q()[0], calculated.on_q()[1])
    plt.plot(measured.on_q()[0], measured.on_q()[1])
    plt.show()

Now, let's say that these two diffraction patterns were on very different scales.  The measured one
has a peak intensity of 10,000, but the calculated one only goes to 1.
With diffraction objects this is easy to handle.  We choose a point on the x-axis where
we want to scale the two together and we use the ``scale_to()`` method,

Continuing the example above, if we wanted to scale the two patterns together at a position
Q=5.5 inverse angstroms, where for the sake of argument we assume the
calculated curve has a strong peak,
we would replace the code above with

.. code-block:: python

    plt.plot(calculated.on_q()[0], calculated.on_q()[1])
    plt.plot(measured.scale_to(calculated, q=5.5).on_q()[0], measured.scale_to(calculated, q=5.5).on_q()[1])
    plt.show()

The ``scale_to()`` method returns a new ``DiffractionObject`` which we can assign to a new
variable and make use of.

The default behavior is to align the objects based on the maximal value of each diffraction object.

.. code-block:: python

    scaled_measured = measured.scale_to(calculated)

If this doesn't give the desirable results, you can specify an ``xtype=value`` to scale
based on the closest x-value in both objects. For example:

.. code-block:: python

    scaled_measured = measured.scale_to(calculated, q=5.5)

For convenience, you can also apply an offset to the scaled new diffraction object with the optional
``offset`` argument, for example,

.. code-block:: python

    scaled_and_offset_measured = measured.scale_to(calculated, q=5.5, offset=0.5)

DiffractionObject convenience functions
---------------------------------------

1. create a copy of a diffraction object using the ``copy`` method
   when you want to preserve the original data while working with a modified version.

.. code-block:: python

    copy_of_calculated = calculated.copy()

2. test the equality of two diffraction objects.  For example,

.. code-block:: python

    diff_object2 = diff_object1.copy()
    diff_object2 == diff_object1

will return ``True``.

3. make arithmetic operations on the intensities of diffraction objects.
For example, you can do scalar operations on a single diffraction object,
which will modify the intensity values (``yarrays``) without affecting other properties:

.. code-block:: python

    increased_intensity = diff_object1 + 5      # Increases the intensities by 5
    decreased_intensity = diff_object1 - 1      # Decreases the intensities by 1
    doubled_object = 2 * diff_object1           # Double the intensities
    reduced_intensity = diff_object1 / 2        # Halves the intensities

You can also do binary operations between two diffraction objects, as long as they are on the same ``q/tth/d-array``.
The operation will apply to the intensity values, while other properties
(such as ``xarrays``, ``xtype``, and ``metadata``) will be inherited
from the left-hand side diffraction object (``diff_object1``).
For example:

.. code-block:: python

    sum_object = diff_object1 + diff_object2            # Sum the intensities
    subtract_scaled = diff_object1 - 5 * diff_object2   # Subtract 5 * obj2 from obj 1
    multiplied_object = diff_object1 * diff_object2     # Multiply the intensities
    divided_object = diff_object1 / diff_object2        # Divide the intensities

You cannot perform operations between diffraction objects and incompatible types.
For example, attempting to add a diffraction object and a string will raise an error:

.. code-block:: python

    diff_object1 + "string_value"       # This will raise an error

4. get the value of the DiffractionObject at a given point in one of the xarrays

.. code-block:: python

    tth_ninety_index = diff_object1.get_array_index(90, xtype="tth")
    intensity_at_ninety = diff_object1.on_tth()[1][tth_ninety_index]

If you do not specify an ``xtype``, it will default to the ``xtype`` used when creating the ``DiffractionObject``.
For example, if you have created a ``DiffractionObject`` called ``do`` with ``xtype="q"``,
you can find its closest index for ``q=0.25`` by typing either of the following:

.. code-block:: python

    print(do._input_xtype)     # remind ourselves which array was input.  prints "q" in this case.
    index = do.get_array_index(0.25) # no xtype passed, defaults to do._input_xtype, or in this example, q
    index = do.get_array_index(0.25, xtype="q") # explicitly choose an xtype to specify a value

5. The ``dump`` function saves the diffraction data and relevant information to an xy format file with headers
(widely used chi format used, for example, by Fit2D and diffpy.  These files can be read by ``LoadData()``
in ``diffpy.utils.parsers``).

You can choose which of the data axes (``q``, ``tth``, or ``d``) to export, with ``q`` as the default.

.. code-block:: python

    # Assume you have created a Diffraction Object do
    file = "diffraction_data.chi"
    do.dump(file, xtype="q")

In the saved file ``diffraction_data.chi``,
relevant metadata are also written in the header (``username``, ``name``, ``scattering quantity``, ``metadata``, etc.).
The datetime when the DiffractionObject was created and the version of the
software (see the Section on ``get_package_info()`` for more information)
is automatically recorded as well.
The diffraction data is saved as two columns: the ``q`` values and corresponding intensity values.
This ensures your diffraction data, along with all other information,
is properly documented and saved for future reference.
