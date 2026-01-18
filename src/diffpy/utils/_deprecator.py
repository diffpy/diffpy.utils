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

        from diffpy.utils._deprecator import deprecated
        import warnings

        @deprecated("old_function is deprecated; use new_function instead")
        def old_function(x, y):
            return x + y

        def new_function(x, y):
            return x + y

        old_function(1, 2)   # Emits DeprecationWarning
        new_function(1, 2)   # No warning


    Deprecating a class:

    .. code-block:: python

        from diffpy._deprecations import deprecated

        warnings.simplefilter("always", DeprecationWarning)

        @deprecated("OldAtom is deprecated; use NewAtom instead")
        class OldAtom:
            def __init__(self, symbol):
                self.symbol = symbol

        class NewAtom:
            def __init__(self, symbol):
                self.symbol = symbol

        a = OldAtom("C")     # Emits DeprecationWarning
        b = NewAtom("C")     # No warning
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


def deprecation_message(
    base, old_name, new_name, removal_version, new_base=None
):
    """Generate a deprecation message.

    Parameters
    ----------
    base : str
        The base module or class where the deprecated item resides.
    old_name : str
        The name of the deprecated item.
    new_name : str
        The name of the new item to use.
    removal_version : str
        The version when the deprecated item will be removed.

    Returns
    -------
    str
        A formatted deprecation message.
    """
    if new_base is None:
        new_base = base
    return (
        f"'{base}.{old_name}' is deprecated and will be removed in "
        f"version {removal_version}. Please use '{new_base}.{new_name}' "
        f"instead."
    )


_DEPRECATION_DOCSTRING_TEMPLATE = (
    "This function has been deprecated and will be "
    "removed in version {removal_version}. Please use"
    "{new_base}.{new_name} instead."
)
