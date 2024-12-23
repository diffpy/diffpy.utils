.. _Tools Utility:

Tools Utility
=============

The ``diffpy.utils.tools`` module provides tool functions for use with diffpy apps.

- ``get_user_info()``: This function is designed for managing and tracking user information (name, email, orcid).
  Developers can use this function to simplify the process of loading, merging, and saving information consistently and easily.
  Additionally, it saves the effort of re-entering information, and allows overriding current information by
  passing parameters.

- ``check_and_build_global_config()``: This function helps create a global configuration file
  that can be used by, for example, ``get_user_info()``.
  If no existing configuration file is found, this function prompts for information.
  The provided inputs are then saved to a global configuration file.
  This file can be reused later by ``get_user_info()`` to ensure that the work credits and user information are consistently stored.

- ``get_package_info()``: This function loads package name and version information into a dictionary.
  It updates the package information under the key "package_info" in the format {"package_name": "version_number"},
  resulting in an entry in the passed metadata dictionary that looks like
  ``{"package_info": {"package1": "version_number1", "package2": "version_number2"}`` if the function is called more than
  once.

  Users can use these functions to track and manage versions of packages that can later be stored, for example, in an output
  file header.

For a more in-depth tutorial for how to use these tools, click :ref:`here <Tools Example>`.
