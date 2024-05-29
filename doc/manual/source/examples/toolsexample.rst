.. _Tools Example:

:tocdepth: 2

Tools Example
#############

This example will demonstrate how diffpy.utils allows us to load and manage username and email information.
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


By using this function, we ensure that user information is correctly loaded, merged, and saved.
