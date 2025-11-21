import functools
import warnings

# Deprecated decorator is available for Python 3.13+, once
# Support for earlier versions is dropped, this custom
# implementation can be removed.
try:
    from warnings import deprecated as _builtin_deprecated
except ImportError:
    _builtin_deprecated = None


def deprecated(*, alt_name=None, message=None):
    """Marks a function or class as deprecated.

    Emits a DeprecationWarning whenever the decorated function is called
    or the decorated class is instantiated.

    Parameters
    ----------
    alt_name : str, optional
        Name of the recommended alternative.
    message : str, optional
        Custom deprecation message. If None, a default message is generated.

    Returns
    -------
    decorator : function
        Decorator that wraps the deprecated object.

    Examples
    --------
    .. code-block:: python

        from diffpy._deprecations import deprecated

        # ------------------------------
        # Deprecated function
        # ------------------------------
        @deprecated(alt_name="new_function")
        def old_function(x, y):
            return x + y

        def new_function(x, y):
            return x + y

        # Usage
        old_function(1, 2)  # Emits DeprecationWarning
        new_function(1, 2)  # No warning

        # ------------------------------
        # Deprecated class
        # ------------------------------
        @deprecated(alt_name="NewAtom")
        class OldAtom:
            def __init__(self, symbol):
                self.symbol = symbol

        # Usage
        a = OldAtom("C")  # Emits DeprecationWarning
        atom = NewAtom("C")  # No warning
    """
    if _builtin_deprecated:
        return _builtin_deprecated

    def decorator(obj):
        name = getattr(obj, "__name__", repr(obj))
        msg = message or (
            f"'{name}' is deprecated. Use '{alt_name}' instead."
            if alt_name
            else f"'{name}' is deprecated."
        )

        if callable(obj):

            @functools.wraps(obj)
            def wrapper(*args, **kwargs):
                warnings.warn(msg, DeprecationWarning, stacklevel=2)
                return obj(*args, **kwargs)

            return wrapper
        else:
            raise TypeError(
                "deprecated decorator can only be applied to functions or "
                "classes"
            )

    return decorator
