import importlib.metadata
import json
import os
from copy import copy
from pathlib import Path


def clean_dict(obj):
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


def stringify(obj):
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


def load_config(file_path):
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
        merged.update(d)
    return merged


def _create_global_config(args):
    username = input(
        f"Please enter the name of the user to put in the diffpy global config file "
        f"[{args.get('username', '')}]:  "
    ).strip() or args.get("username", "")
    email = input(
        f"Please enter the email of the user to put in the diffpy global config file "
        f"[{args.get('email', '')}]:  "
    ).strip() or args.get("email", "")
    return_bool = False if username is None or email is None else True
    with open(Path().home() / "diffpyconfig.json", "w") as f:
        f.write(json.dumps({"username": stringify(username), "email": stringify(email)}))
    return return_bool


def get_user_info(args=None):
    """
    Get username and email configuration.

    First attempts to load config file from global and local paths.
    If neither exists, creates a global config file.
    It prioritizes values from args, then local, then global.
    Removes invalid global config file if creation is needed, replacing it with empty username and email.

    Parameters
    ----------
    args argparse.Namespace
        The arguments from the parser, default is None.

    Returns
    -------
    dict or None:
        The dictionary containing username and email with corresponding values.

    """
    config_bool = True
    global_config = load_config(Path().home() / "diffpyconfig.json")
    local_config = load_config(Path().cwd() / "diffpyconfig.json")
    if global_config is None and local_config is None:
        config_bool = _create_global_config(args)
        global_config = load_config(Path().home() / "diffpyconfig.json")
    config = _sorted_merge(clean_dict(global_config), clean_dict(local_config), clean_dict(args))
    if config_bool is False:
        os.remove(Path().home() / "diffpyconfig.json")
        config = {"username": "", "email": ""}

    return config


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
