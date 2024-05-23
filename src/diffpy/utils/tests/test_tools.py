import json
import os
import re
from pathlib import Path

import pytest

from diffpy.utils.scattering_objects.tools import get_user_info

# Helper test function
def _test_user_info(monkeypatch, cwd, inputs, expected, user_filesystem, no_conf_file=False, expect_error=False, error_msg=None):
    # Determine paths
    cwd_path = user_filesystem / cwd
    home_dir = user_filesystem / "home_dir"
    cwd_config_path = cwd_path / "diffpyconfig.json"
    home_config_path = home_dir / "diffpyconfig.json"

    # Set monkeypatch attributes
    input_user = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_user))
    monkeypatch.setattr("diffpy.utils.scattering_objects.user_config.CWD_CONFIG_PATH", cwd_config_path)
    monkeypatch.setattr("diffpy.utils.scattering_objects.user_config.HOME_CONFIG_PATH", home_config_path)

    # Handle no configuration file
    if no_conf_file:
        os.remove(home_dir / "diffpyconfig.json")
    # Change directory to specified cwd
    os.chdir(user_filesystem / cwd)

    # Perform the test
    if expect_error:
        with pytest.raises(ValueError, match=error_msg):
            get_user_info()
    else:
        actual_username, actual_email = get_user_info()
        expected_username, expected_email, expected_conf_folder, expected_conf_username, expected_conf_email = expected
        assert actual_username == expected_username
        assert actual_email == expected_email

        expected_conf_path = (user_filesystem / expected_conf_folder) / "diffpyconfig.json"
        with open(expected_conf_path, "r") as f:
            config_data = json.load(f)
            assert config_data == {"username": expected_conf_username, "email": expected_conf_email}

params_user_info_with_conf_file = [
    # No cwd config file, only home config file
    ("new_dir", ["", ""], ["home_username", "home@email.com", "home_dir", "home_username", "home@email.com"]),
    ("new_dir", ["input_username", ""], ["input_username", "home@email.com", "home_dir", "home_username", "home@email.com"]),
    ("new_dir", ["", "input@email.com"], ["home_username", "input@email.com", "home_dir", "home_username", "home@email.com"]),
    ("new_dir", ["input_username", "input@email.com"],
     ["input_username", "input@email.com", "home_dir", "home_username", "home@email.com"]),

    # There exists valid cwd config file
    ("cwd_dir", ["", ""], ["cwd_username", "cwd@email.com", "cwd_dir", "cwd_username", "cwd@email.com"]),
    ("cwd_dir", ["input_username", ""], ["input_username", "cwd@email.com", "cwd_dir", "cwd_username", "cwd@email.com"]),
    ("cwd_dir", ["", "input@email.com"], ["cwd_username", "input@email.com", "cwd_dir", "cwd_username", "cwd@email.com"]),
    ("cwd_dir", ["input_username", "input@email.com"],
     ["input_username", "input@email.com", "cwd_dir", "cwd_username", "cwd@email.com"]),
]

params_user_info_without_conf_file = [
    ("new_dir", ["input_username", "input@email.com"], ["input_username", "input@email.com", "home_dir", "input_username", "input@email.com"]),
]

params_user_info_bad = [
    ("new_dir", ["", ""], "Please rerun the program and provide a username and email."),
    ("new_dir", ["", "input@email.com"], "Please rerun the program and provide a username."),
    ("new_dir", ["input_username", ""], "Please rerun the program and provide an email."),
    ("new_dir", ["input_username", "bad_email"], "Please rerun the program and provide a valid email."),
]

@pytest.mark.parametrize("cwd, inputs, expected", params_user_info_with_conf_file)
def test_load_user_info_with_conf_file(monkeypatch, cwd, inputs, expected, user_filesystem):
    _test_user_info(monkeypatch, cwd, inputs, expected, user_filesystem)

@pytest.mark.parametrize("cwd, inputs, expected", params_user_info_without_conf_file)
def test_load_user_info_without_conf_file(monkeypatch, cwd, inputs, expected, user_filesystem):
    _test_user_info(monkeypatch, cwd, inputs, expected, user_filesystem, no_conf_file=True)

@pytest.mark.parametrize("cwd, inputs, msg", params_user_info_bad)
def test_load_user_info_bad(monkeypatch, cwd, inputs, msg, user_filesystem):
    _test_user_info(monkeypatch, cwd, inputs, None, user_filesystem, no_conf_file=True, expect_error=True, error_msg=msg)
