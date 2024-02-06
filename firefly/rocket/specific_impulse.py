""" This module contains classes to represent the specific impulse of a rocket motor."""


from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray

from firefly.validation.values import validate_float
from firefly.math.interp1D import Interp1D

# ============================ GLOBAL INTERFACE ============================ #
@dataclass
class SpecificImpulse(ABC):
    """
    Abstract base class representing the specific impulse of a rocket engine.
    """
    _START_TIME = 0.0

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
