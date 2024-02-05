"""A subpackage for 1D interpolation methods.

This module provides various methods for performing 1D interpolation.
It includes functions for linear interpolation, spline interpolation,
and polynomial interpolation.

"""

__all__ = [
    "Interp1D",
    ]

# Import statements
from dataclasses import dataclass
import timeit

import numpy as np
from numpy.typing import NDArray

from firefly.math.array import is_strictly_monotonic_increasing, is_values_in_interval, sort_arrays
from firefly.validation import validate_bool, validate_float, validate_numpy_vector


@dataclass
class Interp1D:
    """Perform one-dimensional linear interpolation.

    This class provides methods to interpolate new values based on
    discrete sets of known data points (x and y). It supports both
    interpolation and optional extrapolation.

    Attributes:
        x (NDArray[np.float64]): The x-coordinates of the data points,
            must be a 1D numpy array.
        y (NDArray[np.float64]): The y-coordinates of the data points,
            must be a 1D numpy array and have the same shape as x.

    Raises:
        TypeError: If x or y is not a numpy array.
        ValueError: If x and y do not have the same shape, are not
            1D arrays, or if x is not monotonically increasing.

    Methods:
        get_value(new_x: FloatNumber, allow_extrapolation: bool = True) -> float
            Interpolate a single value at a given x-coordinate.

        get_values(new_x: Float641DVector, allow_extrapolation: bool = True) -> Float641DVector
            Interpolate a series of values at given x-coordinates.

        benchmark()
            Benchmark the performance of the interpolation methods.
    """

    x: NDArray[np.float64]
    y: NDArray[np.float64]

    def __post_init__(self):
        """Validate the input data."""
        # validate the input date
        x = validate_numpy_vector(self.x)
        y = validate_numpy_vector(self.y)

        if x.shape != y.shape:
            raise ValueError("x and y must have the same shape")
        if not is_strictly_monotonic_increasing(x):
            raise ValueError(
                "x must be monotonically increasing. "
                f"Got {self.x}")

    @property
    def min_x(self) -> float:
        """Return the minimum x value."""
        return float(self.x[0])

    @property
    def max_x(self) -> float:
        """Return the maximum x value."""
        return float(self.x[-1])

    def is_in_x_range(self, value: float) -> bool:
        """Check if the value is within the range of x.

        Args:
            value (float): The value to check.

        Returns:
            bool: True if the value is within the range of x, False otherwise.

        """
        # validation
        value = validate_float(value)

        return self.min_x <= value <= self.max_x

    def get_value(
            self,
            new_x: float,
            allow_extrapolation: bool = True,
            **kwargs,
            ) -> float:
        """Get the interpolated value at x_new.

        Args:
            new_x (float or np.float64 or int): The new x value to interpolate at.
            allow_extrapolation (bool, optional): Whether to allow
            extrapolation for values outside of the x range.
                Defaults to True.
            **kwargs: Additional keyword arguments to pass to np.interp.

        Returns:
            float: The interpolated value at x_new.

        Raises:
            ValueError: If extrapolation is not allowed and new_x is
                outside the range of x.

        """

        # validation
        new_x_float = validate_float(new_x)
        allow_extrapolation = validate_bool(allow_extrapolation)

        if not allow_extrapolation and (new_x_float < self.x[0] or new_x_float > self.x[-1]):
            raise ValueError(
                "Extrapolation is not allowed. "
                "Got values outside of the range of x.")

        return float(np.interp(new_x_float, self.x, self.y, **kwargs))


    def get_values(
                self,
                new_x: NDArray[np.float64],
                allow_extrapolation: bool = True,
                **kwargs
                ) -> NDArray[np.float64]:
        """
        Returns interpolated values for given x-coordinates.

        Args:
            new_x (ndarray): The x-coordinates for which to compute interpolated values.
            allow_extrapolation (bool, optional): Whether to allow extrapolation. Defaults to True.
            **kwargs: Additional keyword arguments to be passed to np.interp().

        Returns:
            ndarray: The interpolated values corresponding to the given x-coordinates.
        """
        # validation
        new_x = validate_numpy_vector(new_x)

        if not allow_extrapolation and (np.any(new_x < self.x[0]) or \
            np.any(new_x > self.x[-1])):
            raise ValueError(
                "Extrapolation is not allowed. "
                "Got values outside of the range of x.")

        return np.interp(new_x, self.x, self.y, **kwargs)


    def integrate_all(self) -> float:
        """Integrate the interpolated function over the entire range of x.

        Returns:
            float: The integrated value.

        """
        return float(np.trapz(self.y, self.x))

    def add_points(
                self,
                new_x: NDArray[np.float64],
                new_y: NDArray[np.float64],
                ) -> None:
        """
        Adds new points to the interpolation data.

        Args:
            new_x (ndarray): The x-coordinates of the new points.
            new_y (ndarray): The y-coordinates of the new points.

        Raises:
            ValueError: If any of the new_x values already exist in the existing data.

        Returns:
            None
        """

        # validation
        new_x = validate_numpy_vector(new_x)
        new_y = validate_numpy_vector(new_y)

        # check if some of the new_x values are already in x
        for x in new_x:
            if x in self.x:
                raise ValueError(f"the following x value is already in the data: {x}")

        x_values = np.append(self.x, new_x)
        y_values = np.append(self.y, new_y)
        indices = np.argsort(x_values)

        self.x = x_values[indices]
        self.y = y_values[indices]

    def integrate(
            self,
            begin_x: float,
            stop_x: float,
            ) -> float:
        """
        Calculate the integral of the function over the specified interval.

        Args:
            begin_x (float): The lower bound of the interval.
            stop_x (float): The upper bound of the interval.

        Returns:
            float: The value of the integral over the specified interval.

        Raises:
            ValueError: If the interval is not within the range of x.
            ValueError: If begin_x is greater than stop_x.

        """

        # validation
        begin_x = validate_float(begin_x)
        stop_x = validate_float(stop_x)

        # validate interval
        if not is_values_in_interval(
                values=np.array([begin_x,stop_x]),
                interval=self.x):
            raise ValueError("the interval is not within the range of x")
        if begin_x > stop_x:
            raise ValueError("begin_x must be less than or equal to stop_x")
        if begin_x == stop_x:
            return 0.0

        # Initialize a list to hold any points to be added for interpolation
        values_x = self.x
        values_y = self.y

        # check if begin_x and stop_x are in x
        if begin_x not in self.x :
            values_x = np.append(values_x, begin_x)
            values_y = np.append(values_y, self.get_value(begin_x))
        if stop_x not in self.x :
            values_x = np.append(values_x, stop_x)
            values_y = np.append(values_y, self.get_value(stop_x))

        # sort the values in place
        (values_x, values_y) = sort_arrays(values_x, values_y)

        # Find the indices for begin_x and stop_x
        begin_idx = int(np.searchsorted(values_x, begin_x))
        stop_idx = int(np.searchsorted(values_x, stop_x))

        # Perform the integration using the trapezoidal rule
        return np.trapz(values_y[begin_idx:stop_idx+1], values_x[begin_idx:stop_idx+1])

    def cummulative_integral(
            self,
            current_x: float) -> float:
        """
        Calculates the integral up to the given x value.

        Args:
            current_x (float): The x value up to which the cumulative integral is calculated.

        Returns:
            float: The cumulative integral up to the given x value.
        """

        # sourcery skip: extract-method, remove-unnecessary-else, swap-if-else-branches

        # validation
        current_x = validate_float(current_x)

        if not self.is_in_x_range(current_x):
            raise ValueError("current_x is not within the range of x")

        if current_x == self.min_x:
            return 0.0
        if current_x == self.max_x:
            return self.integrate_all()
        if current_x in self.x:
            idx_stop = int(np.searchsorted(self.x, current_x))
            return np.trapz(self.y[:idx_stop+1], self.x[:idx_stop+1])
        else:
            # create a new x array with the current_x value
            x_values = np.append(self.x, current_x)
            y_values = np.append(self.y, self.get_value(current_x))

            # sort the values in place
            (x_values, y_values) = sort_arrays(x_values, y_values)

            # find the index of the current_x value
            idx_stop = int(np.searchsorted(x_values, current_x))
            return np.trapz(y_values[:idx_stop+1], x_values[:idx_stop+1])


    @staticmethod
    def benchmark():
        """Benchmark the performance of the interpolation methods.

        This method runs a performance test on the interpolation methods
        using a large dataset and prints the average execution time.
        """
        # Create a large set of x and y values
        x_test = np.linspace(0, 10, 1000000)  # 1 million points between 0 and 10
        y_test = np.sin(x_test)  # Just an example function

        # New x points for interpolation
        new_x = 555.  # 10 thousand new points

        interp_object = Interp1D(x_test, y_test)

        # Define the interpolation function
        def interpolate():
            interp_object.get_value(new_x)

        # Benchmark the interpolation function
        execution_time = timeit.timeit(interpolate, number=100) / 100
        print(f"Average execution time: {execution_time:.10f} seconds")

    @staticmethod
    def benchmark_integration():
        """Benchmark the performance of the integration method.

        This method runs a performance test on the integration method
        using a large dataset and prints the average execution time.
        """
        # Create a large set of x and y values
        x_test = np.linspace(0, 10, 100)
        y_test = np.sin(x_test)

        print("x_test", 2.0 in x_test)

        interp_object = Interp1D(x_test, y_test)

        # Define the interpolation function
        def integrate():
            interp_object.integrate(
            begin_x=0.330988896678,
            stop_x=9.822302388023)

        # Benchmark the interpolation function
        execution_time = timeit.timeit(integrate, number=100) / 100
        print(f"Average execution time for integration: {execution_time:.6f} seconds")
        print(0.330988896678 in interp_object.x)


        # Define the interpolation function
        def integrate2():
            interp_object.cummulative_integral(
            current_x=2.)

        # Benchmark the interpolation function
        execution_time = timeit.timeit(integrate2, number=100) / 100
        print(f"Average execution time for integration: {execution_time:.6f} seconds")
        print(0.330988896678 in interp_object.x)

if __name__=="__main__":
    Interp1D.benchmark_integration()
    Interp1D.benchmark()
