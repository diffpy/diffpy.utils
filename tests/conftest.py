import json
from pathlib import Path

import numpy as np
import pytest

from diffpy.utils.diffraction_objects import DiffractionObject


@pytest.fixture
def user_filesystem(tmp_path):
    base_dir = Path(tmp_path)
    home_dir = base_dir / "home_dir"
    home_dir.mkdir(parents=True, exist_ok=True)
    cwd_dir = home_dir / "cwd_dir"
    cwd_dir.mkdir(parents=True, exist_ok=True)
    home_config_data = {
        "owner_name": "home_ownername",
        "owner_email": "home@email.com",
        "owner_orcid": "home_orcid",
    }
    with open(home_dir / "diffpyconfig.json", "w") as f:
        json.dump(home_config_data, f)
    yield home_dir, cwd_dir


@pytest.fixture
def datafile():
    """Fixture to dynamically load any test file."""
    base_path = Path(__file__).parent / "testdata"  # Adjusted base path

    def _load(filename):
        return base_path / filename

    return _load


@pytest.fixture
def do_minimal():
    # Create an instance of DiffractionObject with empty xarray and yarray
    # values, and a non-empty wavelength
    return DiffractionObject(
        xarray=np.empty(0), yarray=np.empty(0), xtype="tth", wavelength=1.54
    )


@pytest.fixture
def do_minimal_tth():
    # Create an instance of DiffractionObject with non-empty xarray, yarray,
    # and wavelength values
    return DiffractionObject(
        wavelength=2 * np.pi,
        xarray=np.array([30, 60]),
        yarray=np.array([1, 2]),
        xtype="tth",
    )


@pytest.fixture
def do_minimal_d():
    # Create an instance of DiffractionObject with non-empty xarray, yarray,
    # and wavelength values
    return DiffractionObject(
        wavelength=1.54,
        xarray=np.array([1, 2]),
        yarray=np.array([1, 2]),
        xtype="d",
    )


@pytest.fixture
def wavelength_warning_msg():
    return (
        "No wavelength has been specified. You can continue to use the "
        "DiffractionObject, but some of its powerful features will not be "
        "available. "
        "To specify a wavelength, if you have "
        "do = DiffractionObject(xarray, yarray, 'tth'), "
        "you may set do.wavelength = 1.54 for a wavelength of 1.54 angstroms."
    )


@pytest.fixture
def invalid_q_or_d_or_wavelength_error_msg():
    return (
        "The supplied input array and wavelength will result in an "
        "impossible two-theta. "
        "Please check these values and re-instantiate the DiffractionObject "
        "with correct values."
    )


@pytest.fixture
def invalid_add_type_error_msg():
    return (
        "You may only add a DiffractionObject with another DiffractionObject "
        "or a scalar value. "
        "Please rerun by adding another DiffractionObject instance or a "
        "scalar value. "
        "e.g., my_do_1 + my_do_2 or my_do + 10 or 10 + my_do"
    )


@pytest.fixture
def x_values_not_equal_error_msg():
    return (
        "The two objects have different values in x arrays "
        "(my_do.all_arrays[:, [1, 2, 3]]). "
        "Please ensure the x values of the two objects are identical "
        "by re-instantiating the DiffractionObject with the correct x value "
        "inputs."
    )
