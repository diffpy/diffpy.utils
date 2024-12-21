import re
import uuid
from pathlib import Path
from uuid import UUID

import numpy as np
import pytest
from deepdiff import DeepDiff
from freezegun import freeze_time

from diffpy.utils.diffraction_objects import XQUANTITIES, DiffractionObject


@pytest.mark.parametrize(
    "do_args_1, do_args_2, expected_equality, warning_expected",
    [
        # Test when __eq__ returns True and False
        # Identical args, expect equality
        (
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
            False,
        ),
        (  # Different names, expect inequality
            {
                "name": "something",
                "xtype": "tth",
                "xarray": np.empty(0),
                "yarray": np.empty(0),
                "metadata": {"thing1": 1, "thing2": "thing2"},
            },
            {
                "name": "something else",
                "xtype": "tth",
                "xarray": np.empty(0),
                "yarray": np.empty(0),
                "metadata": {"thing1": 1, "thing2": "thing2"},
            },
            False,
            True,
        ),
        (  # One without wavelength, expect inequality
            {
                "wavelength": 0.71,
                "xtype": "tth",
                "xarray": np.empty(0),
                "yarray": np.empty(0),
                "metadata": {"thing1": 1, "thing2": "thing2"},
            },
            {
                "xtype": "tth",
                "xarray": np.empty(0),
                "yarray": np.empty(0),
                "metadata": {"thing1": 1, "thing2": "thing2"},
            },
            False,
            True,
        ),
        (  # Different wavelengths, expect inequality
            {
                "wavelength": 0.71,
                "xtype": "tth",
                "xarray": np.empty(0),
                "yarray": np.empty(0),
                "metadata": {"thing1": 1, "thing2": "thing2"},
            },
            {
                "wavelength": 0.711,
                "xtype": "tth",
                "xarray": np.empty(0),
                "yarray": np.empty(0),
                "metadata": {"thing1": 1, "thing2": "thing2"},
            },
            False,
            False,
        ),
        (  # Different scat_quantity, expect inequality
            {
                "scat_quantity": "x-ray",
                "xtype": "tth",
                "xarray": np.empty(0),
                "yarray": np.empty(0),
                "metadata": {"thing1": 1, "thing2": "thing2"},
            },
            {
                "scat_quantity": "neutron",
                "xtype": "tth",
                "xarray": np.empty(0),
                "yarray": np.empty(0),
                "metadata": {"thing1": 1, "thing2": "thing2"},
            },
            False,
            True,
        ),
        (  # Different q xarray values, expect inequality
            {
                "xtype": "q",
                "xarray": np.array([1.0, 2.0]),
                "yarray": np.array([100.0, 200.0]),
            },
            {
                "xtype": "q",
                "xarray": np.array([3.0, 4.0]),
                "yarray": np.array([100.0, 200.0]),
                "metadata": {"thing1": 1, "thing2": "thing2"},
            },
            False,
            True,
        ),
        (  # Different metadata, expect inequality
            {
                "xtype": "q",
                "xarray": np.empty(0),
                "yarray": np.empty(0),
                "metadata": {"thing1": 0, "thing2": "thing2"},
            },
            {
                "xtype": "q",
                "xarray": np.empty(0),
                "yarray": np.empty(0),
                "metadata": {"thing1": 1, "thing2": "thing2"},
            },
            False,
            True,
        ),
    ],
)
def test_diffraction_objects_equality(
    do_args_1, do_args_2, expected_equality, warning_expected, wavelength_warning_msg
):
    if warning_expected:
        with pytest.warns(UserWarning, match=re.escape(wavelength_warning_msg)):
            do_1 = DiffractionObject(**do_args_1)
            do_2 = DiffractionObject(**do_args_2)
    else:
        do_1 = DiffractionObject(**do_args_1)
        do_2 = DiffractionObject(**do_args_2)
    assert (do_1 == do_2) == expected_equality


@pytest.mark.parametrize(
    "xtype, expected_xarray",
    [
        ("tth", np.array([30, 60])),
        ("2theta", np.array([30, 60])),
        ("q", np.array([0.51764, 1])),
        ("d", np.array([12.13818, 6.28319])),
    ],
)
def test_on_xtype(xtype, expected_xarray, do_minimal_tth):
    do = do_minimal_tth
    actual_xrray, actual_yarray = do.on_xtype(xtype)
    assert np.allclose(actual_xrray, expected_xarray)
    assert np.allclose(actual_yarray, np.array([1, 2]))


def test_init_invalid_xtype():
    with pytest.raises(
        ValueError,
        match=re.escape(
            f"I don't know how to handle the xtype, 'invalid_type'. "
            f"Please rerun specifying an xtype from {*XQUANTITIES, }"
        ),
    ):
        return DiffractionObject(xarray=np.empty(0), yarray=np.empty(0), xtype="invalid_type", wavelength=1.54)


@pytest.mark.parametrize(
    "org_do_args, target_do_args, scale_inputs, expected",
    [
        # Test that scale_to() scales to the correct values
        # Case 1: same x-array and y-array, check offset
        (
            {
                "xarray": np.array([10, 15, 25, 30, 60, 140]),
                "yarray": np.array([2, 3, 4, 5, 6, 7]),
                "xtype": "tth",
                "wavelength": 2 * np.pi,
            },
            {
                "xarray": np.array([10, 15, 25, 30, 60, 140]),
                "yarray": np.array([2, 3, 4, 5, 6, 7]),
                "xtype": "tth",
                "wavelength": 2 * np.pi,
            },
            {
                "q": None,
                "tth": 60,
                "d": None,
                "offset": 2.1,
            },
            {"xtype": "tth", "yarray": np.array([4.1, 5.1, 6.1, 7.1, 8.1, 9.1])},
        ),
        # Case 2: same length x-arrays with exact x-value match
        (
            {
                "xarray": np.array([10, 15, 25, 30, 60, 140]),
                "yarray": np.array([10, 20, 25, 30, 60, 100]),
                "xtype": "tth",
                "wavelength": 2 * np.pi,
            },
            {
                "xarray": np.array([10, 20, 25, 30, 60, 140]),
                "yarray": np.array([2, 3, 4, 5, 6, 7]),
                "xtype": "tth",
                "wavelength": 2 * np.pi,
            },
            {
                "q": None,
                "tth": 60,
                "d": None,
                "offset": 0,
            },
            {"xtype": "tth", "yarray": np.array([1, 2, 2.5, 3, 6, 10])},
        ),
        # Case 3: same length x-arrays with approximate x-value match
        (
            {
                "xarray": np.array([0.12, 0.24, 0.31, 0.4]),
                "yarray": np.array([10, 20, 40, 60]),
                "xtype": "q",
                "wavelength": 2 * np.pi,
            },
            {
                "xarray": np.array([0.14, 0.24, 0.31, 0.4]),
                "yarray": np.array([1, 3, 4, 5]),
                "xtype": "q",
                "wavelength": 2 * np.pi,
            },
            {
                "q": 0.1,
                "tth": None,
                "d": None,
                "offset": 0,
            },
            {"xtype": "q", "yarray": np.array([1, 2, 4, 6])},
        ),
        # Case 4: different x-array lengths with approximate x-value match
        (
            {
                "xarray": np.array([10, 25, 30.1, 40.2, 61, 120, 140]),
                "yarray": np.array([10, 20, 30, 40, 50, 60, 100]),
                "xtype": "tth",
                "wavelength": 2 * np.pi,
            },
            {
                "xarray": np.array([20, 25.5, 32, 45, 50, 62, 100, 125, 140]),
                "yarray": np.array([1.1, 2, 3, 3.5, 4, 5, 10, 12, 13]),
                "xtype": "tth",
                "wavelength": 2 * np.pi,
            },
            {
                "q": None,
                "tth": 60,
                "d": None,
                "offset": 0,
            },
            # Case 5: Scaling factor is calculated at index = 4 (tth=61) for self and index = 5 for target (tth=62)
            {"xtype": "tth", "yarray": np.array([1, 2, 3, 4, 5, 6, 10])},
        ),
    ],
)
def test_scale_to(org_do_args, target_do_args, scale_inputs, expected):
    original_do = DiffractionObject(**org_do_args)
    target_do = DiffractionObject(**target_do_args)
    scaled_do = original_do.scale_to(
        target_do, q=scale_inputs["q"], tth=scale_inputs["tth"], d=scale_inputs["d"], offset=scale_inputs["offset"]
    )
    # Check the intensity data is the same as expected
    assert np.allclose(scaled_do.on_xtype(expected["xtype"])[1], expected["yarray"])


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
    with pytest.warns(RuntimeWarning, match="divide by zero encountered in divide"):
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


@pytest.mark.parametrize(
    "do_init_args, expected_do_dict, divide_by_zero_warning_expected",
    [
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
                "scat_quantity": "",
                "qmin": np.float64(0.0),
                "qmax": np.float64(1.0),
                "tthmin": np.float64(0.0),
                "tthmax": np.float64(180.0),
                "dmin": np.float64(2 * np.pi),
                "dmax": np.float64(np.inf),
                "wavelength": 4.0 * np.pi,
            },
            True,
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
            False,
        ),
    ],
)
def test_init_valid(do_init_args, expected_do_dict, divide_by_zero_warning_expected):
    if divide_by_zero_warning_expected:
        with pytest.warns(RuntimeWarning, match="divide by zero encountered in divide"):
            actual_do_dict = DiffractionObject(**do_init_args).__dict__
    else:
        actual_do_dict = DiffractionObject(**do_init_args).__dict__
    diff = DeepDiff(
        actual_do_dict, expected_do_dict, ignore_order=True, significant_digits=13, exclude_paths="root['_id']"
    )
    assert diff == {}


@pytest.mark.parametrize(
    "do_init_args, expected_error_msg",
    [
        (  # Case 1: no arguments provided
            {},
            "missing 3 required positional arguments: 'xarray', 'yarray', and 'xtype'",
        ),
        (  # Case 2: only xarray and yarray provided
            {"xarray": np.array([0.0, 90.0]), "yarray": np.array([0.0, 90.0])},
            "missing 1 required positional argument: 'xtype'",
        ),
    ],
)
def test_init_invalid_args(
    do_init_args,
    expected_error_msg,
):
    with pytest.raises(TypeError, match=expected_error_msg):
        DiffractionObject(**do_init_args)


def test_all_array_getter(do_minimal_tth):
    actual_do = do_minimal_tth
    print(actual_do.all_arrays)
    expected_all_arrays = [[1, 0.51763809, 30, 12.13818192], [2, 1, 60, 6.28318531]]
    assert np.allclose(actual_do.all_arrays, expected_all_arrays)


def test_all_array_setter(do_minimal):
    do = do_minimal
    # Attempt to directly modify the property
    with pytest.raises(
        AttributeError,
        match="Direct modification of attribute 'all_arrays' is not allowed. "
        "Please use 'input_data' to modify 'all_arrays'.",
    ):
        do.all_arrays = np.empty((4, 4))


def test_id_getter(do_minimal):
    do = do_minimal
    assert hasattr(do, "id")
    assert isinstance(do.id, UUID)
    assert len(str(do.id)) == 36


def test_id_getter_with_mock(mocker, do_minimal):
    mocker.patch.object(DiffractionObject, "id", new_callable=lambda: UUID("d67b19c6-3016-439f-81f7-cf20a04bee87"))
    do = do_minimal
    assert do.id == UUID("d67b19c6-3016-439f-81f7-cf20a04bee87")


def test_id_setter_error(do_minimal):
    do = do_minimal

    with pytest.raises(
        AttributeError,
        match="Direct modification of attribute 'id' is not allowed. Please use 'input_data' to modify 'id'.",
    ):
        do.id = uuid.uuid4()


def test_xarray_yarray_length_mismatch():
    with pytest.raises(
        ValueError,
        match="'xarray' and 'yarray' are different lengths.  "
        "They must correspond to each other and have the same length. Please "
        "re-initialize 'DiffractionObject'with valid 'xarray' and 'yarray's",
    ):
        DiffractionObject(
            xarray=np.array([1.0, 2.0]), yarray=np.array([0.0, 0.0, 0.0]), xtype="tth", wavelength=1.54
        )


def test_input_xtype_getter(do_minimal):
    do = do_minimal
    assert do.input_xtype == "tth"


def test_input_xtype_setter_error(do_minimal):
    do = do_minimal
    with pytest.raises(
        AttributeError,
        match="Direct modification of attribute 'input_xtype' is not allowed. "
        "Please use 'input_data' to modify 'input_xtype'.",
    ):
        do.input_xtype = "q"


def test_copy_object(do_minimal):
    do = do_minimal
    do_copy = do.copy()
    assert do == do_copy
    assert id(do) != id(do_copy)
