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
    """Compatibility wrapper for Python <3.13.

    Matches the Python 3.13 warnings.deprecated API exactly.
    """
    # If Python 3.13 implementation exists, delegate to it
    if _builtin_deprecated is not None:
        return _builtin_deprecated(
            message, category=category, stacklevel=stacklevel
        )

    # Validate message type like Python 3.13 does
    if not isinstance(message, str):
        raise TypeError(
            f"Expected an object of type str for 'message', not "
            f"{type(message).__name__!r}"
        )

    def decorator(obj):
        # Set __deprecated__ attribute (required by PEP 702)
        setattr(obj, "__deprecated__", message)

        # Must support functions AND classes
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
