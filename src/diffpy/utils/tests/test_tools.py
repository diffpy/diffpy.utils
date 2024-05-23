import json
import os
import re
from pathlib import Path

import pytest

from diffpy.utils.scattering_objects.tools import get_user_info


params_user_info_with_conf_file = [
    (["", ""], ["home_username", "home@email.com", "cwd_username", "cwd@email.com"]),
    (["input_username", ""], ["input_username", "home@email.com", "input_username", "cwd@email.com"]),
    (["", "input@email.com"], ["home_username", "input@email.com", "cwd_username", "input@email.com"]),
    (["input_username", "input@email.com"], ["input_username", "input@email.com", "input_username", "input@email.com"]),
]
@pytest.mark.parametrize("inputs, expected", params_user_info_with_conf_file)
def test_load_user_info_with_conf_file(monkeypatch, inputs, expected, user_filesystem):
    expected_username_home, expected_email_home, expected_username_cwd, expected_email_cwd = expected
    home_dir = user_filesystem / "home_dir"
    cwd_dir = user_filesystem / "cwd_dir"

    # conf file is in home directory, not in cwd
    input_user = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_user))
    monkeypatch.setattr("diffpy.utils.scattering_objects.user_config.CWD_CONFIG_PATH", cwd_dir / "diffpyconfig.json")
    monkeypatch.setattr("diffpy.utils.scattering_objects.user_config.HOME_CONFIG_PATH", home_dir / "diffpyconfig.json")
    actual_username, actual_email = get_user_info()
    assert actual_username == expected_username_home
    assert actual_email == expected_email_home

    # conf file is in cwd
    cwd_username, cwd_email = "cwd_username", "cwd@email.com"
    with open(cwd_dir / "diffpyconfig.json", "w") as f:
        json.dump({"username": cwd_username, "email": cwd_email}, f)
    input_user = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_user))
    actual_username, actual_email = get_user_info()
    assert actual_username == expected_username_cwd
    assert actual_email == expected_email_cwd


params_user_info_without_conf_file = [
    (["new_username", "new@email.com"], ["new_username", "new@email.com", "new_username", "new@email.com"]),
]
@pytest.mark.parametrize("inputs, expected", params_user_info_without_conf_file)
def test_load_user_info_without_conf_file(monkeypatch, inputs, expected, user_filesystem):
    expected_username, expected_email, expected_conf_username, expected_conf_email = expected
    home_dir = user_filesystem / "home_dir"
    cwd_dir = user_filesystem / "cwd_dir"
    os.remove(home_dir / "diffpyconfig.json")
    input_user = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_user))
    monkeypatch.setattr("diffpy.utils.scattering_objects.user_config.CWD_CONFIG_PATH", cwd_dir / "diffpyconfig.json")
    monkeypatch.setattr("diffpy.utils.scattering_objects.user_config.HOME_CONFIG_PATH", user_filesystem / "diffpyconfig.json")

    actual_username, actual_email = get_user_info()
    assert actual_username == expected_username
    assert actual_email == expected_email
    with open(user_filesystem / "diffpyconfig.json", "r") as f:
        config_data = json.load(f)
        assert config_data == {"username": expected_conf_username, "email": expected_conf_email}


params_user_info_bad = [
    # Invalid inputs
    (["input_username", "bad_email"], "Please rerun the program and provide a valid email."),
    # Skipped inputs when there is no valid conf file
    (["", ""], "Please rerun the program and provide a username and email."),
    (["", "input@email.com"], "Please rerun the program and provide a username."),
    (["input_username", ""], "Please rerun the program and provide an email."),
]
@pytest.mark.parametrize("inputs, msg", params_user_info_bad)
def test_load_user_info_bad(monkeypatch, inputs, msg, user_filesystem):
    home_dir = user_filesystem / "home_dir"
    cwd_dir = user_filesystem / "cwd_dir"
    os.remove(home_dir / "diffpyconfig.json")
    input_user = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_user))
    monkeypatch.setattr("diffpy.utils.scattering_objects.user_config.CWD_CONFIG_PATH", cwd_dir / "diffpyconfig.json")
    monkeypatch.setattr("diffpy.utils.scattering_objects.user_config.HOME_CONFIG_PATH", home_dir / "diffpyconfig.json")
    with pytest.raises(ValueError, match=msg[0]):
        get_user_info()


params_user_info_invalid_conf_files = [
    # Invalid conf files
    # Test first invalid home conf file, then invalid cwd conf file
    (["input_username", "input@email.com"], "Please provide a configuration file with username and email."),
]
@pytest.mark.parametrize("inputs, msg", params_user_info_invalid_conf_files)
def test_load_user_info_invalid_conf_files(monkeypatch, inputs, msg, user_filesystem):
    home_dir = user_filesystem / "home_dir"
    cwd_dir = user_filesystem / "cwd_dir"
    os.remove(home_dir / "diffpyconfig.json")
    with open(home_dir / "diffpyconfig.json", "w") as f:
        json.dump({}, f)
    input_user = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_user))
    monkeypatch.setattr("diffpy.utils.scattering_objects.user_config.CWD_CONFIG_PATH", cwd_dir / "diffpyconfig.json")
    monkeypatch.setattr("diffpy.utils.scattering_objects.user_config.HOME_CONFIG_PATH", home_dir / "diffpyconfig.json")
    with pytest.raises(ValueError, match=msg[0]):
        get_user_info()

    with open(cwd_dir / "diffpyconfig.json", "w") as f:
        json.dump({}, f)
    input_user = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_user))
    with pytest.raises(ValueError, match=msg[0]):
        get_user_info()
