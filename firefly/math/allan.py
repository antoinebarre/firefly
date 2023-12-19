# -*- coding: utf-8 -*-
"""
Module Name: allan
Description: This module provides functions for performing Allan variance
calculations.
Author: Antoine Barré
Created: 2023-12-05
"""

__all__ = [
    'allan_variance',
    'plot_allan_deviation',
    ]

# Import statements
from typing import List, Optional, Tuple, Union
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import nnls
import pandas as pd


def _compute_cluster_sizes(
        n_samples: int,
        dt: float,
        tau_min: Optional[float] = None,
        tau_max: Optional[float] = None,
        n_clusters: int = 100,
        ) -> np.ndarray:
    """
    INTERNAL FUNCTION

    Compute the sizes of clusters based on the given parameters.

    This function calculates the minimum and maximum sizes of clusters based
    on the provided tau_min and tau_max values.
    It then generates a logarithmically spaced array of cluster sizes between
    these min and max values.

    Args:
        n_samples (int): The number of samples.
        dt (float): The time step size.
        tau_min (Optional[float]): The minimum cluster size. If None,
        it defaults to 1.
        tau_max (Optional[float]): The maximum cluster size. If None,
        it defaults to n_samples // 10.
        n_clusters (int): The number of clusters.

    Returns:
        np.ndarray: A numpy array of unique, rounded cluster sizes.
    """
    # function implementation
    if tau_min is None:
        min_size = 1
    else:
        min_size = int(tau_min / dt)

    if tau_max is None:
        max_size = n_samples // 10
    else:
        max_size = int(tau_max / dt)

    result = np.logspace(np.log2(min_size), np.log2(max_size),
                         num=n_clusters, base=2)

    return np.unique(np.round(result)).astype(int)


def allan_variance(
        x: np.ndarray,
        dt: float = 1.,
        tau_min: Optional[float] = None,
        tau_max: Optional[float] = None,
        n_clusters: int = 100,

        input_type: str = 'mean'
        ) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute Allan variance (AVAR).

    Args:
        x (np.ndarray): Sensor readings, interpretation depends on `input_type`
        argument. Assumed to vary along the 0-th axis.
        dt (float, optional): Sampling period. Default is 1.
        tau_min (float or None, optional): Minimum averaging time to use.
            If None (default), it is assigned equal to `dt`.
        tau_max (float or None, optional): Maximum averaging time to use.
            If None (default), it is chosen automatically such that to
            averaging is done over 10 *independent* clusters.
        n_clusters (int, optional): Number of clusters to compute Allan
        variance for. The averaging times will be spread approximately uniform
        in a log scale. Default is 100.
        input_type (str, optional): How to interpret the input data.
            Can be 'mean', 'increment', or 'integral'. Default is 'mean'.

    Returns:
        tuple: A tuple containing:
            - tau (np.ndarray): Averaging times for which Allan variance was
                computed, 1-d array.
            - avar (np.ndarray): Values of AVAR. The 0-th dimension is the same
                as for `tau`. The trailing dimensions match ones for `x`.

    Note:
        Consider an underlying measurement y(t). Our sensors output integrals
        of y(t) over successive time intervals of length dt. These measurements
        x(k * dt) form the input to this function.

        Allan variance is defined for different averaging times tau = m * dt as
        follows::

            AVAR(tau) = 1/2 * <(Y(k + m) - Y(k))>,

        where Y(j) is the time average value of y(t) over
        [k * dt, (k + m) * dt]
        (call it a cluster), and < ... > means averaging over different
        clusters. If we define X(j) being an integral of x(s) from 0 to dt * j,
        we can rewrite the AVAR as  follows::

            AVAR(tau) = 1/(2 * tau**2) * <X(k + 2 * m) - 2 * X(k + m) + X(k)>

        We implement < ... > by averaging over different clusters of a given
        sample with overlapping, and X(j) is readily available from x.

    References:
        [1] https://en.wikipedia.org/wiki/Allan_variance
    """
    # function implementation
    allowed_input_types = ['mean', 'increment', 'integral']

    if input_type not in allowed_input_types:
        raise ValueError(
            f"`input_type` must be one of {allowed_input_types}."
                         )

    x = np.asarray(x, dtype=float)
    if input_type == 'integral':
        data = x
    else:
        data = np.cumsum(x, axis=0)

    cluster_sizes = _compute_cluster_sizes(len(x), dt, tau_min, tau_max,
                                           n_clusters)

    avar = np.empty(cluster_sizes.shape + data.shape[1:])
    for i, k in enumerate(cluster_sizes):
        c = data[2*k:] - 2 * data[k:-k] + data[:-2*k]
        avar[i] = np.mean(c**2, axis=0) / k / k

    if input_type == 'mean':
        avar *= 0.5
    else:
        avar *= 0.5 / dt**2

    return cluster_sizes * dt, avar


def __identify_slope(
        tau: np.ndarray,
        avar: np.ndarray,
        ) -> np.ndarray:
    """
    INTERNAL FUNCTION
    identify slope of the allan variance (or allan deviation) curve
    """
    # calculate log values
    logtau = np.log10(tau)
    logavar = np.log10(avar)

    # compute slope
    dlogavar = np.diff(logavar) / np.diff(logtau)

    return dlogavar


def identify_random_walk_coefficient(
        tau: np.ndarray,
        adev: np.ndarray,
        ax: Optional[plt.Axes] = None,):

    # slope of the allan deviation curve for a random walk is 0.5
    slope = 0.5

    # calculate the delta between the slope and the allan deviation curve
    delta = np.abs(slope - __identify_slope(tau, adev))

    # identify the index where the slope of the log-scaled Allan deviation is
    # equal to the slope specified.
    if np.min(delta) > np.abs(slope):
        raise ValueError(("No part of The slope of the Allan deviation curve "
                          "is equal"
                         "to the slope specified (0.5) for a random walk. "
                          f"min value of delta is {np.min(delta)}"))
    else:
        index = np.argmin(delta)

        # find the y intercept of the line
        b = np.log10(adev[index]) - slope * np.log10(tau[index])

        # Determine the rate random walk coefficient from the line.
        log_K = b + slope * np.log10(3)
        K = 10**log_K

    # add plot of the white noise identification figure
    if ax is not None:
        line_n = K * np.sqrt(tau / 3)
        ax.loglog(tau, line_n, 'r--', label='Random Walk Slope')
        ax.legend(loc='best')

    # return the white noise coefficient
    return K


def identify_white_noise_coefficient(
        tau: np.ndarray,
        adev: np.ndarray,
        ax: Optional[plt.Axes] = None,):
    """_summary_

    Args:
        tau (np.ndarray): _description_
        adev (np.ndarray): _description_
        ax (Optional[plt.Axes], optional): _description_. Defaults to None.

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    # slope of the allan deviation curve for a whith noise is -0.5
    slope = -0.5

    # calculate the delta between the slope and the allan deviation curve
    delta = np.abs(slope - __identify_slope(tau, adev))

    # identify the index where the slope of the log-scaled Allan deviation is
    # equal to the slope specified.
    if np.min(delta) > np.abs(slope):
        raise ValueError(("No part of The slope of the Allan deviation curve "
                          "is equal"
                         "to the slope specified (-0.5) for a white noise. "
                          f"min value of delta is {np.min(delta)}"))
    else:
        index = np.argmin(delta)

        # find the y intercept of the line
        b = np.log10(adev[index]) - slope * np.log10(tau[index])

        # determine the white noise coefficient
        log_N = b + slope * np.log10(1)
        N = 10**log_N

    # add plot of the white noise identification figure
    if ax is not None:
        line_n = N/np.sqrt(tau)
        ax.loglog(tau, line_n, 'r--', label='White Noise Slope')
        ax.legend(loc='best')

    # return the white noise coefficient
    return N


def identify_pink_noise_coefficient(
        tau: np.ndarray,
        adev: np.ndarray,
        ax: Optional[plt.Axes] = None,):

    # slope of the allan deviation curve for a random walk is 0.5
    slope = 0.

    # calculate the delta between the slope and the allan deviation curve
    delta = np.abs(slope - __identify_slope(tau, adev))

    # identify the index where the slope of the log-scaled Allan deviation is
    # equal to the slope specified.
    if np.min(delta) > np.abs(0.1):
        raise ValueError(("No part of The slope of the Allan deviation curve "
                          "is equal"
                         "to the slope specified (0.) for a pink noise. "
                          f"min value of delta is {np.min(delta)}"))
    else:
        index = np.argmin(delta)

        # find the y intercept of the line
        b = np.log10(adev[index]) - slope * np.log10(tau[index])

        # Determine the rate random walk coefficient from the line.
        scfB = np.sqrt(2*np.log(2) / np.pi)
        log_B = b + slope * np.log10(scfB)
        B = 10**log_B

    # add plot of the white noise identification figure
    if ax is not None:
        line_b = B * scfB * np.ones(len(tau))
        ax.loglog(tau, line_b, 'r--', label='Pink Noise Slope')
        ax.legend(loc='best')

    # return the white noise coefficient
    return B


def plot_allan_deviation(
        tau: np.ndarray,
        adev: np.ndarray,
        ax: Optional[plt.Axes] = None,
        **kwargs
        ) -> plt.Axes:
    """
    Plot Allan deviation (ADEV) vs. averaging time.

    Args:
        tau (np.ndarray): Averaging times for which Allan variance was computed
            1-d array.
        adev (np.ndarray): Values of ADEV. The 0-th dimension is the same
            as for `tau`. The trailing dimensions match ones for `x`.
        ax (plt.Axes, optional): Axes to plot on. If None (default), a new
            figure is created.
        **kwargs: Additional keyword arguments to pass to `plt.plot`.

    Returns:
        plt.Axes: Axes object.
    """
    # function implementation
    _, ax = plt.subplots()

    ax.loglog(tau, adev, label="Allan deviation", **kwargs)
    ax.set_xlabel(r'Averaging time $\tau$, s')
    ax.set_ylabel('Allan deviation, unit')
    ax.legend(loc='best')
    ax.grid(True, which="both", ls="-", color='0.65')

    return ax


def params_from_avar(
    tau: np.ndarray,
    avar: Union[np.ndarray, Tuple[np.ndarray, int]],
    effects: Optional[List[str]] = None,
    sensor_names: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, Union[np.ndarray, Tuple[np.ndarray, int]]]:
    """
    Estimate noise parameters from Allan variance.

    Args:
        tau (np.ndarray): Values of averaging time.
        avar (Union[np.ndarray, Tuple[np.ndarray, int]]): Values of Allan
            variance corresponding to `tau`.
        effects (List[str], optional): Which effects to estimate. Allowed
            effects are 'quantization', 'white', 'flicker', 'walk', 'ramp'.
            If None (default), estimate all of the mentioned above effects.
        sensor_names (List[str], optional): How to name sensors in the output.
            If None (default), use integer.

    Returns:
        Tuple[pd.DataFrame, Union[np.ndarray, Tuple[np.ndarray, int]]]: A
            tuple containing:
            - params (pd.DataFrame): Estimated parameters.
            - prediction (Union[np.ndarray, Tuple[np.ndarray, int]]):
                Predicted values of Allan variance using the estimated
                parameters.

    Note:
        The parameters being estimated are typical for inertial sensors:
        quantization noise, additive white noise, flicker noise (long term
        bias instability), random walk and linear ramp (this is a
        deterministic effect).

        The parameters are estimated using linear least squares with weights
        inversely proportional to the values of Allan variance. That is the
        sum of relative error is minimized. This approach is approximately
        equivalent of doing estimation in the log-log scale.
    """
    # function implementation
    allowed_effects = ['quantization', 'white', 'flicker', 'walk', 'ramp']

    avar = np.asarray(avar)
    single_series = avar.ndim == 1
    if single_series:
        avar = avar[:, None]

    if effects is None:
        effects = allowed_effects
    elif not set(effects) <= set(allowed_effects):
        raise ValueError("Unknown effects are passed.")

    n = len(tau)

    A = np.empty((n, 5))
    A[:, 0] = 3 / tau**2
    A[:, 1] = 1 / tau
    A[:, 2] = 2 * np.log(2) / np.pi
    A[:, 3] = tau / 3
    A[:, 4] = tau**2 / 2
    mask = ['quantization' in effects,
            'white' in effects,
            'flicker' in effects,
            'walk' in effects,
            'ramp' in effects]

    A = A[:, mask]
    effects = np.asarray(allowed_effects)[mask]

    params = []
    prediction = []

    for column in range(avar.shape[1]):
        avar_single = avar[:, column]
        a_scaled = A / avar_single[:, None]
        x = nnls(a_scaled, np.ones(n))[0]
        prediction.append(a_scaled.dot(x) * avar_single)
        params.append(np.sqrt(x))

    params = np.asarray(params)
    prediction = np.asarray(prediction).T

    params = pd.DataFrame(params, index=sensor_names, columns=effects)

    if single_series:
        params = params.iloc[0]
        prediction = prediction[:, 0]

    return params, prediction


# Main code
if __name__ == "__main__":
    # Code to execute when the module is run as a standalone script
    pass
