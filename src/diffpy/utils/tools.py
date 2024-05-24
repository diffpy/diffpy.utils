import json
from copy import copy
from pathlib import Path

def clean_dict(obj):
    obj = obj if obj is not None else {}
    for key, value in copy(obj).items():
        if not value:
            del obj[key]
    return obj

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
    global_config = load_config(Path().home() / "diffpyconfig.json" )
    local_config = load_config(Path().cwd() / "diffpyconfig.json" )

    config = _sorted_merge(clean_dict(global_config), clean_dict(local_config), clean_dict(args))

    return config
    # # trigger create global config flow only we don't find any config file
    # if global_config is None and local_config is None:
    #     _create_global_config(args)
    # conf_username, conf_email = read_conf_file()
    #
    # no_username = not input_username and not conf_username
    # no_email = not input_email and not conf_email
    # if no_username and no_email:
    #     raise ValueError("Please rerun the program and provide a username and email.")
    # if no_username:
    #     raise ValueError("Please rerun the program and provide a username.")
    # if no_email:
    #     raise ValueError("Please rerun the program and provide an email.")
    #
    # username = input_username or conf_username
    # email = input_email or conf_email
    # if "@" not in email:
    #     raise ValueError("Please rerun the program and provide a valid email.")
    #
    # if not conf_username and not conf_email:
    #     write_conf_file(username, email)
    # return username, email
