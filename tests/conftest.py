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
def do_minimal():
    # Create an instance of DiffractionObject with minimal setup
    return DiffractionObject(xarray=np.empty(0), yarray=np.empty(0), xtype="tth", wavelength=1.54)
