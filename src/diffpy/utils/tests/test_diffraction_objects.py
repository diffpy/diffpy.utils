import numpy as np
from pathlib import Path
from diffpy.utils.scattering_objects.diffraction_objects import Diffraction_object
import pytest


params = [
	(["", None, "", [], {}], ["", None, "", [], {}], True),	# empty
	(["test", 0.71, "x-ray", [[1,2], [3,4]], {"thing1": 1, "thing2": "thing2"}],
	 ["test", 0.71, "x-ray", [[1,2], [3,4]], {"thing2": "thing2", "thing1": 1}],
	 True),		# Compare same attributes
	(["test1", 0.71, "", [[1,2], [3,4]], {"thing1": 1, "thing2": "thing2"}],
	 ["test2", 0.71, "", [[1,2], [3,4]], {"thing1": 1, "thing2": "thing2"}],
	 False),	# Different names
	(["test", 0.71, "", [[1, 2], [3, 4]], {"thing1": 1, "thing2": "thing2"}],
	 ["test", 1.54, "", [[1, 2], [3, 4]], {"thing1": 1, "thing2": "thing2"}],
	 False),	# Different wavelengths
	(["test", 0.71, "", [[1, 2], [3, 4]], {"thing1": 1, "thing2": "thing2"}],
	 ["test", 0.71, "x-ray", [[1, 2], [3, 4]], {"thing1": 1, "thing2": "thing2"}],
	 False),	# Different scat_quantity
	(["test", 0.71, "", [[1, 2], [3, 4]], {"thing1": 1, "thing2": "thing2"}],
	 ["test", 0.71, "", [[1, 3], [3, 4]], {"thing1": 1, "thing2": "thing2"}],
	 False),	# Different on_q, on_tth, on_d
	(["test", 0.71, "", [[1, 2], [3, 4]], {"thing1": 0, "thing2": "thing2"}],
	 ["test", 0.71, "", [[1, 2], [3, 4]], {"thing1": 1, "thing2": "thing2"}],
	 False),	# Different metadata
]

@pytest.mark.parametrize("inputs1, inputs2, expected", params)
def test_diffraction_objects_equality(inputs1, inputs2, expected):
	diffraction_object1 = Diffraction_object(name=inputs1[0], wavelength=inputs1[1])
	diffraction_object2 = Diffraction_object(name=inputs2[0], wavelength=inputs2[1])
	diffraction_object1.scat_quantity = inputs1[2]
	diffraction_object2.scat_quantity = inputs2[2]
	diffraction_object1.on_q = inputs1[3]
	diffraction_object2.on_q = inputs2[3]
	diffraction_object1.on_tth = inputs1[3]
	diffraction_object2.on_tth = inputs2[3]
	diffraction_object1.on_d = inputs1[3]
	diffraction_object2.on_d = inputs2[3]
	diffraction_object1.metadata = inputs1[4]
	diffraction_object2.metadata = inputs2[4]
	assert (diffraction_object1 == diffraction_object2) == expected
	assert Diffraction_object() == Diffraction_object()

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
