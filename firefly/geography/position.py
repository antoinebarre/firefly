"""
Definition of Position Class
"""

from __future__ import annotations

# PYLINT rules
# pylint: disable=C0103

# EXPORT
__all__ = [
    "Position"
]

# IMPORT
import math
from beartype import beartype
import numpy as np
from pydantic import BaseModel, ConfigDict

from firefly.earth.earth_model import EarthModel
from firefly.types import FloatNumber



# IMPORT

from firefly.settings import DEFAULT_EARTH_MODEL


class Position(BaseModel):
    """Class for the management of ECEF position
    """
    x: float
    y: float
    z: float

    # -------------------------- CONFIGURATION ------------------------- #
    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True,
        frozen=False,
        )

    # --------------------------- CONSTRUCTOR -------------------------- #

    def __init__(self,
                 x: FloatNumber,
                 y: FloatNumber,
                 z: FloatNumber):
        """create a Position object based on ECEF coordinates

        Args:
            x (float): x coordinates in ECEF
            y (float): y coordinates in ECEF
            z (float): z coordinates in ECEF
        """
        super().__init__(
            x=float(x),
            y=float(y),
            z=float(z)
        )

    # ------------------------- DUNDER METHODS ------------------------- #
    def __repr__(self):
        """internal method for the print"""
        return f"ECEF Coordinates:\nx : {self.x}\ny : {self.y}\nz : {self.z}"

    def __eq__(self, __o: object) -> bool:
        """internal method for equality"""
        if isinstance(__o, Position):
            return (self.x, self.y, self.z) == (__o.x, __o.y, __o.z)
        raise NotImplementedError(
            "Class Position equality with" +
            f" this data type [{type(__o)} is not implemented]")

    def __sub__(self, __o: object) -> Position:
        """internal method for equality"""
        if isinstance(__o, Position):
            return Position(self.x - __o.x, self.y - __o.y, self.z - __o.z)

        msg = (
            f"Class Position equality with this data type [{type(__o)}"
            " is not implemented]"
        )
        raise NotImplementedError(msg)

    # ------------------------- PROPERTIES -------------------------
    @property
    def norm(self) -> float :
        """
        Calculate the Euclidean norm of the position vector.

        Returns:
            float: The Euclidean norm of the position vector.

        Examples:
            >>> position = Position(x=1, y=2, z=3)
            >>> position.norm
            3.7416573867739413
        """

        return float(np.linalg.norm([self.x, self.y, self.z]))

    # ----------------------------- EXPORT ----------------------------- #

    def as_numpy_vector(self) -> np.ndarray:
        """
        Convert the position to a NumPy array.

        Returns:
            np.ndarray: A NumPy array representing the position vector.

        Examples:
            >>> position = Position(x=1, y=2, z=3)
            >>> position.as_numpy_vector()
            array([1, 2, 3])
        """

        return np.array([self.x, self.y, self.z])

    # --------------------------- LLA / ECEF --------------------------- #

    @beartype
    @staticmethod
    def from_LLA(lat: FloatNumber,
                 long: FloatNumber,
                 alt: FloatNumber,
                 earth_model: str = DEFAULT_EARTH_MODEL
                 ) -> Position:
        """create a position object based on geodetic
        position (ie. latitude, longitude, altitude)

        Args:
            lat (float): latitude in radians
            long (float): longitude in radians
            alt (float): altitude in meters
            earth_model (str, optional): Model of
                Earth Ellipsoid. Defaults to "WGS84".

        Returns:
            obj: instance of Position Class
        """

        # create EarthModel
        earth = EarthModel(earth_model)

        # constante
        a = earth.a
        e2 = earth.e**2

        # transofrmation algorithm
        sinlat = np.sin(lat)
        coslat = np.cos(lat)

        N = a / np.sqrt(1 - e2 * sinlat**2)

        # Calculate ECEF position
        X = (N + alt) * coslat * np.cos(long)
        Y = (N + alt) * coslat * np.sin(long)
        Z = (N*(1 - e2) + alt) * sinlat

        return Position(X, Y, Z)

    def as_LLA(self,
               earth_model: str = DEFAULT_EARTH_MODEL
               ):
        """return the geographic position (i.e. latitude, longitude and
        altitude) against an Ellipsoid model (by default WGS84)

        Args:
            earth_model (str, optional): Ellispoid reference.
            Defaults to "WGS84".

        Returns:
            float : latitude in radians
            float : longitude in radians
            float : altitude in radians
        """
        # create EarthModel
        earth = EarthModel(earth_model)

        # constante
        a = earth.a
        b = earth.b
        f = earth.f
        e = earth.e
        e2 = e**2       # Square of first eccentricity
        ep2 = e2 / (1 - e2)    # Square of second eccentricity

        # Longitude
        longitude = math.atan2(self.y, self.x)

        # Distance from Z-axis
        D = math.hypot(self.x, self.y)

        # Bowring's formula for initial parametric
        # (beta) and geodetic (phi) latitudes
        beta = math.atan2(self.z, (1 - f) * D)
        phi = math.atan2(self.z + b * ep2 * math.sin(beta)**3,
                         D - a * e2 * math.cos(beta)**3)

        # Fixed-point iteration with Bowring's formula
        # (typically converges within two or three iterations)
        beta_new = math.atan2((1 - f)*math.sin(phi), math.cos(phi))
        count = 0

        while beta != beta_new and count < 1000:

            beta = beta_new
            phi = math.atan2(self.z + b * ep2 * math.sin(beta)**3,
                             D - a * e2 * math.cos(beta)**3)
            beta_new = math.atan2((1 - f)*math.sin(phi),
                                 math.cos(phi))
            count += 1

        # Calculate ellipsoidal height from the final value for latitude
        sinphi = math.sin(phi)
        N = a / math.sqrt(1 - e2 * sinphi**2)
        altitude = D * math.cos(phi) + (self.z + e2 * N * sinphi) * sinphi - N

        latitude = phi

        # voir https://github.com/kvenkman/ecef2lla/blob/master/ecef2lla.py
        return latitude, longitude, altitude
