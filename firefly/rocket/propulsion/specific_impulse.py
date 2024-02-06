""" This module contains classes to represent the specific impulse of a rocket motor."""


from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from numpy.typing import NDArray
from firefly.plot.line import plot_line

from firefly.validation.values import validate_float
from firefly.math.interp1D import Interp1D

# ============================ GLOBAL INTERFACE ============================ #
@dataclass
class SpecificImpulse(ABC):
    """
    Abstract base class representing the specific impulse of a rocket engine.
    """
    _START_TIME = 0.0
    _DEFAULT_COMBUSTION_TIME = 100.0 # seconds - used fpr plotting

    @abstractmethod
    def get_current(self, time_since_ignition: float) -> float:
        """
        Abstract method to get the current specific impulse at a given time since ignition.

        Args:
            time_since_ignition (float): The time since ignition.

        Returns:
            float: The current specific impulse at the given time since ignition.
        """

    def _validate_time(self, time_since_ignition: float) -> float:
        """
        Validate the time since ignition.

        Args:
            time_since_ignition (float): The time since ignition.

        Returns:
            float: The time since ignition.
        """
        time_since_ignition = validate_float(time_since_ignition)
        if time_since_ignition < self._START_TIME:
            raise ValueError(
                f"The time since ignition must be greater than or equal to {self._START_TIME}")
        return time_since_ignition

    @abstractmethod
    def plot(self, file: Path) -> Path:
        """
        Plot the specific impulse and save the plot to a file.

        Args:
            file (Path): The file path to save the plot.

        Returns:
            Path: The file path where the plot is saved.
        """

# ================================= NO ISP ================================= #
@dataclass
class NoSpecificImpulse(SpecificImpulse):
    """
    Class representing a specific impulse with no specific value, i.e. no motor

    This class inherits from the SpecificImpulse class and overrides
    the get_current method to always return 0.0.

    """
    specific_impulse = 0.0

    def get_current(self, time_since_ignition: float) -> float:
        #validate time
        time_since_ignition = self._validate_time(time_since_ignition)
        return 0.0

    def plot(self, file: Path) -> Path:
        """
        Plot the specific impulse over time.

        Args:
            file (Path): The file path to save the plot.

        Returns:
            Path: The file path where the plot is saved.
        """
        return plot_line(
            x_data=np.array([0., self._DEFAULT_COMBUSTION_TIME]),
            y_data=np.array([0., 0.]),
            x_label="Combustion Time [s]",
            y_label="Specific Impulse [s]",
            title="Specific Impulse",
            file=file
        )

# ============================== CONSTANT ISP ============================== #
@dataclass
class ConstantSpecificImpulse(SpecificImpulse):
    """
    Class representing a constant specific impulse at all times.

    This class inherits from the SpecificImpulse class and overrides the
    get_current method to always return the specified specific impulse value.

    Args:
        specific_impulse (float): The constant specific impulse value.

    Returns:
        float: The constant specific impulse value.
    """

    def __init__(self, *, specific_impulse: float):
        """
        Initialize the ConstantSpecificImpulse instance.

        Args:
            specific_impulse (float): The constant specific impulse value.

        Returns:
            None
        """
        # validation
        self.specific_impulse = validate_float(specific_impulse)

        # validate that specific impulse is non-negative
        if self.specific_impulse < 0:
            raise ValueError("Specific impulse must be >= 0")

    def get_current(self, time_since_ignition: float) -> float:
        time_since_ignition = self._validate_time(time_since_ignition)
        return self.specific_impulse

    def plot(self,file:Path) -> Path:
        """
        Plot the specific impulse over time.

        Parameters:
        - file (Path): The file path to save the plot.

        Returns:
        - None
        """
        return plot_line(
            x_data=np.array([0.,self._DEFAULT_COMBUSTION_TIME]),
            y_data=np.array([self.specific_impulse,self.specific_impulse]),
            x_label="Combustion Time [s]",
            y_label="Specific Impulse [s]",
            title="Specific Impulse",
            file=file
        )

class VariableSpecificImpulse(SpecificImpulse):
    """
    Class representing a variable specific impulse.

    This class inherits from the SpecificImpulse class and overrides the
    get_current method to interpolate the specific impulse value at a given time since ignition.

    Args:
        time_specific_impulse (ndarray): The time values for the specific impulse
        data since ignition.
        values_specific_impulse (ndarray): The specific impulse values corresponding
        to the time values.

    Returns:
        float: The interpolated specific impulse value at the given time since ignition.

    Raises:
        ValueError: If the time_since_ignition is less than the start time (ie. 0.O).

    """
    __START_TIME = 0.0

    def __init__(self,
                 *,
                 time_specific_impulse:  NDArray[np.float64],
                 values_specific_impulse:  NDArray[np.float64]):

        # create interpolation object
        self._interp1d = Interp1D(time_specific_impulse, values_specific_impulse)

        # validate that time starts at 0
        if time_specific_impulse[0] != self.__START_TIME:
            raise ValueError(f"The first time value must be {self.__START_TIME} [s]")

        # validate that specific impulse values are non-negative
        if np.any(values_specific_impulse < 0):
            raise ValueError("Specific impulse values must be >= 0")

    def get_current(self, time_since_ignition: float) -> float:
        """
        Returns the current specific impulse value based on the time since ignition.
        if the time is greater than the last time value, the last specific impulse
        value is returned.
        if the time is less than the first time value, the first specific impulse
        value is returned.

        Args:
            time_since_ignition (float): The time elapsed since ignition in seconds.

        Returns:
            float: The current specific impulse value.

        Raises:
            ValueError: If the time_since_ignition is negative.
        """

        # validation
        time_since_ignition = self._validate_time(time_since_ignition)

        return self._interp1d.get_value(
            time_since_ignition,
            allow_extrapolation=True,
        )

    def plot(self,file:Path) -> Path:
        return plot_line(
            x_data=self._interp1d.x,
            y_data=self._interp1d.y,
            x_label="Combustion Time [s]",
            y_label="Specific Impulse [s]",
            title="Specific Impulse",
            file=file
        )

if __name__=="__main__":
    isp = ConstantSpecificImpulse(specific_impulse=200.)
    isp.plot(Path('test.png'))
    
    isp = VariableSpecificImpulse(
        time_specific_impulse=np.array([0., 100., 200.]),
        values_specific_impulse=np.array([200., 150., 100.])
    )
    isp.plot(Path('test2.png'))