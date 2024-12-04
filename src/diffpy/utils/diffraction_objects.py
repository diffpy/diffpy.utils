import datetime
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
        f"WARNING: I don't know how to handle the xtype, '{xtype}'.  Please rerun specifying an "
        f"xtype from {*XQUANTITIES, }"
    )


class DiffractionObject:
    def __init__(
        self, name=None, wavelength=None, scat_quantity=None, metadata=None, xarray=None, yarray=None, xtype=None
    ):
        if name is None:
            name = ""
        self.name = name
        if metadata is None:
            metadata = {}
        self.metadata = metadata
        if xtype is None:
            xtype = ""
        self.scat_quantity = scat_quantity
        self.wavelength = wavelength

        if xarray is None:
            xarray = np.empty(0)
        if yarray is None:
            yarray = np.empty(0)
        self.insert_scattering_quantity(xarray, yarray, xtype)

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

    def get_angle_index(self, angle):
        count = 0
        for i, target in enumerate(self.angles):
            if angle == target:
                return i
            else:
                count += 1
        if count >= len(self.angles):
            raise IndexError(f"WARNING: no angle {angle} found in angles list")

    def _set_xarrays(self, xarray, xtype):
        self.all_arrays = np.empty(shape=(len(xarray), 4))
        if xtype.lower() in QQUANTITIES:
            self.all_arrays[:, 1] = xarray
            self.all_arrays[:, 2] = q_to_tth(xarray, self.wavelength)
            self.all_arrays[:, 3] = q_to_d(xarray)
        elif xtype.lower() in ANGLEQUANTITIES:
            self.all_arrays[:, 2] = xarray
            self.all_arrays[:, 1] = tth_to_q(xarray, self.wavelength)
            self.all_arrays[:, 3] = tth_to_d(xarray, self.wavelength)
        elif xtype.lower() in DQUANTITIES:
            self.all_arrays[:, 3] = xarray
            self.all_arrays[:, 1] = d_to_q(xarray)
            self.all_arrays[:, 2] = d_to_tth(xarray, self.wavelength)
        self.qmin = np.nanmin(self.all_arrays[:, 1], initial=np.inf)
        self.qmax = np.nanmax(self.all_arrays[:, 1], initial=0.0)
        self.tthmin = np.nanmin(self.all_arrays[:, 2], initial=np.inf)
        self.tthmax = np.nanmax(self.all_arrays[:, 2], initial=0.0)
        self.dmin = np.nanmin(self.all_arrays[:, 3], initial=np.inf)
        self.dmax = np.nanmax(self.all_arrays[:, 3], initial=0.0)

    def insert_scattering_quantity(
        self,
        xarray,
        yarray,
        xtype,
        metadata={},
        scat_quantity=None,
        name=None,
        wavelength=None,
    ):
        f"""
        insert a new scattering quantity into the scattering object

        Parameters
        ----------
        xarray array-like of floats
          the independent variable array
        yarray array-like of floats
          the dependent variable array
        xtype string
          the type of quantity for the independent variable from {*XQUANTITIES, }
        metadata, scat_quantity, name and wavelength are optional.  They have the same
        meaning as in the constructor. Values will only be overwritten if non-empty values are passed.

        Returns
        -------
        Nothing.  Updates the object in place.

        """
        self._set_xarrays(xarray, xtype)
        self.all_arrays[:, 0] = yarray
        self.input_xtype = xtype
        # only update these optional values if non-empty quantities are passed to avoid overwriting
        # valid data inadvertently
        if metadata:
            self.metadata = metadata
        if scat_quantity is not None:
            self.scat_quantity = scat_quantity
        if name is not None:
            self.name = name
        if wavelength is not None:
            self.wavelength = wavelength

    def _get_original_array(self):
        if self.input_xtype in QQUANTITIES:
            return self.on_q(), "q"
        elif self.input_xtype in ANGLEQUANTITIES:
            return self.on_tth(), "tth"
        elif self.input_xtype in DQUANTITIES:
            return self.on_d(), "d"

    def on_q(self):
        return [self.all_arrays[:, 1], self.all_arrays[:, 0]]

    def on_tth(self):
        return [self.all_arrays[:, 2], self.all_arrays[:, 0]]

    def on_d(self):
        return [self.all_arrays[:, 3], self.all_arrays[:, 0]]

    def scale_to(self, target_diff_object, xtype=None, xvalue=None):
        f"""
        returns a new diffraction object which is the current object but recaled in y to the target

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
        return a 2D np array with x in the first column and y in the second for x of type type

        Parameters
        ----------
        xtype

        Returns
        -------

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
