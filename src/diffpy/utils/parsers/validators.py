def isnumber(s):
    """True if s is convertible to float."""
    try:
        float(s)
        return True
    except ValueError:
        pass
    return False