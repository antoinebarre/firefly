"""
# ======================================================================= #
# ===================== TOOLS FOR RANGE CALCULATION ===================== #
# ======================================================================= #
"""

# EXPORT
__all__ = [
    "get_range",
]

# PYLINT rules
# pylint: disable=C0103


# IMPORT
import math
from beartype import beartype
import numpy as np
from firefly.earth.earth_model import EarthModel

from firefly.settings import DEFAULT_EARTH_MODEL
from firefly.types import FloatNumber


CONVERGENCE_THRESHOLD = 1e-12


@beartype
def get_range(
        lat1: FloatNumber,
        long1: FloatNumber,
        lat2: FloatNumber,
        long2: FloatNumber,
        earth_model: str = DEFAULT_EARTH_MODEL,
        nb_iter:int = 200,
        ) -> float:
    """
    Calculate the distance between two points on the Earth's surface using the Haversine formula.

    Args:
        lat1 (FloatNumber): The latitude of the first point in radians.
        long1 (FloatNumber): The longitude of the first point in radians.
        lat2 (FloatNumber): The latitude of the second point in radians.
        long2 (FloatNumber): The longitude of the second point in radians.
        earth_model (str, optional): The Earth model to use for the calculation.
            Defaults to DEFAULT_EARTH_MODEL.
        nb_iter (int, optional): The number of iterations for convergence.
            Defaults to 200.

    Returns:
        float: The distance between the two points in meters.

    Raises:
        ValueError: If the latitude values are not within the valid range.

    Examples:
        >>> lat1 = 0.0
        >>> long1 = 0.0
        >>> lat2 = 0.0
        >>> long2 = 1.0
        >>> get_range(lat1, long1, lat2, long2)
        111319.4908
    """


    # latitue assertion
    if abs(float(lat1)) > np.pi / 2 or abs(float(lat2)) > np.pi / 2:
        msg = ("Latitudes Value shall be lower than 90"
               f" (lat1: {np.rad2deg(lat1)} , lat2: {np.rad2deg(lat2)})")
        raise ValueError(msg)

    # short-circuit coincident points
    if lat1 == lat2 and long1 == long2:
        return 0.0

    # load earth model
    earth = EarthModel(earth_model)
    a = earth.a
    b = earth.b
    f = earth.f

    def correct_pole(lat: FloatNumber) -> float:
        # correct for errors at exact poles by adjusting 0.6 millimeters:
        if np.absolute(np.pi/2-np.absolute(lat1)) < 1e-10:
            return math.copysign(np.pi/2-(1e-10), lat1)
        else:
            return float(lat)

    # fix Pole
    lat1 = correct_pole(lat1)
    lat2 = correct_pole(lat2)

    U1 = np.arctan((1 - f) * np.tan(lat1))
    U2 = np.arctan((1 - f) * np.tan(lat2))
    L = long2 - long1 # type: ignore
    Lambda = L

    sinU1 = math.sin(U1)
    cosU1 = math.cos(U1)
    sinU2 = math.sin(U2)
    cosU2 = math.cos(U2)

    for _ in range(nb_iter):
        sinLambda = math.sin(Lambda)
        cosLambda = math.cos(Lambda)
        sinSigma = math.sqrt((cosU2 * sinLambda) ** 2 +
                             (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2)
        if sinSigma == 0:
            return 0.0  # coincident points
        cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
        sigma = math.atan2(sinSigma, cosSigma)
        sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
        cosSqAlpha = 1 - sinAlpha ** 2
        try:
            cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha
        except ZeroDivisionError:
            cos2SigmaM = 0
        C = f / 16 * cosSqAlpha * (4 + f * (4 - 3 * cosSqAlpha))
        LambdaPrev = Lambda
        Lambda = L + (1 - C) * f * sinAlpha * (sigma + C * sinSigma *
                                               (cos2SigmaM + C * cosSigma *
                                                (-1 + 2 * cos2SigmaM ** 2)))
        if abs(Lambda - LambdaPrev) < CONVERGENCE_THRESHOLD:
            break  # successful convergence
    else:
        raise RuntimeError("Range Calculation - Impossible to coverge")

    uSq = cosSqAlpha * (a ** 2 - b ** 2) / (b ** 2)
    A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
    B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
    deltaSigma = (B * sinSigma * (cos2SigmaM + B / 4 * (cosSigma *
                  (-1 + 2 * cos2SigmaM ** 2) - B / 6 * cos2SigmaM *
                  (-3 + 4 * sinSigma ** 2) * (-3 + 4 * cos2SigmaM ** 2))))
    s = b * A * (sigma - deltaSigma)

    return round(s, 4)
