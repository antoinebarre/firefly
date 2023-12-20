""" Collection of data types used by firefly package"""

from typing import Annotated, NamedTuple, Union
from beartype.vale import Is
import numpy as np


class EllipsoidParameters(NamedTuple):
    name: str
    semiMajorAxis: float
    flattening: float
    j2: float
    earth_rotation_rate: float


FloatNumber = Union[float, np.float64]


Float64Array3 = Annotated[
    np.ndarray,
    Is[
        lambda array: (
            array.shape == (3,) and
            np.issubdtype(array.dtype, np.float64)
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
