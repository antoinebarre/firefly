"""
Module representing the flow rate of a rocket engine.

This module contains classes and functions related to the flow rate of a rocket engine.
"""

from abc import ABC, abstractmethod
from dataclasses import KW_ONLY, dataclass
import numpy as np
from numpy.typing import NDArray
from firefly.math.interp1D import Interp1D

from firefly.validation import validate_float


@dataclass
class FlowRate(ABC):
    """
    Abstract base class representing the flow rate of a rocket engine.
    """

    _START_TIME = 0.0

    @abstractmethod
    def get_current(self, time_since_ignition: float) -> float:
        """
        Abstract method to get the current flow rate at a given time since ignition.

        Args:
            time_since_ignition (float): The time since ignition.

        Returns:
            float: The current flow rate at the given time since ignition.
        """

    @abstractmethod
    def get_current_used_propellant_mass(self, time_since_ignition: float) -> float:
        """
        Method to get the used propellant mass at a given time since ignition.

        Args:
            time_since_ignition (float): The time since ignition.

        Returns:
            float: The used propellant mass at the given time since ignition.
        """

    @abstractmethod
    def get_total_propellant_mass(self) -> float:
        """
        Method to get the total used propellant mass.

        Returns:
            float: The total propellant mass.
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


@dataclass
class ConstantFlowRate(FlowRate):
    """
    Class representing a constant flow rate at all times.

    This class inherits from the FlowRate class and overrides the
    get_current method to always return the specified flow rate value.

    Args:
        flow_rate (float): The constant flow rate value.

    Returns:
        float: The constant flow rate value.
    """

    _: KW_ONLY
    flow_rate: float
    combustion_duration: float

    def get_current(self, time_since_ignition: float) -> float:
        """
        Get the current flow rate at a given time since ignition.

        Args:
            time_since_ignition (float): The time since ignition.

        Returns:
            float: The current flow rate at the given time since ignition.
        """
        # validation
        time_since_ignition = self._validate_time(time_since_ignition)

        return self.flow_rate if time_since_ignition < self.combustion_duration else 0.0

    def get_current_used_propellant_mass(self, time_since_ignition: float) -> float:
        """
        Get the used propellant mass at a given time since ignition.

        Args:
            time_since_ignition (float): The time since ignition.

        Returns:
            float: The used propellant mass at the given time since ignition.
        """
        # validation
        time_since_ignition = self._validate_time(time_since_ignition)

        return (self.flow_rate * time_since_ignition
                if time_since_ignition < self.combustion_duration
                else self.flow_rate * self.combustion_duration)

    def get_total_propellant_mass(self) -> float:
        """
        Get the total propellant mass.

        Returns:
            float: The total propellant mass.
        """
        return self.flow_rate * self.combustion_duration

# ============================== VARIABLE FLOW RATE ============================== #
@dataclass
class VariableFlowRate(FlowRate):
    """Represents a variable flow rate for a rocket.

    Args:
        times_flow_rate (np.ndarray): Array of time values for flow rate.
        values_flow_rate (np.ndarray): Array of flow rate values corresponding to the time values.

    Attributes:
        _interp1d (Interp1D): Interpolation object for flow rate values.
        combustion_duration (float): Duration of combustion.

    Raises:
        ValueError: If the first time value is not equal to the start time.

    """

    _: KW_ONLY

    def __init__(self,
                 *,
                 times_flow_rate:  NDArray[np.float64],
                 values_flow_rate:  NDArray[np.float64]):
        """Initializes a VariableFlowRate object.

        Args:
            times_flow_rate (np.ndarray): Array of time values for flow rate.
            values_flow_rate (np.ndarray): Array of flow rate values corresponding
            to the time values.

        Raises:
            ValueError: If the first time value is not equal to the start time.

        """
        # create interpolation object
        self._interp1d = Interp1D(times_flow_rate, values_flow_rate)
        self.combustion_duration = times_flow_rate[-1]

        if times_flow_rate[0] != self._START_TIME:
            raise ValueError(f"The first time value must be {self._START_TIME} [s]")

    def get_current(self, time_since_ignition: float) -> float:
        """Returns the current flow rate at a given time since ignition.

        Args:
            time_since_ignition (float): Time elapsed since ignition.

        Returns:
            float: The current flow rate.

        """
        # validation
        time_since_ignition = self._validate_time(time_since_ignition)

        return self._interp1d.get_value(
            time_since_ignition,
            allow_extrapolation=True,
            right=0.0)

    def get_current_used_propellant_mass(self, time_since_ignition: float) -> float:
        """Returns the current used propellant mass at a given time since ignition.

        Args:
            time_since_ignition (float): Time elapsed since ignition.

        Returns:
            float: The current used propellant mass.

        """
        # validation
        time_since_ignition = self._validate_time(time_since_ignition)

        return (
            self._interp1d.cummulative_integral(time_since_ignition)
            if time_since_ignition < self.combustion_duration
            else self.get_total_propellant_mass()
        )

    def get_total_propellant_mass(self) -> float:
        """Returns the total propellant mass.

        Returns:
            float: The total propellant mass.

        """
        return self._interp1d.integrate_all()

if __name__=="__main__":
    print("This is the flow_rate module.")

    b = VariableFlowRate(
        times_flow_rate=np.array([0.0, 10.0, 20.0]),
        values_flow_rate=np.array([100.0, 50.0, 10.0]))

    print(b.get_current(20.1))
    print(b.get_current_used_propellant_mass(20.1))