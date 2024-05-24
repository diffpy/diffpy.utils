import json
import os
from copy import copy
from pathlib import Path

def clean_dict(obj):
    obj = obj if obj is not None else {}
    for key, value in copy(obj).items():
        if not value:
            del obj[key]
    return obj

def stringify(obj):
    return obj if obj is not None else ""

def load_config(file_path):
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
    username = input(f"Please enter the name of the user to put in the diffpy global config file "
                     f"[{args.get("username", "")}]:  ").strip() or args.get("username", "")
    email = input(f"Please enter the email of the user to put in the diffpy global config file "
                     f"[{args.get("email", "")}]:  ").strip() or args.get("email", "")
    return_bool = False if username is None or email is None else True
    with open(Path().home() / "diffpyconfig.json", "w") as f:
        f.write(json.dumps({"username": stringify(username), "email": stringify(email)}))
    return return_bool

def get_user_info(args=None):
    """
    Get username and email.

    Prompt the user to enter username and email.
    If not provided, read from the config file (first from cwd, and then from home directory).
    If neither are available, raise a ValueError.
    Save provided values to the config file if a config file doesn't exist.

    Parameters
    ----------
    args argparse.Namespace
        the arguments from the parser

    Returns
    -------
    two strings on username and email

    """
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
