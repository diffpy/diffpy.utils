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
    def __init__(
        self,
        xarray,
        yarray,
        xtype,
        wavelength,
        scat_quantity="",
        name="",
        metadata={},
    ):

        self._id = uuid.uuid4()
        self.input_data(xarray, yarray, xtype, wavelength, scat_quantity, name, metadata)

    def input_data(self, xarray, yarray, xtype, wavelength, scat_quantity="", name="", metadata={}):
        """
        Insert a new scattering quantity into the scattering object.

        Parameters
        ----------
        xarray : array-like
            The independent variable array (e.g., "q", "tth", or "d").
        yarray : array-like
            The dependent variable array corresponding to intensity values.
        xtype : str
            The type of the independent variable in `xarray`. Must be one of {*XQUANTITIES},
            such as "q", "tth", or "d".
        wavelength : float
            The wavelength of the incoming beam, specified in angstroms (Å).
        scat_quantity : str, optional
            The type of scattering experiment (e.g., "x-ray", "neutron"). Default is an empty string "".
        name : str, optional
            The name or label for the scattering data. Default is an empty string "".
        metadata : dict, optional
            The additional metadata associated with the diffraction object. Default is {}.

        Returns
        -------
        None
            This method updates the object in place and does not return a value.
        """

        # Check xtype is valid. An empty string is the default value.
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
        self._set_xarrays(xarray, xtype)
        self._all_arrays[:, 0] = yarray

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

    def set_angles_from_list(self, angles_list):
        self.angles = angles_list
        self.n_steps = len(angles_list) - 1.0
        self.begin_angle = self.angles[0]
        self.end_angle = self.angles[-1]

    def set_qs_from_range(self, begin_q, end_q, step_size=None, n_steps=None):
        """
        create an array of linear spaced Q-values

        Parameters
        ----------
        begin_q float
          the beginning angle
        end_q float
          the ending angle
        step_size float
          the size of the step between points.  Only specify step_size or n_steps, not both
        n_steps integer
          the number of steps.  Odd numbers are preferred. Only specify step_size or n_steps, not both

        Returns
        -------
        Sets self.qs
        self.qs array of floats
          the q values in the independent array

        """
        self.qs = self._set_array_from_range(begin_q, end_q, step_size=step_size, n_steps=n_steps)

    def set_angles_from_range(self, begin_angle, end_angle, step_size=None, n_steps=None):
        """
        create an array of linear spaced angle-values

        Parameters
        ----------
        begin_angle float
          the beginning angle
        end_angle float
          the ending angle
        step_size float
          the size of the step between points.  Only specify step_size or n_steps, not both
        n_steps integer
          the number of steps.  Odd numbers are preferred. Only specify step_size or n_steps, not both

        Returns
        -------
        Sets self.angles
        self.angles array of floats
          the q values in the independent array

        """
        self.angles = self._set_array_from_range(begin_angle, end_angle, step_size=step_size, n_steps=n_steps)

    def _set_array_from_range(self, begin, end, step_size=None, n_steps=None):
        if step_size is not None and n_steps is not None:
            print(
                "WARNING: both step_size and n_steps have been given.  n_steps will be used and step_size will be "
                "reset."
            )
            array = np.linspace(begin, end, n_steps)
        elif step_size is not None:
            array = np.arange(begin, end, step_size)
        elif n_steps is not None:
            array = np.linspace(begin, end, n_steps)
        return array

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

    def _set_xarrays(self, xarray, xtype):
        self._all_arrays = np.empty(shape=(len(xarray), 4))
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

    def scale_to(self, target_diff_object, xtype=None, xvalue=None):
        """
        Return a new diffraction object which is the current object but recaled in y to the target

        Parameters
        ----------
        target_diff_object: DiffractionObject
          the diffraction object you want to scale the current one on to
        xtype: string, optional.  Default is Q
          the xtype, from {XQUANTITIES}, that you will specify a point from to scale to
        xvalue: float. Default is the midpoint of the array
          the y-value in the target at this x-value will be used as the factor to scale to.
          The entire array is scaled be the factor that places on on top of the other at that point.
          xvalue does not have to be in the x-array, the point closest to this point will be used for the scaling.

        Returns
        -------
        the rescaled DiffractionObject as a new object

        """
        scaled = deepcopy(self)
        if xtype is None:
            xtype = "q"

        data = self.on_xtype(xtype)
        target = target_diff_object.on_xtype(xtype)
        if xvalue is None:
            xvalue = data[0][0] + (data[0][-1] - data[0][0]) / 2.0

        xindex = (np.abs(data[0] - xvalue)).argmin()
        ytarget = target[1][xindex]
        yself = data[1][xindex]
        scaled.on_tth[1] = data[1] * ytarget / yself
        scaled.on_q[1] = data[1] * ytarget / yself
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
