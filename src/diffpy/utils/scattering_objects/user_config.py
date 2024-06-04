import json
from pathlib import Path

CONFIG_FILE = "diffpyconfig.json"
CWD_CONFIG_PATH = Path.cwd() / CONFIG_FILE
HOME_CONFIG_PATH = Path.home() / CONFIG_FILE


def find_conf_file():
    if CWD_CONFIG_PATH.exists() and CWD_CONFIG_PATH.is_file():
        return CWD_CONFIG_PATH
    elif HOME_CONFIG_PATH.exists() and HOME_CONFIG_PATH.is_file():
        return HOME_CONFIG_PATH
    return None


def read_conf_file():
    conf_file = find_conf_file()
    if conf_file:
        with open(conf_file, "r") as f:
            config = json.load(f)
            if not config.get("username") or not config.get("email"):
                raise ValueError("Please provide a configuration file with username and email.")
            return config.get("username"), config.get("email")
    return None, None


def write_conf_file(username, email):
    with open(HOME_CONFIG_PATH, "w") as f:
        json.dump({"username": username, "email": email}, f)
