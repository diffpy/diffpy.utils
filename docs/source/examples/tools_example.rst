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
For example, in ``DiffractionObjects`` this is stored in the ``metadata`` dictionary as ``owner_name``, ``owner_email``,
and ``owner_orcid``.

To reduce experimenter overhead when collecting this information, we have developed an infrastructure that helps
to capture this information automatically when you are using ``DiffractionObjects`` and other diffpy tools.
You may also reuse this infrastructure for your own projects using tools in this tutorial.

This example will demonstrate how ``diffpy.utils`` allows us to conveniently load and manage user and package information.
Using the tools module, we can efficiently get them in terms of a dictionary.

Load user info into your program
--------------------------------

To use this functionality in your own code make use of the ``get_user_info`` function in
``diffpy.utils.tools`` which will search for information about the user, parse it, and return
it in a dictionary object e.g. if the user is "Jane Doe" with email "janedoe@gmail.com" and ORCID
"0000-0000-0000-0000", and if the
function can find the information (more on this below), if you type this

.. code-block:: python

    from diffpy.utils.tools import get_user_info
    user_info = get_user_info()

The function will return

.. code-block:: python

    {"owner_name": "Jane Doe", "owner_email": "janedoe@email.com", "owner_orcid": "0000-0000-0000-0000"}


Where does ``get_user_info()`` get the user information from?
-------------------------------------------------------------

The function will first attempt to load the information from configuration files with the name ``diffpyconfig.json``
on your hard-drive.
It looks for files in the current working directory and in the computer-user's home (i.e., login) directory.
For example, it might be in C:/Users/yourname`` or something like that, but to find this directory, open
a terminal and a unix or mac system type ::

    cd ~
    pwd

Or type ``Echo $HOME``.  On a Windows computer ::

    echo %USERPROFILE%"

It is also possible to override the values in the config files at run-time by passing values directly into the
function according to ``get_user_info``, for example,
``get_user_info(owner_name="Janet Doe", owner_email="janetdoe@email.com", owner_orcid="1111-1111-1111-1111")``.
The information to pass into ``get_user_info`` could be entered by a user through a command-line interface
or into a gui.

What if no config files exist yet?
-----------------------------------

If no configuration files can be found, they can be created using a text editor, or by using a diffpy tool
called ``check_and_build_global_config()`` which, if no global config file can be found, prompts the user for the
information then writes the config file in the user's home directory.

When building an application where you want to capture data-owner information, we recommend you execute
``check_and_build_global_config()`` first followed by ``get_user_info`` in your app workflow.  E.g.,

.. code-block:: python

    from diffpy.utils.tools import check_and_build_global_config, get_user_info
    from datetime import datetime
    import json

    def my_cool_data_enhancer_app_main(data, filepath):
        check_and_build_global_config()
        metadata_enhanced_data = get_user_info()
        metadata_enhanced_data.update({"creation_time": datetime.now(),
                                       "data": data})
        with open(filepath, "w") as f:
            json.dump(metadata_enhanced_data, f)

``check_and_build_global_config()`` only
interrupts execution if it can't find a valid config file, and so if the user enters valid information
it will only run once.  However, if you want to bypass this behavior,
``check_and_build_global_config()`` takes an optional boolean ``skip_config_creation`` parameter that
could be set to ``True`` at runtime to override the config creation.

What happens when you run ``check_and_build_global_config()``?
--------------------------------------------------------------

When you set ``skip_config_creation`` to ``False`` and there is no existing global configuration file,
the function will prompt you for inputs (name, email, ORCID).
An example of the prompts you may see is:

.. code-block:: python

    Please enter the name you would want future work to be credited to: Jane Doe
    Please enter your email: janedoe@example.com
    Please enter your orcid ID if you know it: 0000-0000-0000-0000


After receiving the inputs, the function will write the information to
the `diffpyconfig.json` file in your home directory.


``check_and_build_global_config()`` returns ``True`` if the config file exists (whether it created it or not)
and ``False`` if the config file does not exist in the user's home allowing you to develop your own
workflow for handling missing config files after running it with ``skip_config_creation=True``.

I entered the wrong information in my config file so it always loads incorrect information, how do I fix that?
--------------------------------------------------------------------------------------------------------------

It is easy to fix this simply by deleting the global and/or local config files, which will allow
you to re-enter the information during the ``check_and_build_global_config()`` initialization
workflow.   You can also simply edit the ``diffpyconfig.json`` file directly using a text
editor.

Locate the file ``diffpyconfig.json``, in your home directory and open it in an editor ::

    {
        "owner_name": "John Doe",
        "owner_email": "john.doe@example.com"
        "owner_orcid": "0000-0000-4321-1234"
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
