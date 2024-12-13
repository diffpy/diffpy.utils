import random

import numpy as np
import pytest

from diffpy.utils.resampler import wsinterp


def test_wsinterp():
    # FIXME: if another SW interp function exists, run comparisons for interpolated points

    # Sampling rate
    ssr = 44100**-1  # Standard sampling rate for human-hearable frequencies

    # Creating a symmetric set of sample points around zero.
    n = 5
    xp = np.array([i * ssr for i in range(-n, n + 1, 1)])
    x = np.array([i * ssr for i in range(-n - 1, n + 2, 1)])
    assert len(xp) == 11 and len(x) == 13

    # Generating fp values across 10 trial runs
    trials = 10

    for _ in range(trials):
        # Create random function values (fp) at the points defined in xp above
        fp = np.array([random.random() * ssr for _ in range(-n, n + 1, 1)])

        # Interpolate the values at new x points
        fp_at_x = wsinterp(x, xp, fp)

        # Check that the known points are unchanged by interpolation
        assert np.allclose(fp_at_x[1:-1], fp)
        for i in range(len(x)):
            assert fp_at_x[i] == pytest.approx(wsinterp(x[i], xp, fp))


if __name__ == "__main__":
    test_wsinterp()
