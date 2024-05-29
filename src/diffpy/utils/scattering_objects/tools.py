from pathlib import Path

from diffpy.utils.scattering_objects.user_config import (
    prompt_user_info,
    read_conf_file,
    write_conf_file,
)


def get_user_info():
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
    input_username, input_email = prompt_user_info()
    conf_username, conf_email = read_conf_file()

    no_username = not input_username and not conf_username
    no_email = not input_email and not conf_email
    if no_username and no_email:
        raise ValueError("Please rerun the program and provide a username and email.")
    if no_username:
        raise ValueError("Please rerun the program and provide a username.")
    if no_email:
        raise ValueError("Please rerun the program and provide an email.")

    username = input_username or conf_username
    email = input_email or conf_email
    if "@" not in email:
        raise ValueError("Please rerun the program and provide a valid email.")

    if not conf_username and not conf_email:
        write_conf_file(username, email)
    return username, email
