import numpy as np
import pytest

from diffpy.utils.parsers.resample import wsinterp


def test_wsinterp():
    import random

    # Check known points are unchanged by interpolation
    # FIXME: if another SW interp function exists, run comparisons for interpolated points
    # Sampling rate
    ssr = 44100**-1  # Standard sampling rate for human-hearable frequencies
    t = ssr
    n = 5
    xp = np.array([i * t for i in range(-n, n + 1, 1)])
    x = np.array([i * t for i in range(-n - 1, n + 2, 1)])

    # Interpolate a few random datasets
    trials = 10
    for trial in range(trials):
        fp = np.array([random.random() * ssr for i in range(-n, n + 1, 1)])
        fp_at_x = wsinterp(x, xp, fp)
        assert np.allclose(fp_at_x[1:-1], fp)
        for i in range(len(x)):
            assert fp_at_x[i] == pytest.approx(wsinterp(x[i], xp, fp))


if __name__ == "__main__":
    test_wsinterp()
