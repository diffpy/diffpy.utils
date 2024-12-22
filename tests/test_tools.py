import importlib.metadata
import json
import os
from pathlib import Path

import pytest

from diffpy.utils.tools import check_and_build_global_config, get_package_info, get_user_info


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


@pytest.mark.parametrize(
    "test_inputs,expected",
    [  # Check check_and_build_global_config() builds correct config when config is found missing
        (  # C1: user inputs valid name, email and orcid
            {"user_inputs": ["input_name", "input@email.com", "input_orcid"]},
            {"owner_email": "input@email.com", "owner_orcid": "input_orcid", "owner_name": "input_name"},
        ),
        ({"user_inputs": ["", "", ""]}, None),  # C2: empty strings passed in, expect no config file created
        (  # C3: just username input, expect config file but with some empty values
            {"user_inputs": ["input_name", "", ""]},
            {"owner_email": "", "owner_orcid": "", "owner_name": "input_name"},
        ),
    ],
)
def test_check_and_build_global_config(test_inputs, expected, user_filesystem, mocker):
    # user_filesystem[0] is tmp_dir/home_dir with the global config file in it, user_filesystem[1]
    #   is tmp_dir/cwd_dir
    mocker.patch.object(Path, "home", return_value=user_filesystem[0])
    os.chdir(user_filesystem[1])
    confile = user_filesystem[0] / "diffpyconfig.json"
    # remove the config file from home that came with user_filesystem
    os.remove(confile)
    mocker.patch("builtins.input", side_effect=test_inputs["user_inputs"])
    check_and_build_global_config()
    try:
        with open(confile, "r") as f:
            actual = json.load(f)
    except FileNotFoundError:
        actual = None
    assert actual == expected


def test_check_and_build_global_config_file_exists(user_filesystem, mocker):
    mocker.patch.object(Path, "home", return_value=user_filesystem[0])
    os.chdir(user_filesystem[1])
    confile = user_filesystem[0] / "diffpyconfig.json"
    expected = {"owner_name": "home_ownername", "owner_email": "home@email.com", "owner_orcid": "home_orcid"}
    check_and_build_global_config()
    with open(confile, "r") as f:
        actual = json.load(f)
    assert actual == expected


def test_check_and_build_global_config_skipped(user_filesystem, mocker):
    mocker.patch.object(Path, "home", return_value=user_filesystem[0])
    os.chdir(user_filesystem[1])
    confile = user_filesystem[0] / "diffpyconfig.json"
    # remove the config file from home that came with user_filesystem
    os.remove(confile)
    check_and_build_global_config(skip_config_creation=True)
    assert not confile.exists()


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
