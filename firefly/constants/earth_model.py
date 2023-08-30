# IMPORTED MODULES
import math
from pydantic import BaseModel, ConfigDict

from firefly.settings import DEFAULT_EARTH_MODEL
from firefly.types import EllipsoidParameters

__all__ = [
    "EarthModel",
]

# ------------------------  EARTH MODELS  ------------------------
AVAILABLE_ELLIPSOIDS = {
    "WGS84": EllipsoidParameters(
        name="WGS84",
        semiMajorAxis=6378137.0,
        flattening=1/298.257223563,
        j2=1.08263E-3,
        ),
    "SPHERICAL": EllipsoidParameters(
        name="SPHERICAL",
        semiMajorAxis=6378137.0,
        flattening=0.0,
        j2=0.0,
    )
    }


class EarthModel(BaseModel):
    """Earth Model Class used to model the Earth Ellipsoid and associated
    characteristic
    """
    name: str
    semiMajorAxis: float
    flattening: float
    j2: float
    earth_rotation_rate: float = 72.92115E-6  # rotation rate rad/s
    mu: float = 3.986004418E14  # m-3s-2

    # -------------------------- CONFIGURATION ------------------------- #
    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True,
        frozen=True,
        )

    # ----------------------------- CREATOR ---------------------------- #

    def __init__(self, model: str = DEFAULT_EARTH_MODEL) -> None:
        """Create Earth Model Object

        Args:
            model (str, optional): ellipsoid model name. Defaults to WGS84.
        """
        try:
            earth_model = AVAILABLE_ELLIPSOIDS[model]
        except KeyError:
            msg = (
                f"the model value {model} is not an appropriate model. "
                f"Available models: {list(AVAILABLE_ELLIPSOIDS.keys())}"
                )
            raise ValueError(msg)
        super().__init__(**earth_model._asdict())

    # --------------------------- PROPERTIES --------------------------- #
    @property
    def a(self) -> float:
        """semi major axis value of the ellispoid in meters

        Returns:
            float: semi major axis value of the ellispoid in meters
        """
        return self.semiMajorAxis

    @property
    def f(self) -> float:
        """flattening of the ellispoid

        Returns:
            float: flattening of the ellispoid (SI)
        """
        return self.flattening

    @property
    def b(self) -> float:
        """Semi minor acis of the ellispoid in meters

        Returns:
            float: Semi minor acis of the ellispoid in meters
        """
        return (1-self.f)*self.a

    @property
    def e(self) -> float:
        """Excentricity of the ellispoid

        Returns:
            float: Excentricity of the ellispoid (SI)
        """
        return math.sqrt((self.a**2-self.b**2)/self.a**2)