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
from beartype import beartype
import numpy as np

from firefly.types import Float641DVector, FloatNumber


@dataclass
class Interp1D:
    """Perform one-dimensional linear interpolation.

    This class provides methods to interpolate new values based on
    discrete sets of known data points (x and y). It supports both
    interpolation and optional extrapolation.

    Attributes:
        x (Float641DVector): The x-coordinates of the data points,
            must be a 1D numpy array.
        y (Float641DVector): The y-coordinates of the data points,
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

    x: Float641DVector
    y: Float641DVector

    def __post_init__(self):
        """Validate the input data."""

        if (not isinstance(self.x, np.ndarray)
           or not isinstance(self.y, np.ndarray)):
            raise TypeError("x and y must be numpy arrays")
        if self.x.shape != self.y.shape:
            raise ValueError("x and y must have the same shape")
        if self.x.ndim != 1:
            raise ValueError(
                "x and y must be 1D arrays. "
                f"Got {self.x.ndim}D arrays")
        if not np.all(np.diff(self.x) > 0):
            raise ValueError(
                "x must be monotonically increasing. "
                f"Got {self.x}")

    @beartype
    def get_value(
            self,
            new_x: FloatNumber,
            allow_extrapolation: bool = True,
            **kwargs,
            ) -> float:
        """Get the interpolated value at x_new.

        Args:
            new_x (float or np.float64): The new x value to interpolate at.
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

        if not allow_extrapolation:
            if new_x < self.x[0] or new_x > self.x[-1]:
                raise ValueError(
                    "Extrapolation is not allowed. "
                    "Got values outside of the range of x.")

        return float(np.interp(new_x, self.x, self.y, **kwargs))

    @beartype
    def get_values(
            self,
            new_x: Float641DVector,
            allow_extrapolation: bool = True,
            **kwargs
            ) -> Float641DVector:
        """Get the interpolated values at x_new.

        Args:
            new_x (np.ndarray): The new x values to interpolate at.
            allow_extrapolation (bool, optional): Whether to allow
            extrapolation
            **kwargs: Additional keyword arguments to pass to np.interp.

        Returns:
            np.ndarray: The interpolated values at x_new.

        Raises:
            ValueError: If extrapolation is not allowed and any value in
                new_x is outside the range of x.

        """

        if not allow_extrapolation:
            if np.any(new_x < self.x[0]) or np.any(new_x > self.x[-1]):
                raise ValueError(
                    "Extrapolation is not allowed. "
                    "Got values outside of the range of x.")

        return np.interp(new_x, self.x, self.y, **kwargs)


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
        print(f"Average execution time: {execution_time:.6f} seconds")


if __name__ == "__main__":
    # Example usage
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([1, 2, 3, 4, 5])
    x_new = np.array([1.5, 2.5, 3.5, 4.5])

    a = Interp1D(x, y).get_value(2.5)
    print(f"Interpolated value: {a}")

    a = Interp1D(x, y).get_values(x_new)
    print(f"Interpolated values: {a}")


    Interp1D.benchmark()
