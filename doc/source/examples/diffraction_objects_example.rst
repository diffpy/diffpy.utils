.. _Diffraction Objects Example:

:tocdepth: -1

Diffraction Objects Example
###########################

This example will demonstrate how to use the functions in the ``diffpy.utils.diffraction_objects`` module
to create a ``DiffractionObject`` instance and analyze your diffraction data using relevant functions.

1) To create a ``DiffractionObject``, you need to specify the type of the independent variable
   (referred to as ``xtype``, one of ``q``, ``tth``, or ``d``),
   an ``xarray`` of the corresponding values, and a ``yarray`` of the intensity values.
   It is strongly encouraged to specify the ``wavelength`` in order to access
   most of the other functionalities in the class.
   Additionally, you can specify the type of your scattering experiment using the ``scat_quantity`` parameter,
   the name of your diffraction object using the ``name`` parameter,
   and a ``metadata`` dictionary containing relevant information about the data. Here's an example: ::

    import numpy as np
    from diffpy.utils.diffraction_objects import DiffractionObject
    x = np.array([0.12, 0.24, 0.31, 0.4])  # independent variable (e.g., q)
    y = np.array([10, 20, 40, 60])  # intensity values
    metadata = {
        "sample": "rock salt from the beach",
        "composition": "NaCl",
        "temperature": "300 K,",
        "experimenters": "Phill, Sally"
    }
    do = DiffractionObject(
         xarray=x,
         yarray=y,
         xtype="q",
         wavelength=1.54,
         scat_quantity="x-ray",
         name="beach_rock_salt_1",
         metadata=metadata
    )
    print(do.metadata)

   By creating a ``DiffractionObject`` instance, you store not only the diffraction data
   but also all the associated information for analysis.

2) ``DiffractionObject`` automatically populates the ``xarray`` onto ``q``, ``tth``, and ``d``-spacing.
   If you want to access your diffraction data in a specific spacing, you can do this: ::

    q = do.on_xtype("q")
    tth = do.on_xtype("tth")
    d = do.on_xtype("d")

   This will return the ``xarray`` and ``yarray`` as a list of two 1D arrays, based on the specified ``xtype``.

3) Once the ``DiffractionObject`` is created, you can use ``get_array_index`` to get the index of the closest value
   in the ``xarray`` to a specified value.
   This is useful for alignment or comparison tasks.
   For example, assume you have created a ``DiffractionObject`` called ``do``,
   and you want to find the closest index of ``tth=80``, you can type the following: ::

    index = do.get_array_index(80, xtype="tth")

   If you do not specify an ``xtype``, it will default to the ``xtype`` used when creating the ``DiffractionObject``.
   For example, if you have created a ``DiffractionObject`` called ``do`` with ``xtype="q"``,
   you can find its closest index for ``q=0.25`` by typing either of the following: ::

    index = do.get_array_index(0.25) # no input xtype, defaults to q
    index = do.get_array_index(0.25, xtype="q")

4) You can compare diffraction objects too.
   For example, you can use the ``scale_to`` function to rescale one diffraction object to align its intensity values
   with a second diffraction object at a (closest) specified value on a specified ``xarray``.
   This makes it easier for visualizing and comparing two intensity curves on the same plot.
   For example, to scale ``do1`` to match ``do2`` at ``tth=60``: ::

    # Create Diffraction Objects do1 and do2
    do1 = DiffractionObject(
        xarray=np.array([10, 15, 25, 30, 60, 140]),
        yarray=np.array([10, 20, 25, 30, 60, 100]),
        xtype="tth",
        wavelength=2*np.pi
    )
    do2 = DiffractionObject(
        xarray=np.array([10, 20, 25, 30, 60, 140]),
        yarray=np.array([2, 3, 4, 5, 6, 7]),
        xtype="tth",
        wavelength=2*np.pi
    )
    do1_scaled = do1.scale_to(do2, tth=60)

   Here, the scaling factor is computed at ``tth=60``, aligning the intensity values.
   ``do1_scaled`` will have the intensity array ``np.array([1, 2, 2.5, 3, 6, 10])``.
   You can also scale based on other axes (e.g., ``q=0.2``): ::

    do1_scaled = do1.scale_to(do2, q=0.2)

   The function finds the closest indices for ``q=0.2`` and scales the ``yarray`` accordingly.

   Additionally, you can apply an ``offset`` to the scaled ``yarray``. For example: ::

    do1_scaled = do1.scale_to(do2, tth=60, offset=2) # add 2 to the scaled yarray
    do1_scaled = do1.scale_to(do2, tth=60, offset=-2) # subtract 2 from the scaled yarray

   This allows you to shift the scaled data for easier comparison.

5) You can create a copy of a diffraction object using the ``copy`` function,
   when you want to preserve the original data while working with a modified version. ::

    # Create a copy of Diffraction Object do
    do_copy = do.copy()

6) The ``dump`` function saves the diffraction data and relevant information to a specified file.
   You can choose one of the data axis (``q``, ``tth``, or ``d``) to export, with ``q`` as the default. ::

    # Assume you have created a Diffraction Object do
    file = "diffraction_data.xy"
    do.dump(file, xtype="q")

   In the saved file "diffraction_data.xy",
   the relevant information (name, scattering quantity, metadata, etc.) is included in the header.
   Your analysis time and software version are automatically recorded as well.
   The diffraction data is saved as two columns: the ``q`` values and corresponding intensity values.
   This ensures your diffraction data, along with all other information,
   is properly documented and saved for future reference.
