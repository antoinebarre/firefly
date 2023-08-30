"""
firefly - Math - Basic Rotations matrix tools
"""

# -------------------------------- EXPORT ------------------------------- #
__all__ = [
    "rotx",
    "roty",
    "rotz",
]

# -------------------------------- IMPORT ------------------------------- #
from typing import Union
from beartype import beartype
import numpy as np
from scipy.spatial.transform import Rotation
from ..types import Float64Array3


def rotx(theta: Union[float, np.float64]) -> np.ndarray:
    """Generate a rotation matrix for a rotation around the X-axis.

    Args:
        theta (float, np.float64): Angle in radians for the rotation.

    Returns:
        np.ndarray: 3x3 rotation matrix representing the rotation around
        the X-axis.
    """
    return __fundamentalRotation(np.array([1.0, 0, 0]), theta)


def roty(theta: Union[float, np.float64]) -> np.ndarray:
    """Generate a rotation matrix for a rotation around the Y-axis.

    Args:
        theta (float, np.float64): Angle in radians for the rotation.

    Returns:
        np.ndarray: 3x3 rotation matrix representing the rotation around
        the Y-axis.
    """
    return __fundamentalRotation(np.array([0, 1.0, 0]), theta)


def rotz(theta: Union[float, np.float64]) -> np.ndarray:
    """Generate a rotation matrix for a rotation around the Z-axis.

    Args:
        theta (float, np.float64): Angle in radians for the rotation.

    Returns:
        np.ndarray: 3x3 rotation matrix representing the rotation
        around the Z-axis.
    """
    return __fundamentalRotation(np.array([0, 0, 1.0]), theta)


@beartype
def __fundamentalRotation(
        axis: Float64Array3,
        theta: Union[float, np.float64]
        ) -> np.ndarray:
    """Create a rotation matrix based on angle and axis.

    Args:
        axis (Float64Array3): The rotation axis as a 3D vector.
        theta (float, np.float64): Angle in radians for the rotation.

    Returns:
        np.ndarray: 3x3 rotation matrix.
    """
    theta = float(theta)
    return Rotation.from_rotvec(theta * axis.reshape((3,))).as_matrix().T
