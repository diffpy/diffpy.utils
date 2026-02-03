import pytest

from diffpy.utils._deprecator import deprecated, deprecation_message

old_base = "diffpy.utils"
old_name = "oldFunction"
new_name = "new_function"
removal_version = "4.0.0"

dep_msg = deprecation_message(old_base, old_name, new_name, removal_version)


@deprecated(dep_msg)
def oldFunction(print_msg):
    """This function is deprecated and will be removed in version 4.0.0.

    Please use newFunction instead
    """
    return new_function(print_msg)


def new_function(print_msg):
    print(print_msg)
    return


def test_deprecated(capsys):
    # Case: user deprecates a function with the deprecated decorator
    # Expected: DeprecationWarning is raised when the function is called
    #           and the function executes correctly
    expected_print_msg = "Testing deprecated function"
    with pytest.deprecated_call(match=dep_msg):
        oldFunction(expected_print_msg)
    captured = capsys.readouterr()
    actual_print_msg = captured.out.strip()
    assert actual_print_msg == expected_print_msg
