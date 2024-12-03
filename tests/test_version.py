"""Unit tests for __version__.py
"""

import diffpy.utils


def test_package_version():
    """Ensure the package version is defined and not set to the initial placeholder."""
    assert hasattr(diffpy.utils, "__version__")
    assert diffpy.utils.__version__ != "0.0.0"
