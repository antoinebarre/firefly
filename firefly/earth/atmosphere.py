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
from firefly.earth.earth_model import EarthModel
from firefly.math.array import is_strictly_monotonic_increasing

from firefly.types import Float641DVector



# ============================== GENERIC TYPES ============================= #

class CurrentAtmosphericParameters(NamedTuple):
    """
    NamedTuple representing the current atmospheric parameters.

    Attributes:
        temperature (float): The temperature in the atmosphere.
        pressure (float): The pressure in the atmosphere.
        density (float): The density of the atmosphere.
        speed_of_sound (float): The speed of sound in the atmosphere.
    """
    temperature:float
    pressure:float
    density:float
    speed_of_sound:float

class Atmosphere(ABC):
    """
    Abstract class for handling atmospheric data.
    """
    @abstractmethod
    def current_parameters(
        self,
        altitude:float,
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
        Invalidate the negative Geometric altitude.

        Args:
            altitude2validate (float): The altitude to validate.

        Returns:
            float: The validated altitude.
        """
        if altitude2validate < 0:
            raise ValueError(
                f"Geometric Altitude must be positive, got {altitude2validate}"
            )
        return altitude2validate

    @staticmethod
    def _geometric_to_geopotential_altitude(
            altitude:float,
            r_earth:float
            ) -> float:
        """
        Convert the geometric altitude to geopotential altitude.

        Args:
            altitude (float): The geometric altitude in meters.
            r_earth (float): The radius of the Earth in meters.

        Returns:
            float: The geopotential altitude in meters.
        """
        return altitude*r_earth/(altitude+r_earth)

    @staticmethod
    def _geopotential_to_geometric_altitude(
            altitude:float,
            r_earth:float
            ) -> float:
        """
        Convert the geopotential altitude to geometric altitude.

        Args:
            altitude (float): The geopotential altitude in meters.
            r_earth (float): The radius of the Earth in meters.

        Returns:
            float: The geometric altitude in meters.
        """
        return altitude*r_earth/(r_earth-altitude)

    @staticmethod
    def get_index(
        x:float,
        xlevels:Float641DVector,
        ) -> int:
        """
        Get the index of the closest value in xlevels to x in left.

        Args:
            x (float): The value to search for.
            xlevels (List[float]): The list of values to search in.

        Returns:
            int: The index of the closest value in xlevels to x.

        Raises:
            None
        """
        if not is_strictly_monotonic_increasing(xlevels):
            raise ValueError(
                ("Xlevels must be strictly monotonic increasing.\n"
                 f"Got : {xlevels}"))

        if x <= xlevels[0]:
            return 0
        elif x > xlevels[-1]:
            return len(xlevels) - 1
        elif x in xlevels:
            index = np.where(xlevels==x)
            return int(index[0])
        else:
            return int(np.searchsorted(xlevels, x, side='left')) - 1

    @property
    @abstractmethod
    def max_altitude(self) -> float:
        """
        Get the maximum altitude.

        Returns:
            float: The maximum altitude.
        """

# ================================= USSA76 ================================= #

# The U.S. Standard Atmosphere 1976 is an idealized, steady-state model of
# mean annual conditions of Earth's atmosphere from the surface to 1000 km at
# latitude 45N, as it is assumed to exist during a period with moderate solar
# activity. The defining meteorological elements are sea-level temperature and
# pressure, and a temperature-height profile to 1000 km. The air is assumed to be
# dry, and at heights sufficiently below 86 km, the atmosphere is assumed to be
# homogeneously mixed with a relative-volume composition leading to a constant
# mean molecular weight.

# Since 1976 many constants such us Earth's radius or Avogadro's number have been
# updated. In order to have a pure COESA76 atmospheric model, the official paper
# values were used.

# +--------+---------+---------+-----------+---------------+---------------+
# | Z (km) |  H (km) |  T (K)  |  p (mbar) | rho (kg / m3) | beta (K / km) |
# +--------+---------+---------+-----------+---------------+---------------+
# |   0.0  |   0.0   | 288.150 | 1.01325e3 |     1.2250    |      -6.5     |
# +--------+---------+---------+-----------+---------------+---------------+
# | 11.019 |   11.0  | 216.650 |  2.2632e2 |   3.6392e-1   |      0.0      |
# +--------+---------+---------+-----------+---------------+---------------+
# | 20.063 |   20.0  | 216.650 |  5.4748e1 |   8.8035e-2   |      1.0      |
# +--------+---------+---------+-----------+---------------+---------------+
# | 32.162 |   32.0  | 228.650 |  8.6801e0 |   1.3225e-2   |      2.8      |
# +--------+---------+---------+-----------+---------------+---------------+
# | 47.350 |   47.0  | 270.650 |  1.1090e0 |   1.4275e-3   |      0.0      |
# +--------+---------+---------+-----------+---------------+---------------+
# | 51.413 |   51.0  | 270.650 | 6.6938e-1 |   8.6160e-4   |      -2.8     |
# +--------+---------+---------+-----------+---------------+---------------+
# | 71.802 |   71.0  | 214.650 | 3.9564e-2 |   6.4211e-5   |      -2.0     |
# +--------+---------+---------+-----------+---------------+---------------+
# |  86.0  | 84.8520 |  186.87 | 3.7338e-3 |    6.958e-6   |      0.0      |
# +--------+---------+---------+-----------+---------------+---------------+
# |  91.0  |  89.716 |  186.87 | 1.5381e-3 |    2.860e-6   |   elliptical  |
# +--------+---------+---------+-----------+---------------+---------------+
# |  110.0 | 108.129 |  240.00 | 7.1042e-5 |    9.708e-8   |      12.0     |
# +--------+---------+---------+-----------+---------------+---------------+
# |  120.0 | 117.777 |  360.00 | 2.5382e-5 |    2.222e-8   |  exponential  |
# +--------+---------+---------+-----------+---------------+---------------+
# |  500.0 | 463.540 |  999.24 | 3.0236e-9 |   5.215e-13   |  exponential  |
# +--------+---------+---------+-----------+---------------+---------------+
# | 1000.0 | 864.071 |   1000  | 7.5138e-5 |   3.561e-15   |  exponential  |
# +--------+---------+---------+-----------+---------------+---------------+

# voir https://github.com/poliastro
# voir https://www.pdas.com/programs/atmos.py
class USSA76(Atmosphere):
    """
    Class for U.S Standard Atmosphere models 1976.
    """
    # Define the layers and their properties: Base altitude (m),
    # Lapse rate (K/m), and Base temperature (K), Pressure (Pa)
    __htab = np.array([0.0, 11.0, 20.0, 32.0, 47.0, 51.0, 71.0]) * 1000 # geopotential altitude (km)
    __ttab = np.array(
        [288.15, 216.65, 216.650, 228.650, 270.650, 270.650, 214.650])
    __ptab = np.array([1.01325e3, 2.2632e2, 5.4748e1, 8.6801, 1.1090,
                           6.6938e-1, 3.9564e-2]) * 100
    __gtab = np.array([-6.5, 0.0, 1.0, 2.8, 0.0, -2.8, -2.0])/1000

    __R = 8.31432  # Specific gas constant for dry air (J/kg.K)
    __g0 = 9.80665 # Standard gravity (m/s^2)
    __M0 = 28.9644E-3 # Molar mass of dry air (kg/mol)
    __max_altitude = 86000 # m geopotential altitude
    __gamma = 1.4 # ratio of specific heats
    __P0 = 101325.0 # Pa
    __r_earth = EarthModel("WGS84").mean_radius # km mean radius for WGS84

    def __init__(
        self,
        with_warnings: bool = True) -> None:
        self.__with_warnings = with_warnings
        super().__init__()

    @property
    def max_altitude(self) -> float:
        return self.__max_altitude

    def current_parameters(
        self,
        altitude:float,
        ) -> CurrentAtmosphericParameters:
        """
        Calculate the current atmospheric parameters at the given geometric altitude.

        Args:
            altitude (float): The geometric altitude in meters.

        Returns:
            CurrentAtmosphericParameters: An object containing the current
            atmospheric parameters including temperature, pressure, density, and speed of sound.

        Raises:
            None
        """

        altitude_geometric = self.validate_altitude(altitude)

        if altitude_geometric > self.max_altitude:
            return CurrentAtmosphericParameters(
                temperature=0,
                pressure=0,
                density=0,
                speed_of_sound=0,
                )

        # convert geometric altitude to geopotential altitude
        altitude = self._geometric_to_geopotential_altitude(
             altitude=altitude_geometric,
             r_earth=self.__r_earth)

        # Get the index of the closest value in xlevels to x.
        layer_index = self.get_index(altitude, self.__htab)

        # Get the properties of the local layer
        tgrad = self.__gtab[layer_index]		# temp. gradient of local layer
        tbase = self.__ttab[layer_index]		# base  temp. of local layer
        pbase = self.__ptab[layer_index]		# base  pressure of local layer
        deltah = altitude-self.__htab[layer_index]	# height above local base

        # Calculate temperature
        temperature = tbase + tgrad * deltah	# local temperature

        # Calculate pressure
        alpha = -self.__g0 *self.__M0 / (self.__R)

        # calulate R/M_air
        m_air = self.__R/self.__M0

        if tgrad == 0.:  # isothermal layer
            pressure = pbase * np.exp(alpha / tbase * deltah)
        else: # non-isothermal layer
            pressure = pbase * \
                           (temperature / tbase) ** \
                           (alpha / tgrad)

        # Calculate density
        density = pressure / (m_air * temperature)

        # calculate speed of sound
        a = np.sqrt(self.__gamma * m_air * temperature)

        return CurrentAtmosphericParameters(
            temperature=temperature,
            pressure=pressure,
            density=density,
            speed_of_sound=a,
            )

    def validate_altitude(self, altitude2validate: float) -> float:

        altitude2validate = self._invalidate_negative_altitude(
            altitude2validate
            )
        if altitude2validate > self.max_altitude and self.__with_warnings:
            warnings.warn(
                f"Altitude should be less than {self.max_altitude}m,"
                f" got {altitude2validate}m. "
                "Please consider using a different atmosphere model."
            )
        return altitude2validate

# ================================== TOOLS ================================= #

if __name__ == "__main__":

    # Create an instance of the USSA76 atmosphere
    atmosphere = USSA76()

    ALT = 84000

    # Get the current atmospheric parameters at 10000 m
    current_parameters = atmosphere.current_parameters(ALT)

    # Print the current atmospheric parameters
    print(f"Temperature: {current_parameters.temperature} K")
    print(f"Pressure: {current_parameters.pressure} Pa")
    print(f"Density: {current_parameters.density} kg/m3")

    ALT = 88000

    # Get the current atmospheric parameters at 10000 m
    current_parameters = atmosphere.current_parameters(ALT)

    # Print the current atmospheric parameters
    print(f"Temperature: {current_parameters.temperature} K")
    print(f"Pressure: {current_parameters.pressure} Pa")
    print(f"Density: {current_parameters.density} kg/m3")
