import importlib.metadata
import json
from copy import copy
from pathlib import Path

user_info_imsg = (
    "No global configuration file was found containing "
    "information about the user to associate with the data.\n"
    "By following the prompts below you can add your name and email to this file on the current "
    "computer and your name will be automatically associated with subsequent diffpy data by default.\n"
    "This is not recommended on a shared or public computer. "
    "You will only have to do that once.\n"
    "For more information, please refer to www.diffpy.org/diffpy.utils/examples/toolsexample.html."
)


def _clean_dict(obj):
    """
    Remove keys from the dictionary where the corresponding value is None.

    Parameters
    ----------
    obj: dict
        The dictionary to clean. If None, initialize as an empty dictionary.

    Returns
    -------
    dict:
        The cleaned dictionary with keys removed where the value is None.

    """
    obj = obj if obj is not None else {}
    for key, value in copy(obj).items():
        if not value:
            del obj[key]
    return obj


def _stringify(obj):
    """
    Convert None to an empty string.

    Parameters
    ----------
    obj: str
        The object to convert. If None, return an empty string.

    Returns
    -------
    str or None:
        The converted string if obj is not None, otherwise an empty string.
    """
    return obj if obj is not None else ""


def _load_config(file_path):
    """
    Load configuration from a .json file.

    Parameters
    ----------
    file_path: Path
        The path to the configuration file.

    Returns
    -------
    dict:
        The configuration dictionary or None if file does not exist.

    """
    config_file = Path(file_path).resolve()
    if config_file.is_file():
        with open(config_file, "r") as f:
            config = json.load(f)
        return config
    else:
        return None


def _sorted_merge(*dicts):
    merged = {}
    for d in dicts:
        d = _clean_dict(d)
        merged.update(d)
    return merged


def _get_config_info(user_info):
    global_config = _load_config(Path().home() / "diffpyconfig.json")
    local_config = _load_config(Path().cwd() / "diffpyconfig.json")
    if global_config or local_config:
        return _sorted_merge(global_config, local_config, user_info)
    return None


def _create_global_config(user_info):
    print(user_info_imsg)
    username = input(
        f"Please enter the name you would want future work to be credited to "
        f"[{user_info.get('username', '')}]:  "
    ).strip() or user_info.get("username", "")
    email = input(f"Please enter the your email " f"[{user_info.get('email', '')}]:  ").strip() or user_info.get(
        "email", ""
    )
    config = {"username": _stringify(username), "email": _stringify(email)}
    if username and email:
        with open(Path().home() / "diffpyconfig.json", "w") as f:
            f.write(json.dumps(config))
        print(
            f"You can manually edit the config file at "
            f"{Path().home() / 'diffpyconfig.json'} using any text editor.\n"
            f"Or you can update the config file by passing new values to get_user_info(), "
            f"see examples here: https://www.diffpy.org/diffpy.utils/examples/toolsexample.html."
        )
    return config


def get_user_info(user_info=None, skip_config_creation=False):
    """
    Retrieve or create user configuration (username and email).

    Workflow:
    1. Loads config from global and local paths, prioritizing user_info, then local, then global.
    2. If no config files are found and skip_config_creation is False, prompts the user for input.
       Creates a global config file only if both username and email are valid.
    3. If no config files and skip_config_creation is True, uses user_info (even if empty).

    Parameters
    ----------
    user_info dict or None
        A dictionary containing the user input, default is None.

    Returns
    -------
    dict or None:
        The dictionary containing username and email with corresponding values.
    """
    config = _get_config_info(user_info)
    if config:
        return config
    if not skip_config_creation:
        return _create_global_config(user_info)
    return {
        "username": _stringify(user_info.get("username", "")),
        "email": _stringify(user_info.get("email", "")),
    }


def get_package_info(package_names, metadata=None):
    """
    Fetches package version and updates it into (given) metadata.

    Package info stored in metadata as {'package_info': {'package_name': 'version_number'}}.

    ----------
    package_name : str or list
        The name of the package(s) to retrieve the version number for.
    metadata : dict
        The dictionary to store the package info. If not provided, a new dictionary will be created.

    Returns
    -------
    dict:
        The updated metadata dict with package info inserted.

    """
    if metadata is None:
        metadata = {}
    if isinstance(package_names, str):
        package_names = [package_names]
    package_names.append("diffpy.utils")
    pkg_info = metadata.get("package_info", {})
    for package in package_names:
        pkg_info.update({package: importlib.metadata.version(package)})
    metadata["package_info"] = pkg_info
    return metadata
