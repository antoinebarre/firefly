"""
Firefly - This module provides functions for generating various types of noise.

Author: Your Name
Email: antoine.barre@gmail.com
"""


# -------------------------------- EXPORT ------------------------------- #

__all__ = [
    "white_noise",
    "random_walk"
]


# -------------------------------- IMPORT ------------------------------- #

import math
from typing import Optional
import numpy as np


def white_noise(
    npts: int = 1000,
    dsp: float = 1.0,
    fs: float = 1.0,
    seed: Optional[int] = None
) -> np.ndarray:
    """
    White noise generator.

    Generate time series with white noise that has constant PSD = b0,
    up to the nyquist frequency fs/2.

    The PSD is at 'height' b0 and extends from 0 Hz up to the nyquist
    frequency fs/2 (prefactor math.sqrt(b0*fs/2.0))

    Args:
        npts (int, optional): Number of samples. Default is 1000.
        DSP (float, optional): Desired power-spectral density in [X^2/Hz]
            where X is the unit of x. Default is 1.0.
        fs (float, optional): Sampling frequency, i.e. 1/fs is the
            time-interval between datapoints. Default is 1.0.
        seed (Optional[int], optional): Seed for the random generator.

    Returns:
        np.ndarray: White noise sample.
    """

    # generate random generator
    rng = np.random.default_rng(seed)

    # calculate rms
    # DSP = sig^2*dt soit sig^2 = DSP*fs
    rms = math.sqrt(dsp*fs)

    # generate serie
    if npts > np.iinfo(int).max:
        raise ValueError(
            f"Argument 'npts' must be an integer <= {np.iinfo(int).max}.")
    return rng.normal(loc=0., scale=rms, size=npts)


def random_walk(
    npts: int = 1000,
    dsp: float = 1.0,
    fs: float = 1.0,
    seed: Optional[int] = None
) -> np.ndarray:
    """
    Random walk generator.

    Generate time series with random walk noise that has constant PSD = b0,
    up to the nyquist frequency fs/2.

    The PSD is at 'height' b0 and extends from 0 Hz up to the nyquist
    frequency fs/2 (prefactor math.sqrt(b0*fs/2.0))

    Args:
        npts (int, optional): Number of samples. Default is 1000.
        DSP (float, optional): Desired power-spectral density in [X^2/Hz]
            where X is the unit of x. Default is 1.0.
        fs (float, optional): Sampling frequency, i.e. 1/fs is the
            time-interval between datapoints. Default is 1.0.
        seed (Optional[int], optional): Seed for the random generator.

    Returns:
        np.ndarray: Random walk sample.
    """

    # generate random generator
    rng = np.random.default_rng(seed)

    dt = 1/fs
    # generate serie
    if npts > np.iinfo(int).max:
        raise ValueError(
            f"Argument 'npts' must be an integer <= {np.iinfo(int).max}.")
    rng = np.random.default_rng(seed=seed)
    return np.cumsum((dsp/dt) ** 0.5 * rng.normal(loc=0., scale=1., size=npts)) * dt


if __name__ == "__main__":
    pass
