""" Collection of data types used by firefly package"""

from typing import Annotated, NamedTuple, Union
from beartype.vale import Is
import numpy as np


class EllipsoidParameters(NamedTuple):
    """
    NamedTuple representing the parameters of an ellipsoid.

    Attributes:
        name (str): The name of the ellipsoid.
        semiMajorAxis (float): The semi-major axis of the ellipsoid.
        flattening (float): The flattening of the ellipsoid.
        j2 (float): The J2 coefficient of the ellipsoid.
        earth_rotation_rate (float): The Earth rotation rate.
    """
    name: str
    semiMajorAxis: float
    flattening: float
    j2: float
    earth_rotation_rate: float


FloatNumber = Union[float, np.float64]

FloatInt = Union[float, int, np.float64, np.int64]

FloatVector = Union[np.ndarray, list]


Float64Array3 = Annotated[
    np.ndarray,
    Is[
        lambda array: (
            array.shape == (3,) and
            np.issubdtype(array.dtype, np.float64)
            )
        ]
    ]

Vector = Annotated[
    np.ndarray,
    Is[lambda array: (
        array.ndim == 1 and
        (np.issubdtype(array.dtype, np.float64) or
        np.issubdtype(array.dtype, np.int64))
        )
       ]
        ]

Float641DVector = Annotated[
    np.ndarray,
    Is[
        lambda array: (
            array.ndim == 1 and
            np.issubdtype(array.dtype, np.float64)
            )
        ]
    ]

Float64Matrix_3x3 = Annotated[
    np.ndarray,
    Is[
        lambda array: (
            array.shape == (3, 3) and
            np.issubdtype(array.dtype, np.float64)
            )
        ]
    ]
