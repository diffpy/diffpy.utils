.. _Tools Example:

:tocdepth: -1

Tools Example
#############

The tools module contains various tools that may be useful when you manipulate and analyze diffraction data.

Automatically Capture User Info
===============================

One task we would like to do is to capture and propagate useful metadata that describes the diffraction data.
Some is essential such as wavelength and radiation type. Other metadata is useful such as information about the
sample, co-workers and so on.  However, one of the most important bits of information is the name of the data owner.
For example, in ``DiffractionObjects`` this is stored in the ``metadata`` dictionary as ``username``, ``user_email``,
and ``user_orcid``.

To reduce experimenter overhead when collecting this information, we have developed an infrastructure that helps
to capture this information automatically when you are using `DiffractionObjects` and other diffpy tools.
You may also reuse this infrastructure for your own projects using tools in this tutorial.

This example will demonstrate how ``diffpy.utils`` allows us to conveniently load and manage user and package information.
Using the tools module, we can efficiently get them in terms of a dictionary.

Load user info into your program
--------------------------------

To use this functionality in your own code make use of the ``get_user_info`` function in
``diffpy.utils.tools`` which will search for information about the user, parse it, and return
it in a dictionary object e.g. if the user is "Jane Doe" with email "janedoe@gmail.com" and the
function can find the information, if you type this

.. code-block:: python

    from diffpy.utils.tools import get_user_info
    user_info = get_user_info()

The function will return

.. code-block:: python

        {"email": "janedoe@email.com", "username": "Jane Doe"}


Where does ``get_user_info()`` get the user information from?
-------------------------------------------------------------

The function will first attempt to load the information from configuration files with the name ``diffpyconfig.json``
on your hard-drive.
It looks first for the file in the current working directory.  If it cannot find it there it will look
user's home, i.e., login, directory.  To find this directory, open a terminal and a unix or mac system type ::

    cd ~
    pwd

Or type ``Echo $HOME``.  On a Windows computer ::

    echo %USERPROFILE%"

What if no config files exist yet?
-----------------------------------

If no configuration files can be found, the function attempts to create one in the user's home
directory.  The function will pause execution and ask for a user-response to enter the information.
It will then write the config file in the user's home directory.

In this way, the next, and subsequent times the program is run, it will no longer have to prompt the user
as it will successfully find the new config file.

Getting user data with no config files and with no interruption of execution
----------------------------------------------------------------------------

If you would like get run ``get_user_data()`` but without execution interruption even if it cannot find
an input file, type

.. code-block:: python

    user_data = get_user_data(skip_config_creation=True)

Passing user information directly to ``get_user_data()``
--------------------------------------------------------

It can be passed user information which fully or partially overrides looking in config files
For example, in this way it would be possible to pass in information
that is entered through a gui or command line interface. E.g.,

    .. code-block:: python

        new_user_info = get_user_info({"username": "new_username", "email": "new@example.com"})

This returns ``{"username": "new_username", "email": "new@example.com"}`` (and so, effectively, does nothing)
However, You can update only the username or email individually, for example

.. code-block:: python

        new_user_info = get_user_info({"username": new_username})

will return ``{"username": "new_username", "email": "janedoe@gmail.com"}``
if it found ``janedoe@gmail.com`` as the email in the config file.
Similarly, you can update only the email in the returned dictionary,

.. code-block:: python

        new_user_info = get_user_info({"email": new@email.com})

which will return ``{"username": "Jane Doe", "email": "new@email.com"}``
if it found ``Jane Doe`` as the user in the config file.

I entered the wrong information in my config file so it always loads incorrect information
------------------------------------------------------------------------------------------

You can use of the above methods to temporarily override the incorrect information in your
global config file. However, it is easy to fix this simply by editing that file using a text
editor.

Locate the file ``diffpyconfig.json``, in your home directory and open it in an editor ::

    {
        "username": "John Doe",
        "email": "john.doe@example.com"
    }

   Then you can edit the username and email as needed, make sure to save your edits.

Automatically Capture Info about a Software Package Being Used
==============================================================

We also have a handy tool for capturing information about a python package that is being used
to save in the metadata.  To use this functionality, use he function ``get_package_info``, which
inserts or updates software package names and versions in a given metadata dictionary under
the key "package_info", e.g.,

.. code-block:: python

    {"package_info": {"diffpy.utils": "0.3.0", "my_package": "0.3.1"}}

If the installed version of the package "my_package" is 0.3.1.

This function can be used in your code as follows

.. code-block:: python

    from diffpy.utils.tools import get_package_info
    package_metadata = get_package_info("my_package")

or

.. code-block:: python

    package_metadata = get_package_info(["first_package", "second_package"])

which returns (for example)

.. code-block:: python

    {"package_info": {"diffpy.utils": "0.3.0", "first_package": "1.0.1", "second_package": "0.0.7"}}


You can also specify an existing dictionary to be updated with the information.

.. code-block:: python

    existing_dict = {"key": "value"}
    updated_dict = get_package_info("my_package", metadata=existing_dict))

Which returns

.. code-block:: python

    {"key": "value", "package_info": {"diffpy.utils": "0.3.0", "my_package": "0.3.1"}}


Note that ``"diffpy.utils"`` is automatically included in the package info since the ``get_user_info`` function is
part of ``diffpy.utils``.
