import pytest

from diffpy.utils.validators import is_number


@pytest.mark.parametrize(
    "input,expected",
    [
        ("3.14", True),  # Standard float
        ("2", True),  # Integer
        ("-100", True),  # Negative integer
        ("-3.14", True),  # Negative float
        ("0", True),  # Zero
        ("4.5e-1", True),  # Scientific notation
        ("abc", False),  # Non-numeric string
        ("", False),  # Empty string
        ("3.14.15", False),  # Multiple dots
        ("2+3", False),  # Arithmetic expression
        ("NaN", True),  # Not a Number (special float value)
        ("Infinity", True),  # Positive infinity
        ("-Infinity", True),  # Negative infinity
        ("Inf", True),  # Positive infinity
        ("-Inf", True),  # Negative infinity
    ],
)
def test_is_number(input, expected):
    assert is_number(input) == expected
