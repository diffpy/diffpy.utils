.. _Tools Utility:

:tocdepth: 2

Tools Utility
#############

The ``diffpy.utils.tools`` module provides tool functions for use with diffpy apps.

1) ``get_uder_info``: This function is designed for managing and tracking username and email information.

Developers can use this function to simplify the process of loading, merging, and saving information consistently and easily.
Additionally, it saves the effort of re-entering information, and allows overriding current information by
passing parameters.

2) ``get_package_info``: This function loads package name and version information into a dictionary.
It updates the package information under the key "package_info" in the format {"package_name": "version_number"},
resulting in an entry in the passed metadata dictionary that looks like
`{"package_info": {"package1": "version_number1", "package2": "version_number2"} if the function is called more than
once.

Users can use these functions to track and manage versions of packages that can later be stored, for example, in an output 
file header. 
