""" Collection of data types used by firefly package"""

from typing import Annotated
from beartype.vale import Is
import numpy as np


Float64Array3 = Annotated[np.ndarray, Is[lambda array:
    array.shape == (3,) and np.issubdtype(array.dtype, np.float64)]]