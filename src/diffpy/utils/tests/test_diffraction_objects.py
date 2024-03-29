import numpy as np
from pathlib import Path
from diffpy.utils.scattering_objects.diffraction_objects import Diffraction_object

def test_dump(tmp_path):
	x, y = np.linspace(0, 10, 11), np.linspace(0, 10, 11)
	directory = Path(tmp_path)
	file = directory / "testfile"
	test = Diffraction_object()
	test.wavelength = 1.54
	test.name = "test"
	test.scat_quantity = "x-ray"
	test.insert_scattering_quantity(x, y, "q", metadata={"thing1": 1, "thing2": "thing2"})
	test.dump(file, "q")
	with open(file, "r") as f:
		actual = f.read()
	expected = ("[Diffraction_object]\nname = test\nwavelength = 1.54\nscat_quantity = x-ray\nthing1 = 1\n"
				"thing2 = thing2\n\n#### start data\n0.000000000000000000e+00 0.000000000000000000e+00\n"
				"1.000000000000000000e+00 1.000000000000000000e+00\n2.000000000000000000e+00 2.000000000000000000e+00\n"
				"3.000000000000000000e+00 3.000000000000000000e+00\n4.000000000000000000e+00 4.000000000000000000e+00\n"
				"5.000000000000000000e+00 5.000000000000000000e+00\n"
				"6.000000000000000000e+00 6.000000000000000000e+00\n7.000000000000000000e+00 7.000000000000000000e+00\n"
				"8.000000000000000000e+00 8.000000000000000000e+00\n9.000000000000000000e+00 9.000000000000000000e+00\n"
				"1.000000000000000000e+01 1.000000000000000000e+01\n")
	assert actual == expected
