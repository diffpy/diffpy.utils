import datetime
import uuid
import warnings
from copy import deepcopy

import numpy as np

from diffpy.utils.tools import get_package_info
from diffpy.utils.transforms import d_to_q, d_to_tth, q_to_d, q_to_tth, tth_to_d, tth_to_q

QQUANTITIES = ["q"]
ANGLEQUANTITIES = ["angle", "tth", "twotheta", "2theta"]
DQUANTITIES = ["d", "dspace"]
XQUANTITIES = ANGLEQUANTITIES + DQUANTITIES + QQUANTITIES
XUNITS = ["degrees", "radians", "rad", "deg", "inv_angs", "inv_nm", "nm-1", "A-1"]

x_grid_emsg = (
    "objects are not on the same x-grid. You may add them using the self.add method "
    "and specifying how to handle the mismatch."
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
    """
    Initialize a DiffractionObject instance.

    Parameters
    ----------
    xarray : array-like
        The independent variable array containing "q", "tth", or "d" values.
    yarray : array-like
        The dependent variable array corresponding to intensity values.
    xtype : str
        The type of the independent variable in `xarray`. Must be one of {*XQUANTITIES}.
    wavelength : float, optional
        The wavelength of the incoming beam, specified in angstroms (Å). Default is none.
    scat_quantity : str, optional
        The type of scattering experiment (e.g., "x-ray", "neutron"). Default is an empty string "".
    name : str, optional
        The name or label for the scattering data. Default is an empty string "".
    metadata : dict, optional
        The additional metadata associated with the diffraction object. Default is {}.

    Examples
    --------
    Create a DiffractionObject for X-ray scattering data:

    >>> import numpy as np
    >>> from diffpy.utils.diffraction_objects import DiffractionObject
    ...
    >>> x = np.array([0.12, 0.24, 0.31, 0.4])  # independent variable (e.g., q)
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
    ...     metadata=metadata
    ... )
    >>> print(do.metadata)
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

        self._id = uuid.uuid4()
        self._input_data(xarray, yarray, xtype, wavelength, scat_quantity, name, metadata)

    def _input_data(self, xarray, yarray, xtype, wavelength, scat_quantity, name, metadata):
        if xtype not in XQUANTITIES:
            raise ValueError(_xtype_wmsg(xtype))
        # Check xarray and yarray have the same length
        if len(xarray) != len(yarray):
            raise ValueError(
                "'xarray' and 'yarray' must have the same length. "
                "Please re-initialize 'DiffractionObject' or re-run the method 'input_data' "
                "with 'xarray' and 'yarray' of identical length."
            )
        self.scat_quantity = scat_quantity
        self.wavelength = wavelength
        self.metadata = metadata
        self.name = name
        self._input_xtype = xtype
        self._set_arrays(xarray, xtype, yarray)
        self._set_min_max_xarray()

    def __eq__(self, other):
        if not isinstance(other, DiffractionObject):
            return NotImplemented
        self_attributes = [key for key in self.__dict__ if not key.startswith("_")]
        other_attributes = [key for key in other.__dict__ if not key.startswith("_")]
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
            elif isinstance(value, list) and all(isinstance(i, np.ndarray) for i in value):
                if not all(np.allclose(i, j, rtol=1e-5) for i, j in zip(value, other_value)):
                    return False
            else:
                if value != other_value:
                    return False
        return True

    def __add__(self, other):
        summed = deepcopy(self)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, np.ndarray):
            summed.on_tth[1] = self.on_tth[1] + other
            summed.on_q[1] = self.on_q[1] + other
        elif not isinstance(other, DiffractionObject):
            raise TypeError("I only know how to sum two DiffractionObject objects")
        elif self.on_tth[0].all() != other.on_tth[0].all():
            raise RuntimeError(x_grid_emsg)
        else:
            summed.on_tth[1] = self.on_tth[1] + other.on_tth[1]
            summed.on_q[1] = self.on_q[1] + other.on_q[1]
        return summed

    def __radd__(self, other):
        summed = deepcopy(self)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, np.ndarray):
            summed.on_tth[1] = self.on_tth[1] + other
            summed.on_q[1] = self.on_q[1] + other
        elif not isinstance(other, DiffractionObject):
            raise TypeError("I only know how to sum two Scattering_object objects")
        elif self.on_tth[0].all() != other.on_tth[0].all():
            raise RuntimeError(x_grid_emsg)
        else:
            summed.on_tth[1] = self.on_tth[1] + other.on_tth[1]
            summed.on_q[1] = self.on_q[1] + other.on_q[1]
        return summed

    def __sub__(self, other):
        subtracted = deepcopy(self)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, np.ndarray):
            subtracted.on_tth[1] = self.on_tth[1] - other
            subtracted.on_q[1] = self.on_q[1] - other
        elif not isinstance(other, DiffractionObject):
            raise TypeError("I only know how to subtract two Scattering_object objects")
        elif self.on_tth[0].all() != other.on_tth[0].all():
            raise RuntimeError(x_grid_emsg)
        else:
            subtracted.on_tth[1] = self.on_tth[1] - other.on_tth[1]
            subtracted.on_q[1] = self.on_q[1] - other.on_q[1]
        return subtracted

    def __rsub__(self, other):
        subtracted = deepcopy(self)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, np.ndarray):
            subtracted.on_tth[1] = other - self.on_tth[1]
            subtracted.on_q[1] = other - self.on_q[1]
        elif not isinstance(other, DiffractionObject):
            raise TypeError("I only know how to subtract two Scattering_object objects")
        elif self.on_tth[0].all() != other.on_tth[0].all():
            raise RuntimeError(x_grid_emsg)
        else:
            subtracted.on_tth[1] = other.on_tth[1] - self.on_tth[1]
            subtracted.on_q[1] = other.on_q[1] - self.on_q[1]
        return subtracted

    def __mul__(self, other):
        multiplied = deepcopy(self)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, np.ndarray):
            multiplied.on_tth[1] = other * self.on_tth[1]
            multiplied.on_q[1] = other * self.on_q[1]
        elif not isinstance(other, DiffractionObject):
            raise TypeError("I only know how to multiply two Scattering_object objects")
        elif self.on_tth[0].all() != other.on_tth[0].all():
            raise RuntimeError(x_grid_emsg)
        else:
            multiplied.on_tth[1] = self.on_tth[1] * other.on_tth[1]
            multiplied.on_q[1] = self.on_q[1] * other.on_q[1]
        return multiplied

    def __rmul__(self, other):
        multiplied = deepcopy(self)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, np.ndarray):
            multiplied.on_tth[1] = other * self.on_tth[1]
            multiplied.on_q[1] = other * self.on_q[1]
        elif self.on_tth[0].all() != other.on_tth[0].all():
            raise RuntimeError(x_grid_emsg)
        else:
            multiplied.on_tth[1] = self.on_tth[1] * other.on_tth[1]
            multiplied.on_q[1] = self.on_q[1] * other.on_q[1]
        return multiplied

    def __truediv__(self, other):
        divided = deepcopy(self)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, np.ndarray):
            divided.on_tth[1] = other / self.on_tth[1]
            divided.on_q[1] = other / self.on_q[1]
        elif not isinstance(other, DiffractionObject):
            raise TypeError("I only know how to multiply two Scattering_object objects")
        elif self.on_tth[0].all() != other.on_tth[0].all():
            raise RuntimeError(x_grid_emsg)
        else:
            divided.on_tth[1] = self.on_tth[1] / other.on_tth[1]
            divided.on_q[1] = self.on_q[1] / other.on_q[1]
        return divided

    def __rtruediv__(self, other):
        divided = deepcopy(self)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, np.ndarray):
            divided.on_tth[1] = other / self.on_tth[1]
            divided.on_q[1] = other / self.on_q[1]
        elif self.on_tth[0].all() != other.on_tth[0].all():
            raise RuntimeError(x_grid_emsg)
        else:
            divided.on_tth[1] = other.on_tth[1] / self.on_tth[1]
            divided.on_q[1] = other.on_q[1] / self.on_q[1]
        return divided

    @property
    def all_arrays(self):
        return self._all_arrays

    @all_arrays.setter
    def all_arrays(self, _):
        raise AttributeError(_setter_wmsg("all_arrays"))

    @property
    def input_xtype(self):
        return self._input_xtype

    @input_xtype.setter
    def input_xtype(self, _):
        raise AttributeError(_setter_wmsg("input_xtype"))

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _):
        raise AttributeError(_setter_wmsg("id"))

    def get_array_index(self, value, xtype=None):
        """
        Return the index of the closest value in the array associated with the specified xtype.

        Parameters
        ----------
        xtype str
            the xtype used to access the array
        value float
            the target value to search for

        Returns
        -------
        the index of the value in the array
        """

        xtype = self._input_xtype
        array = self.on_xtype(xtype)[0]
        if len(array) == 0:
            raise ValueError(f"The '{xtype}' array is empty. Please ensure it is initialized.")
        i = (np.abs(array - value)).argmin()
        return i

    def _set_arrays(self, xarray, xtype, yarray):
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
        return [self.all_arrays[:, 1], self.all_arrays[:, 0]]

    def on_tth(self):
        return [self.all_arrays[:, 2], self.all_arrays[:, 0]]

    def on_d(self):
        return [self.all_arrays[:, 3], self.all_arrays[:, 0]]

    def scale_to(self, target_diff_object, q=None, tth=None, d=None, offset=0):
        """
        returns a new diffraction object which is the current object but rescaled in y to the target

        The y-value in the target at the closest specified x-value will be used as the factor to scale to.
        The entire array is scaled by this factor so that one object places on top of the other at that point.
        If multiple values of `q`, `tth`, or `d` are provided, or none are provided, an error will be raised.

        Parameters
        ----------
        target_diff_object: DiffractionObject
            the diffraction object you want to scale the current one onto

        q, tth, d : float, optional, must specify exactly one of them
            The value of the x-array where you want the curves to line up vertically.
            Specify a value on one of the allowed grids, q, tth, or d), e.g., q=10.

        offset : float, optional, default is 0
            an offset to add to the scaled y-values

        Returns
        -------
        the rescaled DiffractionObject as a new object
        """
        scaled = self.copy()
        count = sum([q is not None, tth is not None, d is not None])
        if count != 1:
            raise ValueError(
                "You must specify exactly one of 'q', 'tth', or 'd'. Please rerun specifying only one."
            )

        xtype = "q" if q is not None else "tth" if tth is not None else "d"
        data = self.on_xtype(xtype)
        target = target_diff_object.on_xtype(xtype)

        xvalue = q if xtype == "q" else tth if xtype == "tth" else d

        xindex_data = (np.abs(data[0] - xvalue)).argmin()
        xindex_target = (np.abs(target[0] - xvalue)).argmin()
        scaled._all_arrays[:, 0] = data[1] * target[1][xindex_target] / data[1][xindex_data] + offset
        return scaled

    def on_xtype(self, xtype):
        """
        Return a list of two 1D np array with x and y data, raise an error if the specified xtype is invalid

        Parameters
        ----------
        xtype str
            the type of quantity for the independent variable from {*XQUANTITIES, }

        Returns
        -------
        a list of two 1D np array with x and y data
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
        if xtype is None:
            xtype = "q"
        if xtype in QQUANTITIES:
            data_to_save = np.column_stack((self.on_q()[0], self.on_q()[1]))
        elif xtype in ANGLEQUANTITIES:
            data_to_save = np.column_stack((self.on_tth()[0], self.on_tth()[1]))
        elif xtype in DQUANTITIES:
            data_to_save = np.column_stack((self.on_d()[0], self.on_d()[1]))
        else:
            warnings.warn(_xtype_wmsg(xtype))
        self.metadata.update(get_package_info("diffpy.utils", metadata=self.metadata))
        self.metadata["creation_time"] = datetime.datetime.now()

        with open(filepath, "w") as f:
            f.write(
                f"[DiffractionObject]\nname = {self.name}\nwavelength = {self.wavelength}\n"
                f"scat_quantity = {self.scat_quantity}\n"
            )
            for key, value in self.metadata.items():
                f.write(f"{key} = {value}\n")
            f.write("\n#### start data\n")
            np.savetxt(f, data_to_save, delimiter=" ")

    def copy(self):
        """
        Create a deep copy of the DiffractionObject instance.

        Returns
        -------
        DiffractionObject
            A new instance of DiffractionObject, which is a deep copy of the current instance.
        """
        return deepcopy(self)
