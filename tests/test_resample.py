import random

import numpy as np
import pytest

from diffpy.utils.resampler import nsinterp, wsinterp


def test_wsinterp():
    # FIXME: if another SW interp function exists, run comparisons for
    # interpolated points

    # Sampling rate
    ssr = 44100**-1  # Standard sampling rate for human-hearable frequencies

    # Creating a symmetric set of sample points around zero.
    n = 5
    xp = np.array([i * ssr for i in range(-n, n + 1, 1)])
    x = np.array([i * ssr for i in range(-n - 1, n + 2, 1)])
    assert len(xp) == 11 and len(x) == 13

    # Generate a new set of fp values across 10 trial runs
    trials = 10

    for _ in range(trials):
        # Create random function values (fp) at the points defined in xp above
        fp = np.array([random.random() * ssr for _ in range(-n, n + 1, 1)])
        fp_at_x = wsinterp(x, xp, fp)

        # Check that the known points are unchanged by interpolation
        assert np.allclose(fp_at_x[1:-1], fp)
        for i in range(len(x)):
            assert fp_at_x[i] == pytest.approx(wsinterp(x[i], xp, fp))


def test_nsinterp():
    # Create a cosine function cos(2x) for x \in [0, 3pi]
    xp = np.linspace(0, 3 * np.pi, 100)
    fp = np.cos(2 * xp)

    # Want to resample onto the grid {0, pi, 2pi, 3pi}
    x = np.array([0, np.pi, 2 * np.pi, 3 * np.pi])

    # Get wsinterp result
    ws_f = wsinterp(x, xp, fp)

    # Use nsinterp with qmin-qmax=4/3
    qmin = np.random.uniform()
    qmax = qmin + 4 / 3
    ns_x, ns_f = nsinterp(xp, fp, qmin, qmax)

    assert np.allclose(x, ns_x)
    assert np.allclose(ws_f, ns_f)
