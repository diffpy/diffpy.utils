.. _Tools Utility:

:tocdepth: 2

Tools Utility
#############

The ``diffpy.utils.tools`` module provides tool functions for use with diffpy apps.

1) ``get_uder_info``: This function is designed for managing and tracking username and email information.
It helps to store this data in a ``diffpyconfig.json`` file.

Users can use this function to simplify the process of loading, merging, and saving information consistently and easily.
Additionally, it saves the effort of re-entering information, and allows overriding current information by
passing parameters.

2) ``get_package_info``: This function loads package name and version information into a dictionary.
It stores the package information under the key "package_info" in the format {"package_name": "version_number"}.

Users can use this function to track and manage dependencies, ensuring the correct packages and versions were used.
