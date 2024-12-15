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
    cwd_dir = base_dir / "cwd_dir"
    cwd_dir.mkdir(parents=True, exist_ok=True)

    home_config_data = {"username": "home_username", "email": "home@email.com"}
    with open(home_dir / "diffpyconfig.json", "w") as f:
        json.dump(home_config_data, f)

    yield tmp_path


@pytest.fixture
def datafile():
    """Fixture to dynamically load any test file."""
    base_path = Path(__file__).parent / "testdata"  # Adjusted base path

    def _load(filename):
        return base_path / filename

    return _load


@pytest.fixture
def do_minimal_tth():
    return DiffractionObject(wavelength=2 * np.pi, xarray=np.array([30, 60]), yarray=np.array([1, 2]), xtype="tth")


@pytest.fixture
def wavelength_warning_msg():
    return (
        "No wavelength has been specified. You can continue to use the DiffractionObject, but "
        "some of its powerful features will not be available. "
        "To specify a wavelength, if you have do = DiffractionObject(xarray, yarray, 'tth'), "
        "you may set do.wavelength = 1.54 for a wavelength of 1.54 angstroms."
    )
