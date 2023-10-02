"""
--------------   GRAVITY MODEL  --------------
"""

# EXPORT
__all__ = [
    "gravity",
]


from firefly.geography.position import Position
from firefly.constants.earth_model import EarthModel
from firefly.settings import DEFAULT_EARTH_MODEL


def gravity(
        position: Position,
        earth_model: str = DEFAULT_EARTH_MODEL)-> list[float]:

    # get gravitation parameter
    earth = EarthModel(earth_model)

    # get constant
    a = earth.a
    mu = earth.mu
    J2 = earth.j2

    # get norm of ECEF coordinate
    r = position.norm

    gx = -mu/r**2*(1+3/2*J2*(a/r)**2*(1-5*(position.z/r)**2))*position.x/r
    gy = -mu/r**2*(1+3/2*J2*(a/r)**2*(1-5*(position.z/r)**2))*position.y/r
    gz = -mu/r**2*(1+3/2*J2*(a/r)**2*(3-5*(position.z/r)**2))*position.z/r

    return [gx, gy, gz]