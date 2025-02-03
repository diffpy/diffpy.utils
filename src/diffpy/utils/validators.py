def is_number(string):
    """Check if the provided string can be converted to a float.

    Since integers can be converted to floats, this function will return True
    for integers as well. Hence, we can use this function to check if a
    string is a number.

    Parameters
    ----------
    string : str
        The string to evaluate for numeric conversion.

    Returns
    -------
    bool
        The boolean whether `string` can be successfully converted to float.

    Examples
    --------
    >>> is_number("3.14")
    True

    >>> is_number("-1.23")
    True

    >>> is_number("007")
    True

    >>> is_number("five")
    False

    >>> is_number("3.14.15")
    False

    >>> is_number("NaN")
    True

    >>> is_number("Infinity")
    True

    >>> is_number("Inf")
    True
    """
    try:
        float(string)
        return True
    except ValueError:
        return False
