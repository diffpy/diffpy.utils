import re
import uuid
from pathlib import Path
from uuid import UUID

import numpy as np
import pytest
from deepdiff import DeepDiff
from freezegun import freeze_time

from diffpy.utils.diffraction_objects import XQUANTITIES, DiffractionObject

params = [
    (  # Default
        {},
        {},
        True,
    ),
    (  # Compare same attributes
        {
            "name": "same",
            "scat_quantity": "x-ray",
            "wavelength": 0.71,
            "xtype": "q",
            "xarray": np.array([1.0, 2.0]),
            "yarray": np.array([100.0, 200.0]),
            "metadata": {"thing1": 1},
        },
        {
            "name": "same",
            "scat_quantity": "x-ray",
            "wavelength": 0.71,
            "xtype": "q",
            "xarray": np.array([1.0, 2.0]),
            "yarray": np.array([100.0, 200.0]),
            "metadata": {"thing1": 1},
        },
        True,
    ),
    (  # Different names
        {
            "name": "something",
            "scat_quantity": "",
            "wavelength": None,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        {
            "name": "something else",
            "scat_quantity": "",
            "wavelength": None,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        False,
    ),
    (  # Different wavelengths
        {
            "scat_quantity": "",
            "wavelength": 0.71,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        {
            "scat_quantity": "",
            "wavelength": None,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        False,
    ),
    (  # Different wavelengths
        {
            "scat_quantity": "",
            "wavelength": 0.71,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        {
            "scat_quantity": "",
            "wavelength": 0.711,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        False,
    ),
    (  # Different scat_quantity
        {
            "scat_quantity": "x-ray",
            "wavelength": None,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        {
            "scat_quantity": "neutron",
            "wavelength": None,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        False,
    ),
    (  # Different on_q
        {
            "scat_quantity": "",
            "wavelength": None,
            "xtype": "q",
            "xarray": np.array([1.0, 2.0]),
            "yarray": np.array([100.0, 200.0]),
            "metadata": {},
        },
        {
            "scat_quantity": "",
            "wavelength": None,
            "xtype": "q",
            "xarray": np.array([3.0, 4.0]),
            "yarray": np.array([100.0, 200.0]),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        False,
    ),
    (  # Different metadata
        {
            "scat_quantity": "",
            "wavelength": None,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 0, "thing2": "thing2"},
        },
        {
            "scat_quantity": "",
            "wavelength": None,
            "xtype": "",
            "xarray": np.empty(0),
            "yarray": np.empty(0),
            "metadata": {"thing1": 1, "thing2": "thing2"},
        },
        False,
    ),
]


@pytest.mark.parametrize("inputs1, inputs2, expected", params)
def test_diffraction_objects_equality(inputs1, inputs2, expected):
    do_1 = DiffractionObject(**inputs1)
    do_2 = DiffractionObject(**inputs2)
    assert (do_1 == do_2) == expected


@pytest.mark.parametrize(
    "input_xtype, expected_xarray",
    [
        ("tth", np.array([30, 60])),
        ("2theta", np.array([30, 60])),
        ("q", np.array([0.51764, 1])),
        ("d", np.array([12.13818, 6.28319])),
    ],
)
def test_on_xtype(input_xtype, expected_xarray, do_minimal_tth):
    do = do_minimal_tth
    result = do.on_xtype(input_xtype)
    assert np.allclose(result[0], expected_xarray)
    assert np.allclose(result[1], np.array([1, 2]))


def test_init_invalid_xtype():
    with pytest.raises(
        ValueError,
        match=re.escape(
            f"I don't know how to handle the xtype, 'invalid_type'. "
            f"Please rerun specifying an xtype from {*XQUANTITIES, }"
        ),
    ):
        DiffractionObject(xtype="invalid_type")


params_scale_to = [
    # UC1: same x-array and y-array, check offset
    (
        {
            "xarray": np.array([10, 15, 25, 30, 60, 140]),
            "yarray": np.array([2, 3, 4, 5, 6, 7]),
            "xtype": "tth",
            "wavelength": 2 * np.pi,
            "target_xarray": np.array([10, 15, 25, 30, 60, 140]),
            "target_yarray": np.array([2, 3, 4, 5, 6, 7]),
            "target_xtype": "tth",
            "target_wavelength": 2 * np.pi,
            "q": None,
            "tth": 60,
            "d": None,
            "offset": 2.1,
        },
        {"xtype": "tth", "yarray": np.array([4.1, 5.1, 6.1, 7.1, 8.1, 9.1])},
    ),
    # UC2: same length x-arrays with exact x-value match
    (
        {
            "xarray": np.array([10, 15, 25, 30, 60, 140]),
            "yarray": np.array([10, 20, 25, 30, 60, 100]),
            "xtype": "tth",
            "wavelength": 2 * np.pi,
            "target_xarray": np.array([10, 20, 25, 30, 60, 140]),
            "target_yarray": np.array([2, 3, 4, 5, 6, 7]),
            "target_xtype": "tth",
            "target_wavelength": 2 * np.pi,
            "q": None,
            "tth": 60,
            "d": None,
            "offset": 0,
        },
        {"xtype": "tth", "yarray": np.array([1, 2, 2.5, 3, 6, 10])},
    ),
    # UC3: same length x-arrays with approximate x-value match
    (
        {
            "xarray": np.array([0.12, 0.24, 0.31, 0.4]),
            "yarray": np.array([10, 20, 40, 60]),
            "xtype": "q",
            "wavelength": 2 * np.pi,
            "target_xarray": np.array([0.14, 0.24, 0.31, 0.4]),
            "target_yarray": np.array([1, 3, 4, 5]),
            "target_xtype": "q",
            "target_wavelength": 2 * np.pi,
            "q": 0.1,
            "tth": None,
            "d": None,
            "offset": 0,
        },
        {"xtype": "q", "yarray": np.array([1, 2, 4, 6])},
    ),
    # UC4: different x-array lengths with approximate x-value match
    (
        {
            "xarray": np.array([10, 25, 30.1, 40.2, 61, 120, 140]),
            "yarray": np.array([10, 20, 30, 40, 50, 60, 100]),
            "xtype": "tth",
            "wavelength": 2 * np.pi,
            "target_xarray": np.array([20, 25.5, 32, 45, 50, 62, 100, 125, 140]),
            "target_yarray": np.array([1.1, 2, 3, 3.5, 4, 5, 10, 12, 13]),
            "target_xtype": "tth",
            "target_wavelength": 2 * np.pi,
            "q": None,
            "tth": 60,
            "d": None,
            "offset": 0,
        },
        # scaling factor is calculated at index = 4 (tth=61) for self and index = 5 for target (tth=62)
        {"xtype": "tth", "yarray": np.array([1, 2, 3, 4, 5, 6, 10])},
    ),
]


@pytest.mark.parametrize("inputs, expected", params_scale_to)
def test_scale_to(inputs, expected):
    orig_diff_object = DiffractionObject(
        xarray=inputs["xarray"], yarray=inputs["yarray"], xtype=inputs["xtype"], wavelength=inputs["wavelength"]
    )
    target_diff_object = DiffractionObject(
        xarray=inputs["target_xarray"],
        yarray=inputs["target_yarray"],
        xtype=inputs["target_xtype"],
        wavelength=inputs["target_wavelength"],
    )
    scaled_diff_object = orig_diff_object.scale_to(
        target_diff_object, q=inputs["q"], tth=inputs["tth"], d=inputs["d"], offset=inputs["offset"]
    )
    # Check the intensity data is the same as expected
    assert np.allclose(scaled_diff_object.on_xtype(expected["xtype"])[1], expected["yarray"])


params_scale_to_bad = [
    # UC1: user did not specify anything
    (
        {
            "xarray": np.array([0.1, 0.2, 0.3]),
            "yarray": np.array([1, 2, 3]),
            "xtype": "q",
            "wavelength": 2 * np.pi,
            "target_xarray": np.array([0.05, 0.1, 0.2, 0.3]),
            "target_yarray": np.array([5, 10, 20, 30]),
            "target_xtype": "q",
            "target_wavelength": 2 * np.pi,
            "q": None,
            "tth": None,
            "d": None,
            "offset": 0,
        }
    ),
    # UC2: user specified more than one of q, tth, and d
    (
        {
            "xarray": np.array([10, 25, 30.1, 40.2, 61, 120, 140]),
            "yarray": np.array([10, 20, 30, 40, 50, 60, 100]),
            "xtype": "tth",
            "wavelength": 2 * np.pi,
            "target_xarray": np.array([20, 25.5, 32, 45, 50, 62, 100, 125, 140]),
            "target_yarray": np.array([1.1, 2, 3, 3.5, 4, 5, 10, 12, 13]),
            "target_xtype": "tth",
            "target_wavelength": 2 * np.pi,
            "q": None,
            "tth": 60,
            "d": 10,
            "offset": 0,
        }
    ),
]


@pytest.mark.parametrize("inputs", params_scale_to_bad)
def test_scale_to_bad(inputs):
    orig_diff_object = DiffractionObject(
        xarray=inputs["xarray"], yarray=inputs["yarray"], xtype=inputs["xtype"], wavelength=inputs["wavelength"]
    )
    target_diff_object = DiffractionObject(
        xarray=inputs["target_xarray"],
        yarray=inputs["target_yarray"],
        xtype=inputs["target_xtype"],
        wavelength=inputs["target_wavelength"],
    )
    with pytest.raises(
        ValueError, match="You must specify exactly one of 'q', 'tth', or 'd'. Please rerun specifying only one."
    ):
        orig_diff_object.scale_to(
            target_diff_object, q=inputs["q"], tth=inputs["tth"], d=inputs["d"], offset=inputs["offset"]
        )


params_index = [
    # UC1: exact match
    (4 * np.pi, np.array([30.005, 60]), np.array([1, 2]), "tth", "tth", 30.005, [0]),
    # UC2: target value lies in the array, returns the (first) closest index
    (4 * np.pi, np.array([30, 60]), np.array([1, 2]), "tth", "tth", 45, [0]),
    (4 * np.pi, np.array([30, 60]), np.array([1, 2]), "tth", "q", 0.25, [0]),
    # UC3: target value out of the range, returns the closest index
    (4 * np.pi, np.array([0.25, 0.5, 0.71]), np.array([1, 2, 3]), "q", "q", 0.1, [0]),
    (4 * np.pi, np.array([30, 60]), np.array([1, 2]), "tth", "tth", 63, [1]),
]


@pytest.mark.parametrize("wavelength, xarray, yarray, xtype_1, xtype_2, value, expected_index", params_index)
def test_get_array_index(wavelength, xarray, yarray, xtype_1, xtype_2, value, expected_index):
    do = DiffractionObject(wavelength=wavelength, xarray=xarray, yarray=yarray, xtype=xtype_1)
    actual_index = do.get_array_index(value=value, xtype=xtype_2)
    assert actual_index == expected_index


def test_get_array_index_bad():
    do = DiffractionObject(wavelength=2 * np.pi, xarray=np.array([]), yarray=np.array([]), xtype="tth")
    with pytest.raises(ValueError, match=re.escape("The 'tth' array is empty. Please ensure it is initialized.")):
        do.get_array_index(value=30)


def test_dump(tmp_path, mocker):
    x, y = np.linspace(0, 5, 6), np.linspace(0, 5, 6)
    directory = Path(tmp_path)
    file = directory / "testfile"
    do = DiffractionObject(
        wavelength=1.54,
        name="test",
        scat_quantity="x-ray",
        xarray=np.array(x),
        yarray=np.array(y),
        xtype="q",
        metadata={"thing1": 1, "thing2": "thing2", "package_info": {"package2": "3.4.5"}},
    )
    mocker.patch("importlib.metadata.version", return_value="3.3.0")
    with freeze_time("2012-01-14"):
        do.dump(file, "q")
    with open(file, "r") as f:
        actual = f.read()
    expected = (
        "[DiffractionObject]\nname = test\nwavelength = 1.54\nscat_quantity = x-ray\nthing1 = 1\n"
        "thing2 = thing2\npackage_info = {'package2': '3.4.5', 'diffpy.utils': '3.3.0'}\n"
        "creation_time = 2012-01-14 00:00:00\n\n"
        "#### start data\n0.000000000000000000e+00 0.000000000000000000e+00\n"
        "1.000000000000000000e+00 1.000000000000000000e+00\n"
        "2.000000000000000000e+00 2.000000000000000000e+00\n"
        "3.000000000000000000e+00 3.000000000000000000e+00\n"
        "4.000000000000000000e+00 4.000000000000000000e+00\n"
        "5.000000000000000000e+00 5.000000000000000000e+00\n"
    )

    assert actual == expected


tc_params = [
    (
        {},
        {
            "_all_arrays": np.empty(shape=(0, 4)),  # instantiate empty
            "metadata": {},
            "_input_xtype": "",
            "name": "",
            "scat_quantity": None,
            "qmin": np.float64(np.inf),
            "qmax": np.float64(0.0),
            "tthmin": np.float64(np.inf),
            "tthmax": np.float64(0.0),
            "dmin": np.float64(np.inf),
            "dmax": np.float64(0.0),
            "wavelength": None,
        },
    ),
    (  # instantiate just non-array attributes
        {"name": "test", "scat_quantity": "x-ray", "metadata": {"thing": "1", "another": "2"}},
        {
            "_all_arrays": np.empty(shape=(0, 4)),
            "metadata": {"thing": "1", "another": "2"},
            "_input_xtype": "",
            "name": "test",
            "scat_quantity": "x-ray",
            "qmin": np.float64(np.inf),
            "qmax": np.float64(0.0),
            "tthmin": np.float64(np.inf),
            "tthmax": np.float64(0.0),
            "dmin": np.float64(np.inf),
            "dmax": np.float64(0.0),
            "wavelength": None,
        },
    ),
    (  # instantiate just array attributes
        {
            "xarray": np.array([0.0, 90.0, 180.0]),
            "yarray": np.array([1.0, 2.0, 3.0]),
            "xtype": "tth",
            "wavelength": 4.0 * np.pi,
        },
        {
            "_all_arrays": np.array(
                [
                    [1.0, 0.0, 0.0, np.float64(np.inf)],
                    [2.0, 1.0 / np.sqrt(2), 90.0, np.sqrt(2) * 2 * np.pi],
                    [3.0, 1.0, 180.0, 1.0 * 2 * np.pi],
                ]
            ),
            "metadata": {},
            "_input_xtype": "tth",
            "name": "",
            "scat_quantity": None,
            "qmin": np.float64(0.0),
            "qmax": np.float64(1.0),
            "tthmin": np.float64(0.0),
            "tthmax": np.float64(180.0),
            "dmin": np.float64(2 * np.pi),
            "dmax": np.float64(np.inf),
            "wavelength": 4.0 * np.pi,
        },
    ),
    (  # instantiate just array attributes
        {
            "xarray": np.array([np.inf, 2 * np.sqrt(2) * np.pi, 2 * np.pi]),
            "yarray": np.array([1.0, 2.0, 3.0]),
            "xtype": "d",
            "wavelength": 4.0 * np.pi,
            "scat_quantity": "x-ray",
        },
        {
            "_all_arrays": np.array(
                [
                    [1.0, 0.0, 0.0, np.float64(np.inf)],
                    [2.0, 1.0 / np.sqrt(2), 90.0, np.sqrt(2) * 2 * np.pi],
                    [3.0, 1.0, 180.0, 1.0 * 2 * np.pi],
                ]
            ),
            "metadata": {},
            "_input_xtype": "d",
            "name": "",
            "scat_quantity": "x-ray",
            "qmin": np.float64(0.0),
            "qmax": np.float64(1.0),
            "tthmin": np.float64(0.0),
            "tthmax": np.float64(180.0),
            "dmin": np.float64(2 * np.pi),
            "dmax": np.float64(np.inf),
            "wavelength": 4.0 * np.pi,
        },
    ),
]


@pytest.mark.parametrize("inputs, expected", tc_params)
def test_constructor(inputs, expected):
    actual = DiffractionObject(**inputs).__dict__
    diff = DeepDiff(actual, expected, ignore_order=True, significant_digits=13, exclude_paths="root['_id']")
    assert diff == {}


def test_all_array_getter():
    actual_do = DiffractionObject(
        xarray=np.array([0.0, 90.0, 180.0]),
        yarray=np.array([1.0, 2.0, 3.0]),
        xtype="tth",
        wavelength=4.0 * np.pi,
    )
    expected_all_arrays = np.array(
        [
            [1.0, 0.0, 0.0, np.float64(np.inf)],
            [2.0, 1.0 / np.sqrt(2), 90.0, np.sqrt(2) * 2 * np.pi],
            [3.0, 1.0, 180.0, 1.0 * 2 * np.pi],
        ]
    )
    assert np.allclose(actual_do.all_arrays, expected_all_arrays)


def test_all_array_setter():
    do = DiffractionObject()

    # Attempt to directly modify the property
    with pytest.raises(
        AttributeError,
        match="Direct modification of attribute 'all_arrays' is not allowed. "
        "Please use 'input_data' to modify 'all_arrays'.",
    ):
        do.all_arrays = np.empty((4, 4))


def test_id_getter():
    do = DiffractionObject()
    assert hasattr(do, "id")
    assert isinstance(do.id, UUID)
    assert len(str(do.id)) == 36


def test_id_getter_with_mock(mocker):
    mocker.patch.object(DiffractionObject, "id", new_callable=lambda: UUID("d67b19c6-3016-439f-81f7-cf20a04bee87"))
    do = DiffractionObject()
    assert do.id == UUID("d67b19c6-3016-439f-81f7-cf20a04bee87")


def test_id_setter_error():
    do = DiffractionObject()

    with pytest.raises(
        AttributeError,
        match="Direct modification of attribute 'id' is not allowed. Please use 'input_data' to modify 'id'.",
    ):
        do.id = uuid.uuid4()


def test_xarray_yarray_length_mismatch():
    with pytest.raises(
        ValueError,
        match="'xarray' and 'yarray' must have the same length. "
        "Please re-initialize 'DiffractionObject' or re-run the method 'input_data' "
        "with 'xarray' and 'yarray' of identical length",
    ):
        DiffractionObject(xarray=np.array([1.0, 2.0]), yarray=np.array([0.0, 0.0, 0.0]))


def test_input_xtype_getter():
    do = DiffractionObject(xtype="tth")
    assert do.input_xtype == "tth"


def test_input_xtype_setter_error():
    do = DiffractionObject(xtype="tth")

    # Attempt to directly modify the property
    with pytest.raises(
        AttributeError,
        match="Direct modification of attribute 'input_xtype' is not allowed. "
        "Please use 'input_data' to modify 'input_xtype'.",
    ):
        do.input_xtype = "q"


def test_copy_object():
    do = DiffractionObject(
        name="test",
        wavelength=4.0 * np.pi,
        xarray=np.array([0.0, 90.0, 180.0]),
        yarray=np.array([1.0, 2.0, 3.0]),
        xtype="tth",
    )
    do_copy = do.copy()
    assert do == do_copy
    assert id(do) != id(do_copy)
