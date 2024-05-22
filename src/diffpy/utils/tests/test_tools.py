import json
import os
import re
from pathlib import Path

import pytest

from diffpy.utils.scattering_objects.tools import get_user_info

params_user_info_without_conf_file = [
    (["new_username", "new@email.com"], ["new_username", "new@email.com", "new_username", "new@email.com"]),
]


@pytest.mark.parametrize("inputs, expected", params_user_info_without_conf_file)
def test_load_user_info_without_conf_file(monkeypatch, inputs, expected, user_filesystem):
    expected_username, expected_email, expected_conf_username, expected_conf_email = expected

    os.chdir(user_filesystem)
    input_user = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_user))
    monkeypatch.setattr("diffpy.utils.scattering_objects.user_config.HOME_CONFIG_PATH", user_filesystem / "diffpyconfig.json")

    actual_username, actual_email = get_user_info()
    assert actual_username == expected_username
    assert actual_email == expected_email
    with open(user_filesystem / "diffpyconfig.json", "r") as f:
        config_data = json.load(f)
        assert config_data == {"username": expected_conf_username, "email": expected_conf_email}


params_user_info_with_conf_file = [
    (["", ""], ["good_username", "good@email.com", "good_username", "good@email.com"]),
    (["new_username", ""], ["new_username", "good@email.com", "good_username", "good@email.com"]),
    (["", "new@email.com"], ["good_username", "new@email.com", "good_username", "good@email.com"]),
    (["new_username", "new@email.com"], ["new_username", "new@email.com", "good_username", "good@email.com"]),
]


@pytest.mark.parametrize("inputs, expected", params_user_info_with_conf_file)
def test_load_user_info_with_conf_file(monkeypatch, inputs, expected, user_filesystem):
    expected_username, expected_email, expected_conf_username, expected_conf_email = expected
    user_config_data = {"username": "good_username", "email": "good@email.com"}
    with open(user_filesystem / "diffpyconfig.json", "w") as f:
        json.dump(user_config_data, f)

    # test it works when config file is in current directory
    # check username and email are correctly loaded and config file is not modified
    os.chdir(user_filesystem / "conf_dir")
    input_user = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_user))
    monkeypatch.setattr("diffpy.utils.scattering_objects.user_config.HOME_CONFIG_PATH", user_filesystem / "diffpyconfig.json")

    actual_username, actual_email = get_user_info()
    assert actual_username == expected_username
    assert actual_email == expected_email
    with open(Path.cwd() / "diffpyconfig.json", "r") as f:
        config_data = json.load(f)
        assert config_data == {"username": expected_conf_username, "email": expected_conf_email}

    # test it works when config file is in home directory and not in current directory new_dir
    # check username and email are correctly loaded and config file is not modified
    new_dir = user_filesystem / "new_dir"
    new_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(new_dir)
    input_user = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_user))

    actual_username, actual_email = get_user_info()
    assert actual_username == expected_username
    assert actual_email == expected_email
    with open(user_filesystem / "diffpyconfig.json", "r") as f:
        config_data = json.load(f)
        assert config_data == {"username": expected_conf_username, "email": expected_conf_email}


params_user_info_bad = [
    # No valid username/email in config file (or no config file),
    # and user didn't enter username/email the first time they were asked
    (["", ""], "Please rerun the program and provide a username and email."),
    (["", "good@email.com"], "Please rerun the program and provide a username."),
    (["good_username", ""], "Please rerun the program and provide an email."),
    # User entered an invalid email
    (["good_username", "bad_email"], "Please rerun the program and provide a valid email."),
]


@pytest.mark.parametrize("inputs, msg", params_user_info_bad)
def test_load_user_info_bad(monkeypatch, inputs, msg, user_filesystem):
    os.chdir(user_filesystem)
    input_user = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_user))
    monkeypatch.setattr("diffpy.utils.scattering_objects.user_config.HOME_CONFIG_PATH", user_filesystem / "diffpyconfig.json")

    with pytest.raises(ValueError, match=msg[0]):
        actual_username, actual_email = get_user_info()
