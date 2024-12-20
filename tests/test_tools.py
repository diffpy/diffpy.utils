import importlib.metadata
import json
import os
from pathlib import Path

import pytest

from diffpy.utils.tools import get_package_info, get_user_info


def _setup_dirs(monkeypatch, user_filesystem):
    cwd = Path(user_filesystem)
    home_dir = cwd / "home_dir"
    monkeypatch.setattr("pathlib.Path.home", lambda _: home_dir)
    os.chdir(cwd)
    return home_dir


def _run_tests(cli_inputs, expected):
    user_info = {"username": cli_inputs["cli_username"], "email": cli_inputs["cli_email"]}
    config = get_user_info(user_info=user_info, skip_config_creation=cli_inputs["skip_config_creation"])
    expected_username = expected["expected_username"]
    expected_email = expected["expected_email"]
    assert config.get("username") == expected_username
    assert config.get("email") == expected_email


params_user_info_with_home_conf_file = [
    (
        {"skip_config_creation": False, "cli_username": None, "cli_email": None},
        {"expected_username": "home_username", "expected_email": "home@email.com"},
    ),
    (
        {"skip_config_creation": False, "cli_username": "cli_username", "cli_email": None},
        {"expected_username": "cli_username", "expected_email": "home@email.com"},
    ),
    (
        {"skip_config_creation": False, "cli_username": None, "cli_email": "cli@email.com"},
        {"expected_username": "home_username", "expected_email": "cli@email.com"},
    ),
    (
        {"skip_config_creation": False, "cli_username": "cli_username", "cli_email": "cli@email.com"},
        {"expected_username": "cli_username", "expected_email": "cli@email.com"},
    ),
    (
        {"skip_config_creation": True, "cli_username": None, "cli_email": None},
        {"expected_username": "home_username", "expected_email": "home@email.com"},
    ),
    (
        {"skip_config_creation": True, "cli_username": "cli_username", "cli_email": None},
        {"expected_username": "cli_username", "expected_email": "home@email.com"},
    ),
    (
        {"skip_config_creation": True, "cli_username": None, "cli_email": "cli@email.com"},
        {"expected_username": "home_username", "expected_email": "cli@email.com"},
    ),
    (
        {"skip_config_creation": True, "cli_username": "cli_username", "cli_email": "cli@email.com"},
        {"expected_username": "cli_username", "expected_email": "cli@email.com"},
    ),
]
params_user_info_with_local_conf_file = [
    (
        {"skip_config_creation": False, "cli_username": None, "cli_email": None},
        {"expected_username": "cwd_username", "expected_email": "cwd@email.com"},
    ),
    (
        {"skip_config_creation": False, "cli_username": "cli_username", "cli_email": None},
        {"expected_username": "cli_username", "expected_email": "cwd@email.com"},
    ),
    (
        {"skip_config_creation": False, "cli_username": None, "cli_email": "cli@email.com"},
        {"expected_username": "cwd_username", "expected_email": "cli@email.com"},
    ),
    (
        {"skip_config_creation": False, "cli_username": "cli_username", "cli_email": "cli@email.com"},
        {"expected_username": "cli_username", "expected_email": "cli@email.com"},
    ),
    (
        {"skip_config_creation": True, "cli_username": None, "cli_email": None},
        {"expected_username": "cwd_username", "expected_email": "cwd@email.com"},
    ),
    (
        {"skip_config_creation": True, "cli_username": "cli_username", "cli_email": None},
        {"expected_username": "cli_username", "expected_email": "cwd@email.com"},
    ),
    (
        {"skip_config_creation": True, "cli_username": None, "cli_email": "cli@email.com"},
        {"expected_username": "cwd_username", "expected_email": "cli@email.com"},
    ),
    (
        {"skip_config_creation": True, "cli_username": "cli_username", "cli_email": "cli@email.com"},
        {"expected_username": "cli_username", "expected_email": "cli@email.com"},
    ),
]
params_user_info_with_no_conf_file = [
    # Case 1: no inputs, do not create config files
    (
        {"skip_config_creation": False, "cli_username": None, "cli_email": None},
        {"input_username": "", "input_email": ""},
        {"expected_username": "", "expected_email": "", "config_file_exists": False},
    ),
    # Case 2: One input (username / email) and the other is empty, do not create config file
    (
        {"skip_config_creation": False, "cli_username": "cli_username", "cli_email": None},
        {"input_username": "", "input_email": ""},
        {"expected_username": "cli_username", "expected_email": "", "config_file_exists": False},
    ),
    (
        {"skip_config_creation": False, "cli_username": None, "cli_email": "cli@email.com"},
        {"input_username": "", "input_email": ""},
        {"expected_username": "", "expected_email": "cli@email.com", "config_file_exists": False},
    ),
    (
        {"skip_config_creation": False, "cli_username": None, "cli_email": None},
        {"input_username": "input_username", "input_email": ""},
        {"expected_username": "input_username", "expected_email": "", "config_file_exists": False},
    ),
    (
        {"skip_config_creation": False, "cli_username": None, "cli_email": None},
        {"input_username": "", "input_email": "input@email.com"},
        {"expected_username": "", "expected_email": "input@email.com", "config_file_exists": False},
    ),
    (
        {"skip_config_creation": False, "cli_username": "cli_username", "cli_email": None},
        {"input_username": "input_username", "input_email": ""},
        {"expected_username": "input_username", "expected_email": "", "config_file_exists": False},
    ),
    (
        {"skip_config_creation": False, "cli_username": None, "cli_email": "cli@email.com"},
        {"input_username": "", "input_email": "input@email.com"},
        {"expected_username": "", "expected_email": "input@email.com", "config_file_exists": False},
    ),
    # Case 2: Both inputs, create global config file
    (
        {"skip_config_creation": False, "cli_username": "cli_username", "cli_email": "cli@email.com"},
        {"input_username": "", "input_email": ""},
        {"expected_username": "cli_username", "expected_email": "cli@email.com", "config_file_exists": True},
    ),
    (
        {"skip_config_creation": False, "cli_username": "cli_username", "cli_email": None},
        {"input_username": "", "input_email": "input@email.com"},
        {"expected_username": "cli_username", "expected_email": "input@email.com", "config_file_exists": True},
    ),
    (
        {"skip_config_creation": False, "cli_username": None, "cli_email": "cli@email.com"},
        {"input_username": "input_username", "input_email": ""},
        {"expected_username": "input_username", "expected_email": "cli@email.com", "config_file_exists": True},
    ),
    (
        {"skip_config_creation": False, "cli_username": None, "cli_email": None},
        {"input_username": "input_username", "input_email": "input@email.com"},
        {"expected_username": "input_username", "expected_email": "input@email.com", "config_file_exists": True},
    ),
    (
        {"skip_config_creation": False, "cli_username": "cli_username", "cli_email": "cli@email.com"},
        {"input_username": "input_username", "input_email": "input@email.com"},
        {"expected_username": "input_username", "expected_email": "input@email.com", "config_file_exists": True},
    ),
]
params_user_info_no_conf_file_no_inputs = [
    (
        {"skip_config_creation": True, "cli_username": None, "cli_email": None},
        {"expected_username": "", "expected_email": ""},
    ),
    (
        {"skip_config_creation": True, "cli_username": "cli_username", "cli_email": None},
        {"expected_username": "cli_username", "expected_email": ""},
    ),
    (
        {"skip_config_creation": True, "cli_username": None, "cli_email": "cli@email.com"},
        {"expected_username": "", "expected_email": "cli@email.com"},
    ),
    (
        {"skip_config_creation": True, "cli_username": "cli_username", "cli_email": "cli@email.com"},
        {"expected_username": "cli_username", "expected_email": "cli@email.com"},
    ),
]


@pytest.mark.parametrize("cli_inputs, expected", params_user_info_with_home_conf_file)
def test_get_user_info_with_home_conf_file(monkeypatch, cli_inputs, expected, user_filesystem):
    _setup_dirs(monkeypatch, user_filesystem)
    _run_tests(cli_inputs, expected)


@pytest.mark.parametrize("cli_inputs, expected", params_user_info_with_local_conf_file)
def test_get_user_info_with_local_conf_file(monkeypatch, cli_inputs, expected, user_filesystem):
    _setup_dirs(monkeypatch, user_filesystem)
    local_config_data = {"username": "cwd_username", "email": "cwd@email.com"}
    with open(Path(user_filesystem) / "diffpyconfig.json", "w") as f:
        json.dump(local_config_data, f)
    _run_tests(cli_inputs, expected)
    # Run tests again without global config, results should be the same
    os.remove(Path().home() / "diffpyconfig.json")
    _run_tests(cli_inputs, expected)


@pytest.mark.parametrize("cli_inputs, inputs, expected", params_user_info_with_no_conf_file)
def test_get_user_info_with_no_conf_file(monkeypatch, cli_inputs, inputs, expected, user_filesystem):
    _setup_dirs(monkeypatch, user_filesystem)
    os.remove(Path().home() / "diffpyconfig.json")
    inp_iter = iter([inputs["input_username"], inputs["input_email"]])
    monkeypatch.setattr("builtins.input", lambda _: next(inp_iter))
    _run_tests(cli_inputs, expected)
    confile = Path().home() / "diffpyconfig.json"
    assert confile.is_file() == expected["config_file_exists"]


@pytest.mark.parametrize("cli_inputs, expected", params_user_info_no_conf_file_no_inputs)
def test_get_user_info_no_conf_file_no_inputs(monkeypatch, cli_inputs, expected, user_filesystem):
    _setup_dirs(monkeypatch, user_filesystem)
    os.remove(Path().home() / "diffpyconfig.json")
    _run_tests(cli_inputs, expected)
    confile = Path().home() / "diffpyconfig.json"
    assert confile.exists() is False


params_package_info = [
    (["diffpy.utils", None], {"package_info": {"diffpy.utils": "3.3.0"}}),
    (["package1", None], {"package_info": {"package1": "1.2.3", "diffpy.utils": "3.3.0"}}),
    (["package1", {"thing1": 1}], {"thing1": 1, "package_info": {"package1": "1.2.3", "diffpy.utils": "3.3.0"}}),
    (
        ["package1", {"package_info": {"package1": "1.1.0", "package2": "3.4.5"}}],
        {"package_info": {"package1": "1.2.3", "package2": "3.4.5", "diffpy.utils": "3.3.0"}},
    ),
]


@pytest.mark.parametrize("inputs, expected", params_package_info)
def test_get_package_info(monkeypatch, inputs, expected):
    monkeypatch.setattr(
        importlib.metadata, "version", lambda package_name: "3.3.0" if package_name == "diffpy.utils" else "1.2.3"
    )
    actual_metadata = get_package_info(inputs[0], metadata=inputs[1])
    assert actual_metadata == expected
