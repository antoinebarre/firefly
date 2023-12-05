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
        tau_min: Optional[float],
        tau_max: Optional[float],
        n_clusters: int
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


def plot_allan_deviation(
        tau: np.ndarray,
        avar: np.ndarray,
        ax: Optional[plt.Axes] = None,
        **kwargs
        ) -> plt.Axes:
    """
    Plot Allan deviation (AVAR) vs. averaging time.

    Args:
        tau (np.ndarray): Averaging times for which Allan variance was computed
            1-d array.
        avar (np.ndarray): Values of AVAR. The 0-th dimension is the same
            as for `tau`. The trailing dimensions match ones for `x`.
        ax (plt.Axes, optional): Axes to plot on. If None (default), a new
            figure is created.
        **kwargs: Additional keyword arguments to pass to `plt.plot`.

    Returns:
        plt.Axes: Axes object.
    """
    # function implementation
    _, ax = plt.subplots()

    ax.loglog(tau, np.sqrt(avar), **kwargs)
    ax.set_xlabel(r'Averaging time $\tau$, s')
    ax.set_ylabel('Allan deviation, unit')
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
