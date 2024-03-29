import uuid
from copy import deepcopy

import numpy as np
from numpy import array

QQUANTITIES = ["q"]
ANGLEQUANTITIES = ["angle","tth", "twotheta", "2theta"]
DQUANTITIES = ["d", "dspace"]
XQUANTITIES = ANGLEQUANTITIES + DQUANTITIES + QQUANTITIES
XUNITS = ["degrees","radians","rad","deg","inv_angs","inv_nm","nm-1","A-1"]

class Diffraction_object():
    def __init__(self, name='', wavelength=None):
        self.name = name
        self.wavelength = wavelength
        self.scat_quantity = ""
        self.on_q = [np.empty(1), np.empty(1)]
        self.on_tth = [np.empty(1), np.empty(1)]
        self.on_d = [np.empty(1), np.empty(1)]
        self._all_arrays = [self.on_q, self.on_tth]

    def __add__(self, other):
        summed = deepcopy(self)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, np.ndarray):
            summed.on_tth[1] = self.on_tth[1] + other
            summed.on_q[1] = self.on_q[1] + other
        elif not isinstance(other, Diffraction_object):
            raise TypeError(f"I only know how to sum two Diffraction_object objects")
        elif self.on_tth[0].all() != other.on_tth[0].all():
            raise RuntimeError(f"objects are not on the same x-grid. You may add them using the self.add method and"
                               f"specifying how to handle the mismatch.")
        else:
            summed.on_tth[1] = self.on_tth[1] + other.on_tth[1]
            summed.on_q[1] = self.on_q[1] + other.on_q[1]
        return summed
    def __radd__(self, other):
        summed = deepcopy(self)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, np.ndarray):
            summed.on_tth[1] = self.on_tth[1] + other
            summed.on_q[1] = self.on_q[1] + other
        elif not isinstance(other, Diffraction_object):
            raise TypeError(f"I only know how to sum two Scattering_object objects")
        elif self.on_tth[0].all() != other.on_tth[0].all():
            raise RuntimeError(f"objects are not on the same x-grid. You may add them using the self.add method and"
                               f"specifying how to handle the mismatch.")
        else:
            summed.on_tth[1] = self.on_tth[1] + other.on_tth[1]
            summed.on_q[1] = self.on_q[1] + other.on_q[1]
        return summed

    def __sub__(self, other):
        subtracted = deepcopy(self)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, np.ndarray):
            subtracted.on_tth[1] = self.on_tth[1] - other
            subtracted.on_q[1] = self.on_q[1] - other
        elif not isinstance(other, Diffraction_object):
            raise TypeError(f"I only know how to subtract two Scattering_object objects")
        elif self.on_tth[0].all() != other.on_tth[0].all():
            raise RuntimeError(
                f"objects are not on the same x-grid. You may subtract them using the self.add method and"
                f"specifying how to handle the mismatch.")
        else:
            subtracted.on_tth[1] = self.on_tth[1] - other.on_tth[1]
            subtracted.on_q[1] = self.on_q[1] - other.on_q[1]
        return subtracted

    def __rsub__(self, other):
        subtracted = deepcopy(self)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, np.ndarray):
            subtracted.on_tth[1] = other - self.on_tth[1]
            subtracted.on_q[1] = other - self.on_q[1]
        elif not isinstance(other, Diffraction_object):
            raise TypeError(f"I only know how to subtract two Scattering_object objects")
        elif self.on_tth[0].all() != other.on_tth[0].all():
            raise RuntimeError(
                f"objects are not on the same x-grid. You may subtract them using the self.add method and"
                f"specifying how to handle the mismatch.")
        else:
            subtracted.on_tth[1] =  other.on_tth[1] - self.on_tth[1]
            subtracted.on_q[1] = other.on_q[1] - self.on_q[1]
        return subtracted

    def __mul__(self, other):
        multiplied = deepcopy(self)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, np.ndarray):
            multiplied.on_tth[1] = other * self.on_tth[1]
            multiplied.on_q[1] = other * self.on_q[1]
        elif not isinstance(other, Diffraction_object):
            raise TypeError(f"I only know how to multiply two Scattering_object objects")
        elif self.on_tth[0].all() != other.on_tth[0].all():
            raise RuntimeError(
                f"objects are not on the same x-grid. You may multiply them using the self.add method and"
                f"specifying how to handle the mismatch.")
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
            raise RuntimeError(
                f"objects are not on the same x-grid. You may multiply them using the self.add method and"
                f"specifying how to handle the mismatch.")
        else:
            multiplied.on_tth[1] = self.on_tth[1] * other.on_tth[1]
            multiplied.on_q[1] = self.on_q[1] * other.on_q[1]
        return multiplied

    def __truediv__(self, other):
        divided = deepcopy(self)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, np.ndarray):
            divided.on_tth[1] = other / self.on_tth[1]
            divided.on_q[1] = other / self.on_q[1]
        elif not isinstance(other, Diffraction_object):
            raise TypeError(f"I only know how to multiply two Scattering_object objects")
        elif self.on_tth[0].all() != other.on_tth[0].all():
            raise RuntimeError(
                f"objects are not on the same x-grid. You may multiply them using the self.add method and"
                f"specifying how to handle the mismatch.")
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
            raise RuntimeError(
                f"Diffraction objects are not on the same x-grid. You may multiply them using the self.add method and"
                f"specifying how to handle the mismatch.")
        else:
            divided.on_tth[1] = other.on_tth[1] / self.on_tth[1]
            divided.on_q[1] = other.on_q[1] / self.on_q[1]
        return divided


    def set_angles_from_list(self, angles_list):
            self.angles = angles_list
            self.n_steps = len(angles_list) - 1.
            self.begin_angle = self.angles[0]
            self.end_angle = self.angles[-1]

    def set_qs_from_range(self, begin_q, end_q, step_size=None, n_steps=None):
        '''
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

        '''
        self.qs = self._set_array_from_range(begin_q, end_q, step_size=step_size, n_steps=n_steps)


    def set_angles_from_range(self, begin_angle, end_angle, step_size=None, n_steps=None):
        '''
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

        '''
        self.angles = self._set_array_from_range(begin_angle, end_angle, step_size=step_size, n_steps=n_steps)


    def _set_array_from_range(self, begin, end, step_size=None, n_steps=None):
        if step_size is not None and n_steps is not None:
            print(
                "WARNING: both step_size and n_steps have been given.  n_steps will be used and step_size will be "
                "reset.")
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

    def insert_scattering_quantity(self, xarray, yarray, xtype, metadata={}):
        f"""
        insert a new scattering quantity into the scattering object
        
        Parameters
        ----------
        xarray array-like of floats
          the independent variable array
        yarray array-like of floats
          the dependent variable array
        xtype string
          the type of quantity for the independent variable from {*XQUANTITIES,}
        metadata: dict
          the metadata in the form of a dictionary of user-supplied key:value pairs
        
        Returns
        -------

        """
        self.input_xtype = xtype
        self.metadata = metadata
        if xtype.lower() in QQUANTITIES:
            self.on_q = [np.array(xarray),np.array(yarray)]
        elif xtype.lower() in ANGLEQUANTITIES:
            self.on_tth = [np.array(xarray),np.array(yarray)]
        elif xtype.lower() in DQUANTITIES:
            self.on_tth = [np.array(xarray),np.array(yarray)]
        self.set_all_arrays()
    def q_to_tth(self):
        r"""
        Helper function to convert q to two-theta.

        By definition the relationship is:

        .. math::

            \sin\left(\frac{2\theta}{2}\right) = \frac{\lambda q}{4 \pi}

        thus

        .. math::

            2\theta_n = 2 \arcsin\left(\frac{\lambda q}{4 \pi}\right)

        Parameters
        ----------
        q : array
            An array of :math:`q` values

        wavelength : float
            Wavelength of the incoming x-rays

        Function adapted from scikit-beam.  Thanks to those developers

        Returns
        -------
        two_theta : array
            An array of :math:`2\theta` values in radians
        """
        q = self.on_q[0]
        q = np.asarray(q)
        wavelength = float(self.wavelength)
        pre_factor = wavelength / (4 * np.pi)
        return np.rad2deg(2 * np.arcsin(q * pre_factor))

    def tth_to_q(self):
        r"""
        Helper function to convert two-theta to q

        By definition the relationship is

        .. math::

            \sin\left(\frac{2\theta}{2}\right) = \frac{\lambda q}{4 \pi}

        thus

        .. math::

            q = \frac{4 \pi \sin\left(\frac{2\theta}{2}\right)}{\lambda}



        Parameters
        ----------
        two_theta : array
            An array of :math:`2\theta` values in units of degrees

        wavelength : float
            Wavelength of the incoming x-rays

        Function adapted from scikit-beam.  Thanks to those developers.

        Returns
        -------
        q : array
            An array of :math:`q` values in the inverse of the units
            of ``wavelength``
        """
        two_theta = np.asarray(np.deg2rad(self.on_tth[0]))
        wavelength = float(self.wavelength)
        pre_factor = (4 * np.pi) / wavelength
        return pre_factor * np.sin(two_theta / 2)

    def set_all_arrays(self):
        master_array, xtype = self._get_original_array()
        if xtype == "q":
            self.on_tth[0] = self.q_to_tth()
            self.on_tth[1] = master_array[1]
        if xtype == "tth":
            self.on_q[0] = self.tth_to_q()
            self.on_q[1] = master_array[1]
        self.tthmin = self.on_tth[0][0]
        self.tthmax = self.on_tth[0][-1]
        self.qmin = self.on_q[0][0]
        self.qmax = self.on_q[0][-1]


    def _get_original_array(self):
        if self.input_xtype in QQUANTITIES:
            return self.on_q, "q"
        elif self.input_xtype in ANGLEQUANTITIES:
            return self.on_tth, "tth"
        elif self.input_xtype in DQUANTITIES:
            return self.on_d, "d"

    def scale_to(self, target_diff_object, xtype=None, xvalue=None):
        f"""
        returns a new diffraction object which is the current object but recaled in y to the target

        Parameters
        ----------
        target_diff_object: Diffraction_object
          the diffractoin object you want to scale the current one on to
        xtype: string, optional.  Default is Q
          the xtype, from {XQUANTITIES}, that you will specify a point from to scale to
        xvalue: float. Default is the midpoint of the array
          the y-value in the target at this x-value will be used as the factor to scale to.
          The entire array is scaled be the factor that places on on top of the other at that point.
          xvalue does not have to be in the x-array, the point closest to this point will be used for the scaling.

        Returns
        -------
        the rescaled Diffraction_object as a new object

        """
        scaled = deepcopy(self)
        if xtype is None:
            xtype = "q"

        data = self.on_xtype(xtype)
        target = target_diff_object.on_xtype(xtype)
        if xvalue is None:
            xvalue = data[0][0] + (data[0][-1] - data[0][0]) / 2.

        xindex = (np.abs(data[0] - xvalue)).argmin()
        ytarget = target[1][xindex]
        yself = data[1][xindex]
        scaled.on_tth[1] = data[1]*ytarget/yself
        scaled.on_q[1] = data[1]*ytarget/yself
        return scaled

    def on_xtype(self, xtype):
        '''
        return a 2D np array with x in the first column and y in the second for x of type type
        Parameters
        ----------
        xtype

        Returns
        -------

        '''
        if xtype.lower() in ANGLEQUANTITIES:
            return self.on_tth
        elif xtype.lower() in QQUANTITIES:
            return self.on_q
        elif xtype.lower() in DQUANTITIES:
            return self.on_d
        pass

    def dump(self, filepath, xtype=None):
        if xtype is None:
            xtype = " q"
        if xtype == "q":
            data_to_save = np.column_stack((self.on_q[0], self.on_q[1]))
        elif xtype == "tth":
            data_to_save = np.column_stack((self.on_tth[0], self.on_tth[1]))
        else:
            print(f"WARNING: cannot handle the xtype '{xtype}'")

        with open(filepath, 'w') as f:
            f.write(f"[Diffraction_object]\nname = {self.name}\nwavelength = {self.wavelength}\n"
                    f"scat_quantity = {self.scat_quantity}\n")
            for key, value in self.metadata.items():
                f.write(f"{key} = {value}\n")
            f.write("\n#### start data\n")
            np.savetxt(f, data_to_save, delimiter=" ")
