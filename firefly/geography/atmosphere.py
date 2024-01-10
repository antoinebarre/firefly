"""
Module for handling atmospheric data.
"""

__author__ = "Antoine Barré"
__version__ = "1.0.0"
__license__ = "MIT"

__all__ = [
    "Atmosphere",
    "CurrentAtmosphericParameters",
    "USSA76"
]

# ================================ IMPORTS ================================= #

from abc import ABC, abstractmethod
from typing import NamedTuple
import warnings

import numpy as np



# ============================== GENERIC TYPES ============================= #

class CurrentAtmosphericParameters(NamedTuple):
    """
    NamedTuple representing the current atmospheric parameters.

    Attributes:
        temperature (float): The temperature in the atmosphere.
        pressure (float): The pressure in the atmosphere.
        density (float): The density of the atmosphere.
    """
    temperature:float
    pressure:float
    density:float

class Atmosphere(ABC):
    """
    Abstract class for handling atmospheric data.
    """
    @abstractmethod
    def current_parameters(
        self,
        altitude:float
        ) -> CurrentAtmosphericParameters:
        """
        Returns the temperature at the given altitude.
        """
    @abstractmethod
    def validate_altitude(
            self,
            altitude2validate:float) -> float:
        """
        Validate the altitude.

        Args:
            altitude2validate (float): The altitude to validate.

        Returns:
            float: The validated altitude.
        """
    def _invalidate_negative_altitude(self, altitude2validate:float) -> float:
        """
        Invalidate the negative altitude.

        Args:
            altitude2validate (float): The altitude to validate.

        Returns:
            float: The validated altitude.
        """
        if altitude2validate < 0:
            raise ValueError(
                f"Altitude must be positive, got {altitude2validate}"
            )
        return altitude2validate

    @property
    @abstractmethod
    def max_altitude(self) -> float:
        """
        Get the maximum altitude.

        Returns:
            float: The maximum altitude.
        """



# ================================= USSA76 ================================= #

class USSA76(Atmosphere):
    """
    Class for U.S Standard Atmosphere models 1976.
    """

    def __init__(self):

        # Define the layers and their properties: Base altitude (m),
        # Lapse rate (K/m), and Base temperature (K)
        self.layers = [
            (0, -0.0065, 288.15),      # Troposphere
            (11000, 0, 216.65),        # Lower Stratosphere
            (20000, 0.001, 216.65),    # Middle Stratosphere
            (32000, 0.0028, 228.65),   # Upper Stratosphere
            (47000, 0, 270.65),        # Lower Mesosphere
            (51000, -0.0028, 270.65),  # Middle Mesosphere
            (71000, -0.002, 214.65)    # Upper Mesosphere
        ]
        self.R = 287.053  # Specific gas constant for dry air (J/kg.K)
        self.g0 = 9.80665 # Standard gravity (m/s^2)

        # Get the maximum altitude
        self._max_altitude = 86E3 # m

    @property
    def max_altitude(self) -> float:
        return self._max_altitude


    def __get_layer(self, altitude):
        return next(
            (
                i - 1 if i > 0 else 0
                for i, layer in enumerate(self.layers)
                if altitude < layer[0]
            ),
            len(self.layers) - 1,
        )

    def current_parameters(
        self,
        altitude:float
        ) -> CurrentAtmosphericParameters:

        # Validate the altitude
        altitude = self.validate_altitude(altitude)

        layer_index = self.__get_layer(altitude)
        base_alt, lapse_rate, base_temp = self.layers[layer_index]

        # Calculate temperature
        temperature = base_temp + lapse_rate * (altitude - base_alt)

        # Calculate pressure
        # if lapse_rate == 0:
        #     prev_temp = self.layers[layer_index - 1][2]
        #     pressure = prev_temp * np.exp(-self.g0 / (self.R * base_temp) *
        #                                   (altitude - base_alt))
        # else:
        #     pressure = self.layers[layer_index - 1][2] * \
        #                (temperature / base_temp) ** \
        #                (-self.g0 / (self.R * lapse_rate))
        if lapse_rate == 0:
            pressure = self.layers[layer_index - 1][2] * np.exp(-self.g0 / (self.R * base_temp) * (altitude - base_alt))
        else:
            pressure = self.layers[layer_index - 1][2] * (temperature / base_temp) ** (-self.g0 / (self.R * lapse_rate))


        # Calculate density
        density = pressure / (self.R * temperature)

        return CurrentAtmosphericParameters(
            temperature=temperature,
            pressure=pressure,
            density=density
            )

    def validate_altitude(self, altitude2validate: float) -> float:

        altitude2validate = self._invalidate_negative_altitude(
            altitude2validate
            )
        if altitude2validate > self.max_altitude:
            warnings.warn(
                f"Altitude should be less than {self.max_altitude},"
                f" got {altitude2validate}. "
                "Please consider using a different atmosphere model."
            )
        return altitude2validate

# ================================== TOOLS ================================= #

if __name__ == "__main__":

    # Create an instance of the USSA76 atmosphere
    atmosphere = USSA76()

    # Get the current atmospheric parameters at 10000 m
    current_parameters = atmosphere.current_parameters(100000)

    # Print the current atmospheric parameters
    print(current_parameters)

    # Print the maximum altitude
    print(atmosphere.max_altitude)
