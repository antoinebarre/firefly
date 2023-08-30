""" ##################  UNITEST FOR GRAVITY  ##################
"""

# MODULE IMPORT
from firefly.geography.position import Position
from firefly.geography.gravity import gravity
import numpy as np


ABSOLUTE_TOLERANCE = 1e-12
RELATIVE_TOLERANCE = 1e-6


def test_equator_WGS84():

    g_expected = [-9.814197355899799, 0., 0.]

    pos2test = Position.from_LLA(0., 0., 0.)

    g_list = gravity(position=pos2test)

    np.testing.assert_allclose(
            g_list,
            g_expected,
            atol=ABSOLUTE_TOLERANCE,
            rtol=RELATIVE_TOLERANCE)


def test_NorthPole_WGS84():

    g_expected = [0., 0., -9.83206684120325]
    g_list = gravity(
        position=Position.from_LLA(np.deg2rad(90), 0., 0.)
        )
    np.testing.assert_array_almost_equal(
        g_list,
        g_expected)