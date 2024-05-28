.. _Tools Example:

:tocdepth: 2

Tools Example
#############

This example will demonstrate how diffpy.utils allows us to load and manage username and email information.
Using the tools module, we can efficiently handle username and email configurations stored in ``diffpyconfig.json``.

1) To begin, we may create a configuration file ``diffpyconfig.json`` and add username and email to it. ::

    with ("diffpyconfig.json", "w") as f:
        json.dump({"username": "example_username", "email": "example@email.com"}, f)

2) To read the configuration file, we can use the ``load_config`` function,
   which reads a json file and returns its content as a dictionary. ::

    from pathlib import Path
    from diffpy.utils.tools import load_config
    global_config = load_config(Path().home() / "diffpyconfig.json")
    local_config = load_config(Path().cwd() / "diffpyconfig.json")

   If the configuration file does not exist, this function will return ``None``.

3) To clean the configuration dictionary by removing keys with ``None`` values,
   we can use the ``clean_dict`` function. ::

    from diffpy.utils.tools import clean_dict
    cleaned_global_config = clean_dict(global_config)
    cleaned_local_config = clean_dict(local_config)

4) We have the function ``get_user_info`` that integrates all functionalities mentioned above,
   neatly returning a dictionary containing the username and email. ::

    from diffpy.utils.tools import get_user_info
    user_info = get_user_info()

   This function first searches for a configuration file in the current working directory and then the home directory.
   If no configuration files exist, it prompts for user input and creates a configuration file in the home directory.
   You can also override existing values by passing a dictionary to the function. ::

    new_args = {"username": "new_username", "email": "new@example.com"}
    new_user_info = get_user_info(new_args)

   Here, the function returns a dictionary containing the new args.
   Parameters provided to the function override any existing values,
   and values from the current directory file override those in the home directory file.


By using this function, we ensure that user information is correctly loaded, merged, and saved.
