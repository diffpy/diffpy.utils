import datetime
import uuid
import warnings
from copy import deepcopy

import numpy as np

from diffpy.utils.tools import get_package_info
from diffpy.utils.transforms import (
    d_to_q,
    d_to_tth,
    q_to_d,
    q_to_tth,
    tth_to_d,
    tth_to_q,
)

QQUANTITIES = ["q"]
ANGLEQUANTITIES = ["angle", "tth", "twotheta", "2theta"]
DQUANTITIES = ["d", "dspace"]
XQUANTITIES = ANGLEQUANTITIES + DQUANTITIES + QQUANTITIES
XUNITS = [
    "degrees",
    "radians",
    "rad",
    "deg",
    "inv_angs",
    "inv_nm",
    "nm-1",
    "A-1",
]

x_values_not_equal_emsg = (
    "The two objects have different values in x arrays "
    "(my_do.all_arrays[:, [1, 2, 3]]). "
    "Please ensure the x values of the two objects are identical by "
    "re-instantiating the DiffractionObject with the correct x value inputs."
)

invalid_add_type_emsg = (
    "You may only add a DiffractionObject with another DiffractionObject or "
    "a scalar value. "
    "Please rerun by adding another DiffractionObject instance or a "
    "scalar value. e.g., my_do_1 + my_do_2 or my_do + 10 or 10 + my_do"
)


def _xtype_wmsg(xtype):
    return (
        f"I don't know how to handle the xtype, '{xtype}'. "
        f"Please rerun specifying an xtype from {*XQUANTITIES, }"
    )


def _setter_wmsg(attribute):
    return (
        f"Direct modification of attribute '{attribute}' is not allowed. "
        f"Please use 'input_data' to modify '{attribute}'.",
    )


class DiffractionObject:
    """Class for storing and manipulating diffraction data.

    DiffractionObject stores data produced from X-ray, neutron,
    and electron scattering experiments. The object can transform
    between different scattering quantities such as q (scattering vector),
    2θ (two-theta angle), and d (interplanar spacing), and perform various
    operations like scaling, addition, subtraction, and comparison for equality
    between diffraction objects.

    Attributes
    ----------
    scat_quantity : str
        The type of scattering experiment (e.g., "x-ray", "neutron"). Default
        is an empty string "".
    wavelength : float
        The wavelength of the incoming beam, specified in angstroms (Å).
        Default is none.
    name: str
        The name or label for the scattering data. Default is an empty string
        "".
    qmin : float
        The minimum q value.
    qmax : float
        The maximum q value.
    tthmin : float
        The minimum two-theta value.
    tthmax : float
        The maximum two-theta value.
    dmin : float
        The minimum d-spacing value.
    dmax : float
        The maximum d-spacing value.
    """

    def __init__(
        self,
        xarray,
        yarray,
        xtype,
        wavelength=None,
        scat_quantity="",
        name="",
        metadata={},
    ):
        """Initialize a DiffractionObject instance.

        Parameters
        ----------
        xarray : ndarray
            The independent variable array containing "q", "tth", or "d" values.
        yarray : ndarray
            The dependent variable array corresponding to intensity values.
        xtype : str
            The type of the independent variable in `xarray`. Must be one of
            {*XQUANTITIES}.
        wavelength : float, optional, default is None.
            The wavelength of the incoming beam, specified in angstroms (Å)
        scat_quantity : str, optional, default is an empty string "".
            The type of scattering experiment (e.g., "x-ray", "neutron").
        name : str, optional, default is an empty string "".
            The name or label for the scattering data.
        metadata : dict, optional, default is an empty dictionary {}
            The additional metadata associated with the diffraction object.

        Examples
        --------
        Create a DiffractionObject for X-ray scattering data:
        >>> import numpy as np
        >>> from diffpy.utils.diffraction_objects import DiffractionObject
        ...
        >>> x = np.array([0.12, 0.24, 0.31, 0.4])  # independent variable (e.g., q)  # noqa: E501
        >>> y = np.array([10, 20, 40, 60])  # intensity values
        >>> metadata = {
        ...     "sample": "rock salt from the beach",
        ...     "composition": "NaCl",
        ...     "temperature": "300 K,",
        ...     "experimenters": "Phill, Sally"
        ... }
        >>> do = DiffractionObject(
        ...     xarray=x,
        ...     yarray=y,
        ...     xtype="q",
        ...     wavelength=1.54,
        ...     scat_quantity="x-ray",
        ...     name="beach_rock_salt_1",
        ...     metadata=metadata
        ... )
        >>> print(do.metadata)
        """

        self._uuid = uuid.uuid4()
        self._input_data(
            xarray, yarray, xtype, wavelength, scat_quantity, name, metadata
        )

    def _input_data(
        self, xarray, yarray, xtype, wavelength, scat_quantity, name, metadata
    ):
        if xtype not in XQUANTITIES:
            raise ValueError(_xtype_wmsg(xtype))
        if len(xarray) != len(yarray):
            raise ValueError(
                "'xarray' and 'yarray' are different lengths.  They must "
                "correspond to each other and have the same length. "
                "Please re-initialize 'DiffractionObject'"
                "with valid 'xarray' and 'yarray's"
            )
        self.scat_quantity = scat_quantity
        self.wavelength = wavelength
        self.metadata = metadata
        self.name = name
        self._input_xtype = xtype
        self._set_arrays(xarray, yarray, xtype)
        self._set_min_max_xarray()

    def __eq__(self, other):
        if not isinstance(other, DiffractionObject):
            return NotImplemented
        self_attributes = [
            key for key in self.__dict__ if not key.startswith("_")
        ]
        other_attributes = [
            key for key in other.__dict__ if not key.startswith("_")
        ]
        if not sorted(self_attributes) == sorted(other_attributes):
            return False
        for key in self_attributes:
            value = getattr(self, key)
            other_value = getattr(other, key)
            if isinstance(value, float):
                if (
                    not (value is None and other_value is None)
                    and (value is None)
                    or (other_value is None)
                    or not np.isclose(value, other_value, rtol=1e-5)
                ):
                    return False
            elif isinstance(value, list) and all(
                isinstance(i, np.ndarray) for i in value
            ):
                if not all(
                    np.allclose(i, j, rtol=1e-5)
                    for i, j in zip(value, other_value)
                ):
                    return False
            else:
                if value != other_value:
                    return False
        return True

    def __add__(self, other):
        """Add a scalar value or another DiffractionObject to the yarray of the
        DiffractionObject.

        Parameters
        ----------
        other : DiffractionObject, int, or float
            The item to be added. If `other` is a scalar value, this value
            will be added to each element of the yarray of this
            DiffractionObject instance. If `other` is another DiffractionObject
            , the yarrays of the two DiffractionObjects will be combined
            element -wise. The result is a new DiffractionObject instance,
            representing the addition and using the xarray from the left-hand
            side DiffractionObject.

        Returns
        -------
        DiffractionObject
            The new DiffractionObject instance with modified yarray values.
            This instance is a deep copy of the original with the additions
            applied.

        Raises
        ------
        ValueError
            Raised when the xarrays of two DiffractionObject instances are
            not equal.
        TypeError
            Raised when `other` is not an instance of DiffractionObject, int,
            or float.

        Examples
        --------
        Add a scalar value to the yarray of a DiffractionObject instance:
        >>> new_do = my_do + 10.1
        >>> new_do = 10.1 + my_do

        Combine the yarrays of two DiffractionObject instances:
        >>> new_do = my_do_1 + my_do_2
        """

        self._check_operation_compatibility(other)
        summed_do = deepcopy(self)
        if isinstance(other, (int, float)):
            summed_do._all_arrays[:, 0] += other
        if isinstance(other, DiffractionObject):
            summed_do._all_arrays[:, 0] += other.all_arrays[:, 0]
        return summed_do

    __radd__ = __add__

    def __sub__(self, other):
        """Subtract scalar value or another DiffractionObject to the yarray of
        the DiffractionObject.

        This method behaves similarly to the `__add__` method, but performs
        subtraction instead of addition. For details on parameters, returns
        , and exceptions, refer to the documentation for `__add__`.

        Examples
        --------
        Subtract a scalar value from the yarray of a DiffractionObject
        instance:
        >>> new_do = my_do - 10.1

        Subtract the yarrays of two DiffractionObject instances:
        >>> new_do = my_do_1 - my_do_2
        """

        self._check_operation_compatibility(other)
        subtracted_do = deepcopy(self)
        if isinstance(other, (int, float)):
            subtracted_do._all_arrays[:, 0] -= other
        if isinstance(other, DiffractionObject):
            subtracted_do._all_arrays[:, 0] -= other.all_arrays[:, 0]
        return subtracted_do

    __rsub__ = __sub__

    def __mul__(self, other):
        """Multiply a scalar value or another DiffractionObject with the yarray
        of this DiffractionObject.

        This method behaves similarly to the `__add__` method, but performs
        multiplication instead of addition. For details on parameters,
        returns, and exceptions, refer to the documentation for `__add__`.

        Examples
        --------
        Multiply a scalar value with the yarray of a DiffractionObject
        instance:
        >>> new_do = my_do * 3.5

        Multiply the yarrays of two DiffractionObject instances:
        >>> new_do = my_do_1 * my_do_2
        """

        self._check_operation_compatibility(other)
        multiplied_do = deepcopy(self)
        if isinstance(other, (int, float)):
            multiplied_do._all_arrays[:, 0] *= other
        if isinstance(other, DiffractionObject):
            multiplied_do._all_arrays[:, 0] *= other.all_arrays[:, 0]
        return multiplied_do

    __rmul__ = __mul__

    def __truediv__(self, other):
        """Divide the yarray of this DiffractionObject by a scalar value or
        another DiffractionObject.

        This method behaves similarly to the `__add__` method, but performs
        division instead of addition. For details on parameters, returns,
        and exceptions, refer to the documentation for `__add__`.

        Examples
        --------
        Divide the yarray of a DiffractionObject instance by a scalar value:
        >>> new_do = my_do / 2.0

        Divide the yarrays of two DiffractionObject instances:
        >>> new_do = my_do_1 / my_do_2
        """
        self._check_operation_compatibility(other)
        divided_do = deepcopy(self)
        if isinstance(other, (int, float)):
            divided_do._all_arrays[:, 0] /= other
        if isinstance(other, DiffractionObject):
            divided_do._all_arrays[:, 0] /= other.all_arrays[:, 0]
        return divided_do

    __rtruediv__ = __truediv__

    def _check_operation_compatibility(self, other):
        if not isinstance(other, (DiffractionObject, int, float)):
            raise TypeError(invalid_add_type_emsg)
        if isinstance(other, DiffractionObject):
            if self.all_arrays.shape != other.all_arrays.shape:
                raise ValueError(x_values_not_equal_emsg)
            if not np.allclose(
                self.all_arrays[:, [1, 2, 3]], other.all_arrays[:, [1, 2, 3]]
            ):
                raise ValueError(x_values_not_equal_emsg)

    @property
    def all_arrays(self):
        """The 2D array containing `xarray` and `yarray` values.

        Returns
        -------
        ndarray
            The shape (len(data), 4) 2D array with columns containing the `
            yarray` (intensity) and the `xarray` values in q, tth, and d.

        Examples
        --------
        To access specific arrays individually, use these slices:

        >>> my_do.all_arrays[:, 0]  # yarray
        >>> my_do.all_arrays[:, 1]  # xarray in q
        >>> my_do.all_arrays[:, 2]  # xarray in tth
        >>> my_do.all_arrays[:, 3]  # xarray in d
        """
        return self._all_arrays

    @all_arrays.setter
    def all_arrays(self, _):
        raise AttributeError(_setter_wmsg("all_arrays"))

    @property
    def input_xtype(self):
        """The type of the independent variable in `xarray`.

        Returns
        -------
        input_xtype : str
            The type of `xarray`, which must be one of {*XQUANTITIES}.
        """
        return self._input_xtype

    @input_xtype.setter
    def input_xtype(self, _):
        raise AttributeError(_setter_wmsg("input_xtype"))

    @property
    def uuid(self):
        """The unique identifier for the DiffractionObject instance.

        Returns
        -------
        uuid : UUID
            The unique identifier of the DiffractionObject instance.
        """
        return self._uuid

    @uuid.setter
    def uuid(self, _):
        raise AttributeError(_setter_wmsg("uuid"))

    def get_array_index(self, xtype, xvalue):
        """Return the index of the closest value in the array associated with
        the specified xtype and the value provided.

        Parameters
        ----------
        xtype : str
            The type of the independent variable in `xarray`. Must be one
            of {*XQUANTITIES}.
        xvalue : float
            The value of the xtype to find the closest index for.

        Returns
        -------
        index : int
            The index of the closest value in the array associated with the
            specified xtype and the value provided.
        """

        xtype = self._input_xtype
        xarray = self.on_xtype(xtype)[0]
        if len(xarray) == 0:
            raise ValueError(
                f"The '{xtype}' array is empty. "
                "Please ensure it is initialized."
            )
        index = (np.abs(xarray - xvalue)).argmin()
        return index

    def _set_arrays(self, xarray, yarray, xtype):
        self._all_arrays = np.empty(shape=(len(xarray), 4))
        self._all_arrays[:, 0] = yarray
        if xtype.lower() in QQUANTITIES:
            self._all_arrays[:, 1] = xarray
            self._all_arrays[:, 2] = q_to_tth(xarray, self.wavelength)
            self._all_arrays[:, 3] = q_to_d(xarray)
        elif xtype.lower() in ANGLEQUANTITIES:
            self._all_arrays[:, 2] = xarray
            self._all_arrays[:, 1] = tth_to_q(xarray, self.wavelength)
            self._all_arrays[:, 3] = tth_to_d(xarray, self.wavelength)
        elif xtype.lower() in DQUANTITIES:
            self._all_arrays[:, 3] = xarray
            self._all_arrays[:, 1] = d_to_q(xarray)
            self._all_arrays[:, 2] = d_to_tth(xarray, self.wavelength)

    def _set_min_max_xarray(self):
        self.qmin = np.nanmin(self._all_arrays[:, 1], initial=np.inf)
        self.qmax = np.nanmax(self._all_arrays[:, 1], initial=0.0)
        self.tthmin = np.nanmin(self._all_arrays[:, 2], initial=np.inf)
        self.tthmax = np.nanmax(self._all_arrays[:, 2], initial=0.0)
        self.dmin = np.nanmin(self._all_arrays[:, 3], initial=np.inf)
        self.dmax = np.nanmax(self._all_arrays[:, 3], initial=0.0)

    def _get_original_array(self):
        if self._input_xtype in QQUANTITIES:
            return self.on_q(), "q"
        elif self._input_xtype in ANGLEQUANTITIES:
            return self.on_tth(), "tth"
        elif self._input_xtype in DQUANTITIES:
            return self.on_d(), "d"

    def on_q(self):
        """Return the tuple of two 1D numpy arrays containing q and y data.

        Returns
        -------
        (q-array, y-array) : tuple of ndarray
            The tuple containing two 1D numpy arrays with q and y data
        """
        return [self.all_arrays[:, 1], self.all_arrays[:, 0]]

    def on_tth(self):
        """Return the tuple of two 1D numpy arrays containing tth and y data.

        Returns
        -------
        (tth-array, y-array) : tuple of ndarray
            The tuple containing two 1D numpy arrays with tth and y data
        """
        return [self.all_arrays[:, 2], self.all_arrays[:, 0]]

    def on_d(self):
        """Return the tuple of two 1D numpy arrays containing d and y data.

        Returns
        -------
        (d-array, y-array) : tuple of ndarray
            The tuple containing two 1D numpy arrays with d and y data
        """
        return [self.all_arrays[:, 3], self.all_arrays[:, 0]]

    def scale_to(
        self, target_diff_object, q=None, tth=None, d=None, offset=None
    ):
        """Return a new diffraction object which is the current object but
        rescaled in y to the target.

        By default, if `q`, `tth`, or `d` are not provided, scaling is
        based on the max intensity from each object. Otherwise, y-value in
        the target at the closest specified x-value will be used as the
        factor to scale to. The entire array is scaled by this factor so
        that one object places on top of the other at that point. If
        multiple values of `q`, `tth`, or `d` are provided, an error will
        be raised.

        Parameters
        ----------
        target_diff_object: DiffractionObject
            The diffraction object you want to scale the current one onto.

        q, tth, d : float, optional, default is None
            The value of the x-array where you want the curves to line up
            vertically. Specify a value on one of the allowed grids, q, tth,
            or d), e.g., q=10.

        offset : float, optional, default is None
            The offset to add to the scaled y-values.

        Returns
        -------
        scaled_do : DiffractionObject
            The rescaled DiffractionObject as a new object.
        """
        if offset is None:
            offset = 0
        scaled_do = self.copy()
        count = sum([q is not None, tth is not None, d is not None])
        if count > 1:
            raise ValueError(
                "You must specify none or exactly one of 'q', 'tth', or 'd'. "
                "Please provide either none or one value."
            )

        if count == 0:
            q_target_max = max(target_diff_object.on_q()[1])
            q_self_max = max(self.on_q()[1])
            scaled_do._all_arrays[:, 0] = (
                scaled_do._all_arrays[:, 0] * q_target_max / q_self_max
                + offset
            )
            return scaled_do

        xtype = "q" if q is not None else "tth" if tth is not None else "d"
        data = self.on_xtype(xtype)
        target = target_diff_object.on_xtype(xtype)

        xvalue = q if xtype == "q" else tth if xtype == "tth" else d

        xindex_data = (np.abs(data[0] - xvalue)).argmin()
        xindex_target = (np.abs(target[0] - xvalue)).argmin()
        scaled_do._all_arrays[:, 0] = (
            data[1] * target[1][xindex_target] / data[1][xindex_data] + offset
        )
        return scaled_do

    def on_xtype(self, xtype):
        """Return a tuple of two 1D numpy arrays containing x and y data.

        Parameters
        ----------
        xtype : str
            The type of quantity for the independent variable chosen from
            {*XQUANTITIES, }

        Raises
        ------
        ValueError
            Raised when the specified xtype is not among {*XQUANTITIES, }

        Returns
        -------
        (xarray, yarray) : tuple of ndarray
            The tuple containing two 1D numpy arrays with x and y data for
            the specified xtype.
        """
        if xtype.lower() in ANGLEQUANTITIES:
            return self.on_tth()
        elif xtype.lower() in QQUANTITIES:
            return self.on_q()
        elif xtype.lower() in DQUANTITIES:
            return self.on_d()
        else:
            raise ValueError(_xtype_wmsg(xtype))

    def dump(self, filepath, xtype=None):
        """Dump the xarray and yarray of the diffraction object to a two-column
        file, with the associated information included in the header.

        Parameters
        ----------
        filepath : str
            The filepath where the diffraction object will be dumped
        xtype : str, optional, default is q
            The type of quantity for the independent variable chosen from
            {*XQUANTITIES, }

        Examples
        --------
        To save a diffraction object to a file named "diffraction_data.chi"
        in the current directory with the independent variable 'q':

        >>> file = "diffraction_data.chi"
        >>> do.dump(file, xtype="q")

        To save the diffraction data to a file in a subfolder `output`:

        >>> file = "./output/diffraction_data.chi"
        >>> do.dump(file, xtype="q")

        To save the diffraction data with a different independent variable,
        such as 'tth':

        >>> file = "diffraction_data_tth.chi"
        >>> do.dump(file, xtype="tth")
        """
        if xtype is None:
            xtype = "q"
        if xtype in QQUANTITIES:
            data_to_save = np.column_stack((self.on_q()[0], self.on_q()[1]))
        elif xtype in ANGLEQUANTITIES:
            data_to_save = np.column_stack(
                (self.on_tth()[0], self.on_tth()[1])
            )
        elif xtype in DQUANTITIES:
            data_to_save = np.column_stack((self.on_d()[0], self.on_d()[1]))
        else:
            warnings.warn(_xtype_wmsg(xtype))
        self.metadata.update(
            get_package_info("diffpy.utils", metadata=self.metadata)
        )
        self.metadata["creation_time"] = datetime.datetime.now()

        with open(filepath, "w") as f:
            f.write(
                f"[DiffractionObject]\n"
                f"name = {self.name}\n"
                f"wavelength = {self.wavelength}\n"
                f"scat_quantity = {self.scat_quantity}\n"
            )
            for key, value in self.metadata.items():
                f.write(f"{key} = {value}\n")
            f.write("\n#### start data\n")
            np.savetxt(f, data_to_save, delimiter=" ")

    def copy(self):
        """Create a deep copy of the DiffractionObject instance.

        Returns
        -------
        DiffractionObject
            The new instance of DiffractionObject, which is a deep copy of
            the current instance.
        """
        return deepcopy(self)
