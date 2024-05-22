import json
from pathlib import Path

import pytest


@pytest.fixture
def user_filesystem(tmp_path):
    base_dir = Path(tmp_path)
    conf_dir = base_dir / "conf_dir"
    conf_dir.mkdir(parents=True, exist_ok=True)

    user_config_data = {"username": "good_username", "email": "good@email.com"}
    with open(conf_dir / "diffpyconfig.json", "w") as f:
        json.dump(user_config_data, f)

    yield tmp_path
