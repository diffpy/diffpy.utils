import importlib.metadata
import json
import os
from pathlib import Path

import pytest

from diffpy.utils.tools import check_and_build_global_config, get_package_info, get_user_info

# def _setup_dirs(monkeypatch, user_filesystem):
#     home_dir, cwd_dir = user_filesystem.home_dir, user_filesystem.cwd_dir
#     os.chdir(cwd_dir)
#     return home_dir
#


def _run_tests(inputs, expected):
    args = {"username": inputs[0], "email": inputs[1]}
    expected_username, expected_email = expected
    config = get_user_info(args)
    assert config.get("username") == expected_username
    assert config.get("email") == expected_email


params_user_info_with_local_conf_file = [
    (["", ""], ["cwd_username", "cwd@email.com"]),
    (["cli_username", ""], ["cli_username", "cwd@email.com"]),
    (["", "cli@email.com"], ["cwd_username", "cli@email.com"]),
    ([None, None], ["cwd_username", "cwd@email.com"]),
    (["cli_username", None], ["cli_username", "cwd@email.com"]),
    ([None, "cli@email.com"], ["cwd_username", "cli@email.com"]),
    (["cli_username", "cli@email.com"], ["cli_username", "cli@email.com"]),
]
params_user_info_with_no_home_conf_file = [
    (
        [None, None],
        ["input_username", "input@email.com"],
        ["input_username", "input@email.com"],
    ),
    (
        ["cli_username", None],
        ["", "input@email.com"],
        ["cli_username", "input@email.com"],
    ),
    (
        [None, "cli@email.com"],
        ["input_username", ""],
        ["input_username", "cli@email.com"],
    ),
    (
        ["", ""],
        ["input_username", "input@email.com"],
        ["input_username", "input@email.com"],
    ),
    (
        ["cli_username", ""],
        ["", "input@email.com"],
        ["cli_username", "input@email.com"],
    ),
    (
        ["", "cli@email.com"],
        ["input_username", ""],
        ["input_username", "cli@email.com"],
    ),
    (
        ["cli_username", "cli@email.com"],
        ["input_username", "input@email.com"],
        ["cli_username", "cli@email.com"],
    ),
]
params_user_info_no_conf_file_no_inputs = [
    ([None, None], ["", ""], ["", ""]),
]


@pytest.mark.parametrize(
    "runtime_inputs, expected",
    [  # config file in home is present, no config in cwd.  various runtime values passed
        # C1: nothing passed in, expect uname, email, orcid from home_config
        ({}, {"owner_name": "home_ownername", "owner_email": "home@email.com", "owner_orcid": "home_orcid"}),
        # C2: empty strings passed in, expect uname, email, orcid from home_config
        (
            {"owner_name": "", "owner_email": "", "owner_orcid": ""},
            {"owner_name": "home_ownername", "owner_email": "home@email.com", "owner_orcid": "home_orcid"},
        ),
        # C3: just owner name passed in at runtime.  expect runtime_oname but others from config
        (
            {"owner_name": "runtime_ownername"},
            {"owner_name": "runtime_ownername", "owner_email": "home@email.com", "owner_orcid": "home_orcid"},
        ),
        # C4: just owner email passed in at runtime.  expect runtime_email but others from config
        (
            {"owner_email": "runtime@email.com"},
            {"owner_name": "home_ownername", "owner_email": "runtime@email.com", "owner_orcid": "home_orcid"},
        ),
        # C5: just owner ci passed in at runtime.  expect runtime_orcid but others from config
        (
            {"owner_orcid": "runtime_orcid"},
            {"owner_name": "home_ownername", "owner_email": "home@email.com", "owner_orcid": "runtime_orcid"},
        ),
    ],
)
def test_get_user_info_with_home_conf_file(runtime_inputs, expected, user_filesystem, mocker):
    # user_filesystem[0] is tmp_dir/home_dir with the global config file in it, user_filesystem[1]
    #   is tmp_dir/cwd_dir
    mocker.patch.object(Path, "home", return_value=user_filesystem[0])
    os.chdir(user_filesystem[1])
    actual = get_user_info(**runtime_inputs)
    assert actual == expected


@pytest.mark.parametrize(
    "runtime_inputs, expected",
    [  # tests as before but now config file present in cwd and home but orcid
        #   missing in the cwd config
        # C1: nothing passed in, expect uname, email from local config, orcid from home_config
        ({}, {"owner_name": "cwd_ownername", "owner_email": "cwd@email.com", "owner_orcid": "home_orcid"}),
        # C2: empty strings passed in, expect uname, email, orcid from home_config
        (
            {"owner_name": "", "owner_email": "", "owner_orcid": ""},
            {"owner_name": "cwd_ownername", "owner_email": "cwd@email.com", "owner_orcid": "home_orcid"},
        ),
        # C3: just owner name passed in at runtime.  expect runtime_oname but others from config
        (
            {"owner_name": "runtime_ownername"},
            {"owner_name": "runtime_ownername", "owner_email": "cwd@email.com", "owner_orcid": "home_orcid"},
        ),
        # C4: just owner email passed in at runtime.  expect runtime_email but others from config
        (
            {"owner_email": "runtime@email.com"},
            {"owner_name": "cwd_ownername", "owner_email": "runtime@email.com", "owner_orcid": "home_orcid"},
        ),
        # C5: just owner ci passed in at runtime.  expect runtime_orcid but others from config
        (
            {"owner_orcid": "runtime_orcid"},
            {"owner_name": "cwd_ownername", "owner_email": "cwd@email.com", "owner_orcid": "runtime_orcid"},
        ),
    ],
)
def test_get_user_info_with_local_conf_file(runtime_inputs, expected, user_filesystem, mocker):
    # user_filesystem[0] is tmp_dir/home_dir with the global config file in it, user_filesystem[1]
    #   is tmp_dir/cwd_dir
    mocker.patch.object(Path, "home", return_value=user_filesystem[0])
    os.chdir(user_filesystem[1])
    local_config_data = {"owner_name": "cwd_ownername", "owner_email": "cwd@email.com"}
    with open(user_filesystem[1] / "diffpyconfig.json", "w") as f:
        json.dump(local_config_data, f)
    actual = get_user_info(**runtime_inputs)
    assert actual == expected


# @pytest.mark.parametrize("inputsa, inputsb, expected", params_user_info_with_no_home_conf_file)
# def test_get_user_info_with_no_home_conf_file(monkeypatch, inputsa, inputsb, expected, user_filesystem):
#     _setup_dirs(monkeypatch, user_filesystem)
#     os.remove(Path().home() / "diffpyconfig.json")
#     inp_iter = iter(inputsb)
#     monkeypatch.setattr("builtins.input", lambda _: next(inp_iter))
#     _run_tests(inputsa, expected)
#     confile = Path().home() / "diffpyconfig.json"
#     assert confile.is_file()
#
#
# @pytest.mark.parametrize("inputsa, inputsb, expected", params_user_info_no_conf_file_no_inputs)
# def test_get_user_info_no_conf_file_no_inputs(monkeypatch, inputsa, inputsb, expected, user_filesystem):
#     _setup_dirs(monkeypatch, user_filesystem)
#     os.remove(Path().home() / "diffpyconfig.json")
#     inp_iter = iter(inputsb)
#     monkeypatch.setattr("builtins.input", lambda _: next(inp_iter))
#     _run_tests(inputsa, expected)
#     confile = Path().home() / "diffpyconfig.json"
#     assert confile.exists() is False
#


@pytest.mark.parametrize(
    "test_inputs,expected",
    [  # Check check_and_build_global_config() builds correct config when config is found missing
        (  # C1: user inputs valid name, email and orcid
            {"user_inputs": ["input_name", "input@email.com", "input_orcid"]},
            {"owner_email": "input@email.com", "owner_orcid": "input_orcid", "owner_name": "input_name"},
        ),
        # (  # C2: empty strings passed in, expect uname, email, orcid from home_config
        #     {"owner_name": "", "owner_email": "", "owner_orcid": ""},
        #     {"owner_name": "home_ownername", "owner_email": "home@email.com", "owner_orcid": "home_orcid"},
        # ),
    ],
)
def test_check_and_build_global_config(test_inputs, expected, user_filesystem, mocker):
    # user_filesystem[0] is tmp_dir/home_dir with the global config file in it, user_filesystem[1]
    #   is tmp_dir/cwd_dir
    mocker.patch.object(Path, "home", return_value=user_filesystem[0])
    os.chdir(user_filesystem[1])
    # remove the config file from home that came with user_filesystem
    old_confile = user_filesystem[0] / "diffpyconfig.json"
    os.remove(old_confile)
    check_and_build_global_config()
    inp_iter = iter(test_inputs["user_inputs"])
    mocker.patch("builtins.input", lambda _: next(inp_iter))
    with open(old_confile, "r") as f:
        actual = json.load(f)
    print(actual)
    assert actual == expected


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
