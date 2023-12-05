"""test for white_noise function
path: tests/math/test_white_noise.py
"""

import math
import numpy as np
import pytest
from firefly.math.noise import white_noise

ABSOLUTE_TOLERANCE = 1e-3

def test_white_noise():
    """
    Test function for white_noise.

    This function tests the white_noise function with different parameters.
    It checks if the generated white noise has the expected properties.

    Test case 1: Default parameters
    Test case 2: Custom parameters
    """

    # Test case 1: Default parameters
    npts = 10000000
    dsp = 1.0
    fs = 1.0
    seed = None

    result = white_noise(npts, dsp, fs, seed)

    assert len(result) == npts
    assert np.mean(result) == pytest.approx(0.0, abs=ABSOLUTE_TOLERANCE)
    assert np.std(result) == pytest.approx(math.sqrt(dsp*fs), abs=ABSOLUTE_TOLERANCE)

    # Test case 2: Custom parameters
    npts = 5000000
    dsp = 0.5
    fs = 2.0
    seed = 12345

    result = white_noise(npts, dsp, fs, seed)

    assert len(result) == npts
    assert np.mean(result) == pytest.approx(0.0, abs=ABSOLUTE_TOLERANCE)
    assert np.std(result) == pytest.approx(math.sqrt(dsp*fs), abs=ABSOLUTE_TOLERANCE)
