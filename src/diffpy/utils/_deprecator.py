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
    """Deprecation decorator for functions and classes that is compatible with
    Python versions prior to 3.13."""
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
