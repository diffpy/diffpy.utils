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
    "do_args_1, do_args_2, expected_equality, wavelength_warning_expected",
    [
        # Test when __eq__ returns True and False
        (  # C1: Identical args, expect equality
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
        (  # C2: Different names, expect inequality
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
        (  # C3: One without wavelength, expect inequality
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
        (  # C4: Different wavelength values, expect inequality
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
        (  # C5: Different scat_quantity, expect inequality
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
        (  # C6: Different q xarray values, expect inequality
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
        (  # C7: Different metadata, expect inequality
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
    do_args_1,
    do_args_2,
    expected_equality,
    wavelength_warning_expected,
    wavelength_warning_msg,
):
    if wavelength_warning_expected:
        with pytest.warns(
            UserWarning, match=re.escape(wavelength_warning_msg)
        ):
            do_1 = DiffractionObject(**do_args_1)
            do_2 = DiffractionObject(**do_args_2)
    else:
        do_1 = DiffractionObject(**do_args_1)
        do_2 = DiffractionObject(**do_args_2)
    assert (do_1 == do_2) == expected_equality


@pytest.mark.parametrize(
    "xtype, expected_xarray",
    [
        # Test whether on_xtype returns the correct xarray values.
        # C1: tth to tth, expect no change in xarray value
        # 1. "tth" provided, expect tth
        ("tth", np.array([30, 60])),
        # 2. "2theta" provided, expect tth
        ("2theta", np.array([30, 60])),
        # C2: "q" provided, expect q converted from tth
        ("q", np.array([0.51764, 1])),
        # C3: "d" provided, expect d converted from tth
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
        return DiffractionObject(
            xarray=np.empty(0),
            yarray=np.empty(0),
            xtype="invalid_type",
            wavelength=1.54,
        )


@pytest.mark.parametrize(
    "org_do_args, target_do_args, scale_inputs, expected",
    [
        # Test whether the original y-array is scaled as expected
        (  # C1: none of q, tth, d, provided, expect to scale on the maximal
            # intensity from each object
            {
                "xarray": np.array([0.1, 0.2, 0.3]),
                "yarray": np.array([1, 2, 3]),
                "xtype": "q",
                "wavelength": 2 * np.pi,
            },
            {
                "xarray": np.array([0.05, 0.1, 0.2, 0.3]),
                "yarray": np.array([5, 10, 20, 30]),
                "xtype": "q",
                "wavelength": 2 * np.pi,
            },
            {},
            {"xtype": "q", "yarray": np.array([10, 20, 30])},
        ),
        (  # C2: Same x-arrays
            # x-value has exact matches at tth=60 (y=60) and tth=60 (y=6),
            # for original and target diffraction objects,
            # expect original y-array to multiply by 6/60=1/10
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
            {"tth": 60},
            {"xtype": "tth", "yarray": np.array([1, 2, 2.5, 3, 6, 10])},
        ),
        (  # C3: Different x-arrays with same length,
            # x-value has closest match at q=0.12 (y=10) and q=0.14 (y=1)
            # for original and target diffraction objects,
            # expect original y-array to multiply by 1/10
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
            {"q": 0.1},
            {"xtype": "q", "yarray": np.array([1, 2, 4, 6])},
        ),
        (  # C4: Different x-array lengths
            # x-value has closest matches at tth=61 (y=50) and tth=62 (y=5),
            # for original and target diffraction objects,
            # expect original y-array to multiply by 5/50=1/10
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
            {"tth": 60},
            {"xtype": "tth", "yarray": np.array([1, 2, 3, 4, 5, 6, 10])},
        ),
        (  # C5.1: Reuse test case from C1, none of q, tth, d, provided, but
            # include an offset, expect scaled y-array in C1 to shift up by 2
            {
                "xarray": np.array([0.1, 0.2, 0.3]),
                "yarray": np.array([1, 2, 3]),
                "xtype": "q",
                "wavelength": 2 * np.pi,
            },
            {
                "xarray": np.array([0.05, 0.1, 0.2, 0.3]),
                "yarray": np.array([5, 10, 20, 30]),
                "xtype": "q",
                "wavelength": 2 * np.pi,
            },
            {"offset": 2},
            {"xtype": "q", "yarray": np.array([12, 22, 32])},
        ),
        (  # C5.2: Reuse test case from C4, but include an offset, expect
            # scaled y-array in C4 to shift up by 2
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
            {"tth": 60, "offset": 2},
            {"xtype": "tth", "yarray": np.array([3, 4, 5, 6, 7, 8, 12])},
        ),
    ],
)
def test_scale_to(org_do_args, target_do_args, scale_inputs, expected):
    original_do = DiffractionObject(**org_do_args)
    target_do = DiffractionObject(**target_do_args)
    scaled_do = original_do.scale_to(target_do, **scale_inputs)
    # Check the intensity data is the same as expected
    assert np.allclose(
        scaled_do.on_xtype(expected["xtype"])[1], expected["yarray"]
    )


@pytest.mark.parametrize(
    "org_do_args, target_do_args, scale_inputs",
    [
        # Test expected errors produced from scale_to() with invalid inputs
        (  # C2: tth and d both provided, expect ValueError
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
                "tth": 60,
                "d": 10,
            },
        ),
    ],
)
def test_scale_to_bad(org_do_args, target_do_args, scale_inputs):
    original_do = DiffractionObject(**org_do_args)
    target_do = DiffractionObject(**target_do_args)
    with pytest.raises(
        ValueError,
        match="You must specify none or exactly one of 'q', 'tth', or 'd'. "
        "Please provide either none or one value.",
    ):
        original_do.scale_to(target_do, **scale_inputs)


@pytest.mark.parametrize(
    "do_args, get_array_index_inputs, expected_index",
    [
        # Test get_array_index() returns the expected index given xtype and
        # value
        (  # C1: Target value is in the xarray and xtype is identical, expect
            # exact index match
            {
                "wavelength": 4 * np.pi,
                "xarray": np.array([30.005, 60]),
                "yarray": np.array([1, 2]),
                "xtype": "tth",
            },
            {
                "xtype": "tth",
                "value": 30.005,
            },
            0,
        ),
        (  # C2: Target value lies in the array, expect the (first) closest
            # index
            {
                "wavelength": 4 * np.pi,
                "xarray": np.array([30, 60]),
                "yarray": np.array([1, 2]),
                "xtype": "tth",
            },
            {
                "xtype": "tth",
                "value": 45,
            },
            0,
        ),
        (
            {
                "wavelength": 4 * np.pi,
                "xarray": np.array([30, 60]),
                "yarray": np.array([1, 2]),
                "xtype": "tth",
            },
            {
                "xtype": "q",
                "value": 0.25,
            },
            0,
        ),
        # C3: Target value out of the range, expect the closest index
        (  # 1. Test with xtype of "q"
            {
                "wavelength": 4 * np.pi,
                "xarray": np.array([0.25, 0.5, 0.71]),
                "yarray": np.array([1, 2, 3]),
                "xtype": "q",
            },
            {
                "xtype": "q",
                "value": 0.1,
            },
            0,
        ),
        (  # 2. Test with xtype of "tth"
            {
                "wavelength": 4 * np.pi,
                "xarray": np.array([30, 60]),
                "yarray": np.array([1, 2]),
                "xtype": "tth",
            },
            {
                "xtype": "tth",
                "value": 63,
            },
            1,
        ),
    ],
)
def test_get_array_index(do_args, get_array_index_inputs, expected_index):
    do = DiffractionObject(**do_args)
    actual_index = do.get_array_index(
        get_array_index_inputs["xtype"], get_array_index_inputs["value"]
    )
    assert actual_index == expected_index


def test_get_array_index_bad():
    do = DiffractionObject(
        wavelength=2 * np.pi,
        xarray=np.array([]),
        yarray=np.array([]),
        xtype="tth",
    )
    with pytest.raises(
        ValueError,
        match=re.escape(
            "The 'tth' array is empty. Please ensure it is initialized."
        ),
    ):
        do.get_array_index(xtype="tth", xvalue=30)


def test_dump(tmp_path, mocker):
    x, y = np.linspace(0, 5, 6), np.linspace(0, 5, 6)
    directory = Path(tmp_path)
    file = directory / "testfile"
    with pytest.warns(
        RuntimeWarning, match="divide by zero encountered in divide"
    ):
        do = DiffractionObject(
            wavelength=1.54,
            name="test",
            scat_quantity="x-ray",
            xarray=np.array(x),
            yarray=np.array(y),
            xtype="q",
            metadata={
                "thing1": 1,
                "thing2": "thing2",
                "package_info": {"package2": "3.4.5"},
            },
        )
    mocker.patch("importlib.metadata.version", return_value="3.3.0")
    with freeze_time("2012-01-14"):
        do.dump(file, "q")
    with open(file, "r") as f:
        actual = f.read()
    expected = (
        "[DiffractionObject]\n"
        "name = test\n"
        "wavelength = 1.54\n"
        "scat_quantity = x-ray\n"
        "thing1 = 1\n"
        "thing2 = thing2\n"
        "package_info = {'package2': '3.4.5', 'diffpy.utils': '3.3.0'}\n"
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
    (
        "do_init_args, expected_do_dict, "
        "divide_by_zero_warning_expected, wavelength_warning_expected"
    ),
    [
        # Test __dict__ of DiffractionObject instance initialized with valid
        # arguments
        (  # C1: Instantiate DO with empty arrays, expect it to be a valid DO,
            # but with everything empty
            {
                "xarray": np.empty(0),
                "yarray": np.empty(0),
                "xtype": "tth",
            },
            {
                "_all_arrays": np.array([]),
                "_input_xtype": "tth",
                "metadata": {},
                "name": "",
                "scat_quantity": "",
                "qmin": np.float64(np.inf),
                "qmax": np.float64(0.0),
                "tthmin": np.float64(np.inf),
                "tthmax": np.float64(0.0),
                "dmin": np.float64(np.inf),
                "dmax": np.float64(0.0),
                "wavelength": None,
            },
            False,
            True,
        ),
        (  # C2: Instantiate just DO with empty array like in C1 but with
            # wavelength, xtype, name, and metadata expect a valid DO with
            # empty arrays, but with some non-array attributes
            {
                "xarray": np.empty(0),
                "yarray": np.empty(0),
                "xtype": "tth",
                "name": "test_name",
                "wavelength": 1.54,
                "metadata": {"item_1": "1", "item_2": "2"},
            },
            {
                "_all_arrays": np.array([]),
                "_input_xtype": "tth",
                "metadata": {"item_1": "1", "item_2": "2"},
                "name": "test_name",
                "scat_quantity": "",
                "qmin": np.float64(np.inf),
                "qmax": np.float64(0.0),
                "tthmin": np.float64(np.inf),
                "tthmax": np.float64(0.0),
                "dmin": np.float64(np.inf),
                "dmax": np.float64(0.0),
                "wavelength": 1.54,
            },
            False,
            False,
        ),
        (  # C3: Minimum arguments provided for init with non-empty values
            # for xarray and yarray and wavelength expect all attributes set
            # without None
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
            False,
        ),
        (  # C4: Same as C3, but with an optional scat_quantity argument,
            # expect non-empty string for scat_quantity
            {
                "xarray": np.array(
                    [np.inf, 2 * np.sqrt(2) * np.pi, 2 * np.pi]
                ),
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
            False,
        ),
    ],
)
def test_init_valid(
    do_init_args,
    expected_do_dict,
    divide_by_zero_warning_expected,
    wavelength_warning_expected,
    wavelength_warning_msg,
):
    if divide_by_zero_warning_expected:
        with pytest.warns(
            RuntimeWarning, match="divide by zero encountered in divide"
        ):
            actual_do_dict = DiffractionObject(**do_init_args).__dict__
    elif wavelength_warning_expected:
        with pytest.warns(
            UserWarning, match=re.escape(wavelength_warning_msg)
        ):
            actual_do_dict = DiffractionObject(**do_init_args).__dict__
    else:
        actual_do_dict = DiffractionObject(**do_init_args).__dict__
    diff = DeepDiff(
        actual_do_dict,
        expected_do_dict,
        ignore_order=True,
        significant_digits=13,
        exclude_paths="root['_uuid']",
    )
    assert diff == {}


@pytest.mark.parametrize(
    "do_init_args, expected_error_msg",
    [
        # Test expected error messages when 3 required arguments not provided
        # in DiffractionObject init
        (  # C1: No arguments provided, expect 3 required positional
            # arguments error
            {},
            (
                "missing 3 required positional arguments: "
                "'xarray', 'yarray', and 'xtype'"
            ),
        ),
        (  # C2: Only xarray and yarray provided, expect 1 required
            # positional argument error
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
    expected_all_arrays = [
        [1, 0.51763809, 30, 12.13818192],
        [2, 1, 60, 6.28318531],
    ]
    assert np.allclose(actual_do.all_arrays, expected_all_arrays)


def test_all_array_setter(do_minimal):
    do = do_minimal
    with pytest.raises(
        AttributeError,
        match="Direct modification of attribute 'all_arrays' is not allowed. "
        "Please use 'input_data' to modify 'all_arrays'.",
    ):
        do.all_arrays = np.empty((4, 4))


def test_uuid_getter(do_minimal):
    do = do_minimal
    assert hasattr(do, "uuid")
    assert isinstance(do.uuid, UUID)
    assert len(str(do.uuid)) == 36


def test_uuid_getter_with_mock(mocker, do_minimal):
    mocker.patch.object(
        DiffractionObject,
        "uuid",
        new_callable=lambda: UUID("d67b19c6-3016-439f-81f7-cf20a04bee87"),
    )
    do = do_minimal
    assert do.uuid == UUID("d67b19c6-3016-439f-81f7-cf20a04bee87")


def test_uuid_setter_error(do_minimal):
    do = do_minimal

    with pytest.raises(
        AttributeError,
        match=(
            "Direct modification of attribute 'uuid' is not allowed. "
            "Please use 'input_data' to modify 'uuid'."
        ),
    ):
        do.uuid = uuid.uuid4()


def test_xarray_yarray_length_mismatch():
    with pytest.raises(
        ValueError,
        match="'xarray' and 'yarray' are different lengths.  "
        "They must correspond to each other and have the same length. Please "
        "re-initialize 'DiffractionObject'with valid 'xarray' and 'yarray's",
    ):
        DiffractionObject(
            xarray=np.array([1.0, 2.0]),
            yarray=np.array([0.0, 0.0, 0.0]),
            xtype="tth",
            wavelength=1.54,
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


@pytest.mark.parametrize(
    "operation, starting_yarray, scalar_value, expected_yarray",
    [
        # Test scalar addition, subtraction, multiplication, and division to
        # y-values by adding a scalar value
        # C1: Test scalar addition to y-values (intensity), expect no change
        # to x-values (q, tth, d)
        (  # 1. Add 5
            "add",
            np.array([1.0, 2.0]),
            5,
            np.array([6.0, 7.0]),
        ),
        (  # 2. Add 5.1
            "add",
            np.array([1.0, 2.0]),
            5.1,
            np.array([6.1, 7.1]),
        ),
        # C2: Test scalar subtraction to y-values (intensity), expect no
        # change to x-values (q, tth, d)
        (  # 1. Subtract 1
            "sub",
            np.array([1.0, 2.0]),
            1,
            np.array([0.0, 1.0]),
        ),
        (  # 2. Subtract 0.5
            "sub",
            np.array([1.0, 2.0]),
            0.5,
            np.array([0.5, 1.5]),
        ),
        # C3: Test scalar multiplication to y-values (intensity), expect no
        # change to x-values (q, tth, d)
        (  # 1. Multiply by 2
            "mul",
            np.array([1.0, 2.0]),
            2,
            np.array([2.0, 4.0]),
        ),
        (  # 2. Multiply by 2.5
            "mul",
            np.array([1.0, 2.0]),
            2.5,
            np.array([2.5, 5.0]),
        ),
        # C4: Test scalar division to y-values (intensity), expect no change
        # to x-values (q, tth, d)
        (  # 1. Divide by 2
            "div",
            np.array([1.0, 2.0]),
            2,
            np.array([0.5, 1.0]),
        ),
        (  # 2. Divide by 2.5
            "div",
            np.array([1.0, 2.0]),
            2.5,
            np.array([0.4, 0.8]),
        ),
    ],
)
def test_scalar_operations(
    operation, starting_yarray, scalar_value, expected_yarray, do_minimal_tth
):
    do = do_minimal_tth
    expected_xarray_constant = np.array(
        [[0.51763809, 30.0, 12.13818192], [1.0, 60.0, 6.28318531]]
    )
    assert np.allclose(do.all_arrays[:, [1, 2, 3]], expected_xarray_constant)
    assert np.allclose(do.all_arrays[:, 0], starting_yarray)
    if operation == "add":
        do_right_op = do + scalar_value
        do_left_op = scalar_value + do
    elif operation == "sub":
        do_right_op = do - scalar_value
        do_left_op = scalar_value - do
    elif operation == "mul":
        do_right_op = do * scalar_value
        do_left_op = scalar_value * do
    elif operation == "div":
        do_right_op = do / scalar_value
        do_left_op = scalar_value / do
    assert np.allclose(do_right_op.all_arrays[:, 0], expected_yarray)
    assert np.allclose(do_left_op.all_arrays[:, 0], expected_yarray)
    # Ensure x-values are unchanged
    assert np.allclose(
        do_right_op.all_arrays[:, [1, 2, 3]], expected_xarray_constant
    )
    assert np.allclose(
        do_left_op.all_arrays[:, [1, 2, 3]], expected_xarray_constant
    )


@pytest.mark.parametrize(
    (
        "operation, expected_do_1_all_arrays_with_y_modified, "
        "expected_do_2_all_arrays_with_y_modified"
    ),
    [
        # Test addition, subtraction, multiplication, and division of two DO
        # objects
        (  # Test addition of two DO objects, expect combined yarray values
            "add",
            np.array(
                [
                    [2.0, 0.51763809, 30.0, 12.13818192],
                    [4.0, 1.0, 60.0, 6.28318531],
                ]
            ),
            np.array(
                [
                    [2.0, 0.51763809, 30.0, 12.13818192],
                    [4.0, 1.0, 60.0, 6.28318531],
                ]
            ),
        ),
        (  # Test subtraction of two DO objects, expect differences in yarray
            # values
            "sub",
            np.array(
                [
                    [0.0, 0.51763809, 30.0, 12.13818192],
                    [0.0, 1.0, 60.0, 6.28318531],
                ]
            ),
            np.array(
                [
                    [0.0, 0.51763809, 30.0, 12.13818192],
                    [0.0, 1.0, 60.0, 6.28318531],
                ]
            ),
        ),
        (  # Test multiplication of two DO objects, expect multiplication in
            # yarray values
            "mul",
            np.array(
                [
                    [1.0, 0.51763809, 30.0, 12.13818192],
                    [4.0, 1.0, 60.0, 6.28318531],
                ]
            ),
            np.array(
                [
                    [1.0, 0.51763809, 30.0, 12.13818192],
                    [4.0, 1.0, 60.0, 6.28318531],
                ]
            ),
        ),
        (  # Test division of two DO objects, expect division in yarray values
            "div",
            np.array(
                [
                    [1.0, 0.51763809, 30.0, 12.13818192],
                    [1.0, 1.0, 60.0, 6.28318531],
                ]
            ),
            np.array(
                [
                    [1.0, 0.51763809, 30.0, 12.13818192],
                    [1.0, 1.0, 60.0, 6.28318531],
                ]
            ),
        ),
    ],
)
def test_binary_operator_on_do(
    operation,
    expected_do_1_all_arrays_with_y_modified,
    expected_do_2_all_arrays_with_y_modified,
    do_minimal_tth,
):
    do_1 = do_minimal_tth
    do_2 = do_minimal_tth
    assert np.allclose(
        do_1.all_arrays,
        np.array(
            [
                [1.0, 0.51763809, 30.0, 12.13818192],
                [2.0, 1.0, 60.0, 6.28318531],
            ]
        ),
    )
    assert np.allclose(
        do_2.all_arrays,
        np.array(
            [
                [1.0, 0.51763809, 30.0, 12.13818192],
                [2.0, 1.0, 60.0, 6.28318531],
            ]
        ),
    )

    if operation == "add":
        do_1_y_modified = do_1 + do_2
        do_2_y_modified = do_2 + do_1
    elif operation == "sub":
        do_1_y_modified = do_1 - do_2
        do_2_y_modified = do_2 - do_1
    elif operation == "mul":
        do_1_y_modified = do_1 * do_2
        do_2_y_modified = do_2 * do_1
    elif operation == "div":
        do_1_y_modified = do_1 / do_2
        do_2_y_modified = do_2 / do_1

    assert np.allclose(
        do_1_y_modified.all_arrays, expected_do_1_all_arrays_with_y_modified
    )
    assert np.allclose(
        do_2_y_modified.all_arrays, expected_do_2_all_arrays_with_y_modified
    )


def test_operator_invalid_type(do_minimal_tth, invalid_add_type_error_msg):
    # Add a string to a DiffractionObject, expect TypeError
    do = do_minimal_tth
    invalid_value = "string_value"
    operations = [
        (lambda x, y: x + y),  # Test addition
        (lambda x, y: x - y),  # Test subtraction
        (lambda x, y: x * y),  # Test multiplication
        (lambda x, y: x / y),  # Test division
    ]
    for operation in operations:
        with pytest.raises(
            TypeError, match=re.escape(invalid_add_type_error_msg)
        ):
            operation(do, invalid_value)
        with pytest.raises(
            TypeError, match=re.escape(invalid_add_type_error_msg)
        ):
            operation(invalid_value, do)


@pytest.mark.parametrize("operation", ["add", "sub", "mul", "div"])
def test_operator_invalid_xarray_values_not_equal(
    operation, do_minimal_tth, do_minimal_d, x_values_not_equal_error_msg
):
    # Add two DO objects with different xarray values but equal in shape,
    # expect ValueError
    do_1 = do_minimal_tth
    do_2 = do_minimal_d
    with pytest.raises(
        ValueError, match=re.escape(x_values_not_equal_error_msg)
    ):
        if operation == "add":
            do_1 + do_2
        elif operation == "sub":
            do_1 - do_2
        elif operation == "mul":
            do_1 * do_2
        elif operation == "div":
            do_1 / do_2


@pytest.mark.parametrize("operation", ["add", "sub", "mul", "div"])
def test_operator_invalid_xarray_shape_not_equal(
    operation, do_minimal, do_minimal_tth, x_values_not_equal_error_msg
):
    # Add two DO objects with different xarrays shape, expect ValueError
    do_1 = do_minimal
    do_2 = do_minimal_tth
    with pytest.raises(
        ValueError, match=re.escape(x_values_not_equal_error_msg)
    ):
        if operation == "add":
            do_1 + do_2
        elif operation == "sub":
            do_1 - do_2
        elif operation == "mul":
            do_1 * do_2
        elif operation == "div":
            do_1 / do_2
