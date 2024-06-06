.. _Tools Example:

:tocdepth: 2

Tools Example
#############

This example will demonstrate how diffpy.utils allows us to load and manage user and package information.
Using the tools module, we can efficiently get them in terms of a dictionary.

1) We have the function ``get_user_info`` that neatly returns a dictionary containing the username and email.
   You can use this function without arguments. ::

    from diffpy.utils.tools import get_user_info
    user_info = get_user_info()

   This function will first attempt to load configuration files
   from both the current working directory and the home directory.
   If no configuration files exist, it prompts for user input and creates a configuration file in the home directory.
   It prioritizes prompted user inputs, then current working directory, and finally home directory.
   If no configuration files or inputs are found, this function creates a configuration in the home directory
   with empty values for username and email stored as a dictionary.

2) You can also override existing values by passing a dictionary to the function. ::

    new_args = {"username": "new_username", "email": "new@example.com"}
    new_user_info = get_user_info(new_args)

   Here, the function returns a dictionary containing the new arguments.
   If no configuration files exist, it prompts for inputs again. The arguments passed here also override input values.
   The updated arguments will not be saved in files.

   You can update only the username or email individually, for example ::

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
    package_metadata = get_package_info("diffpy.utils")

   You can also specify a specific metadata dictionary to store the information. ::

    existing_dict = {"key": "value"}
    existing_dict.update(get_package_info("diffpy.utils", metadata=existing_dict))

   In this case, the function inserts the package info into ``existing_dict``.

   If you want to specify package other than "diffpy.utils",
   "diffpy.utils" is automatically included in the package info. ::

    existing_dict.update(get_package_info("new_package", metadata=existing_dict))

   The package info will then contain information for both "diffpy.utils" and "new_package".

4) We can also use ``get_package_info`` with diffraction objects to update the package information. ::

    from diffpy.utils.scattering_objects.diffraction_objects import Diffraction_object
    example = Diffraction_object()
    example.metadata.update(get_package_info("diffpy.utils", metadata=example.metadata))

By using this module, we ensure that user and package information is correctly loaded, merged, and saved.
