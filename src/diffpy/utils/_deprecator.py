import functools
import warnings

# Deprecated decorator is available for Python 3.13+, once
# Support for earlier versions is dropped, this custom
# implementation can be removed.
try:
    from warnings import deprecated as _builtin_deprecated
except ImportError:
    _builtin_deprecated = None


def deprecated(message, *, category=DeprecationWarning, stacklevel=1):
    """Deprecation decorator for functions and classes that is
    compatible with Python versions prior to 3.13.

    Examples
    --------
    Basic usage with a deprecated function:

    .. code-block:: python

        from diffpy._deprecations import deprecated, deprecation_message

        deprecation_warning = build_deprecation_message("diffpy.utils",
                                                        "old_function",
                                                        "new_function",
                                                        "4.0.0")

        @deprecated(deprecation_warning)
        def old_function(x, y):
            '''This function is deprecated and will be removed in version
            4.0.0. Please use new_function instead'''
            return new_function(x, y)

        def new_function(x, y):
            return x + y

        old_function(1, 2)   # Works but emits DeprecationWarning
        new_function(1, 2)   # Works, no warning


    Deprecating a class:

    .. code-block:: python

        from diffpy._deprecations import deprecated, deprecation_message

        deprecation_warning = build_deprecation_message("diffpy.utils",
                                                        "OldAtom",
                                                        "NewAtom",
                                                        "4.0.0")

        @deprecated(deprecation_warning)
        class OldAtom:
            def __new__(cls, *args, **kwargs):
                warnings.warn(
                    "OldAtom is deprecated and will be removed in
                    version 4.0.0. Use NewClass instead.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                return NewAtom(*args, **kwargs)

        class NewAtom:
            def __init__(self, symbol):
                self.symbol = symbol

        a = OldAtom("C")     # Works but emits DeprecationWarning
        b = NewAtom("C")     # Works with no warning
    """
    if _builtin_deprecated is not None:
        return _builtin_deprecated(
            message, category=category, stacklevel=stacklevel
        )
    if not isinstance(message, str):
        raise TypeError(
            f"Expected an object of type str for 'message', not "
            f"{type(message).__name__!r}"
        )

    def decorator(obj):
        setattr(obj, "__deprecated__", message)
        if callable(obj):

            @functools.wraps(obj)
            def wrapper(*args, **kwargs):
                warnings.warn(message, category, stacklevel=stacklevel + 1)
                return obj(*args, **kwargs)

            return wrapper
        raise TypeError(
            "deprecated decorator can only be applied to functions or classes"
        )

    return decorator


def build_deprecation_message(
    old_base, old_name, new_name, removal_version, new_base=None
):
    """Generate a deprecation message.

    Parameters
    ----------
    old_base : str
        The base module or class where the deprecated item resides.
        This will look like the import statement used in the code
        currently
    old_name : str
        The name of the deprecated item.
    new_name : str
        The name of the new item to use.
    removal_version : str
        The version when the deprecated item will be removed.
    new_base : str Optional. Defaults to old_base.
        The base module or class where the new item resides.
        This will look like the import statement that
        will be used in the code moving forward. If not specified,
        the new base defaults to the old one.

    Returns
    -------
    str
        A formatted deprecation message.
    """
    if new_base is None:
        new_base = old_base
    return (
        f"'{old_base}.{old_name}' is deprecated and will be removed in "
        f"version {removal_version}. Please use '{new_base}.{new_name}' "
        f"instead."
    )


def generate_deprecation_docstring(new_name, removal_version, new_base=None):
    """Generate a docstring for copy-pasting into a deprecated function.

    this function will print the text to the terminal for copy-pasting

    usage:
      python
      >>> import diffpy.utils._deprecator.generate_deprecation_docstring as gdd
      >>> gdd("new_name", "4.0.0")

    The message looks like:
      This function has been deprecated and will be removed in version
      {removal_version}. Please use  {new_base}.{new_name} instead.

    Parameters
    ----------
    new_name: str
        The name of the new function or class to replace the existing one
    removal_version: str
        The version when the deprecated item is targeted for removal,
        e.g., 4.0.0
    new_base: str Optional. Defaults to old_base.
        The new base for importing.  The new import statement would look like
        "from new_base import new_name"

    Returns
    -------
    None
    """
    print(
        f"This function has been deprecated and will be "
        f"removed in version {removal_version}. Please use"
        f"{new_base}.{new_name} instead."
    )
    return
