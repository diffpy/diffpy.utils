.. _Tools Example:

:tocdepth: 2

Tools Example
#############

This example will demonstrate how diffpy.utils allows us to conveniently load and manage user and package information.
Using the tools module, we can efficiently get them in terms of a dictionary.

1) We have the function ``get_user_info`` that neatly returns a dictionary containing the username and email.
   You can use this function without arguments. ::

    from diffpy.utils.tools import get_user_info
    user_info = get_user_info()

   This function will first attempt to load the information from configuration files looking first in
   the current working directory and then in the user's home directory.
   If no configuration files exist, it prompts for user input and creates a configuration file in the home directory
   so that the next time the program is run it will no longer have to prompt the user.
   It can be passed user information which overrides looking in config files, and so could be passed
   information that is entered through a gui or command line interface to override default information at runtime.
   It prioritizes prompted user inputs, then current working directory config file, and finally home directory config file.

   The function returns a dictionary containing the username and email information.

2) You can also override existing values by passing a dictionary to the function with the keys `"username"` and `"email"` ::

    new_args = {"username": "new_username", "email": "new@example.com"}
    new_user_info = get_user_info(new_args)

3) You can update only the username or email individually, for example ::

    new_username = {"username": new_username}
    new_user_info = get_user_info(new_username)

   This updates username to "new_username" while fetching the email from inputs or the configuration files.
   Similarly, you can update only the email. ::

    new_email = {"email": new@email.com}
    new_user_info = get_user_info(new_email)

   This updates the email to "new@email.com" while fetching the username from inputs or the configuration files.

3) We also have the function ``get_package_info``, which inserts or updates package names and versions
   in the given metadata dictionary under the key "package_info".
   It stores the package information as {"package_info": {"package_name": "version_number"}}.
   This function can be used as follows. ::

    from diffpy.utils.tools import get_user_info
    package_metadata = get_package_info("my_package")

   You can also specify an existing dictionary to be updated with the information. ::

    existing_dict = {"key": "value"}
    updated_dict = get_package_info("my_package", metadata=existing_dict))

    note that `"diffpy.utils"` is automatically included in the package info since the `get_user_info` function is
    part of diffpy.utils. 
