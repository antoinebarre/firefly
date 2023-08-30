"""
# ===================== UNIT TEST FOR Position Class ==================== #
"""

# MODULE IMPORT
from firefly.geography.position import Position
import pytest
import numpy as np

# CONSTANTS
ABSOLUTE_TOLERANCE = 1e-12
RELATIVE_TOLERANCE = 1e-6


SIMPLE_LIST = [10, 20, 30]

# from https://www.convertecef.com
LLA4ECEF = [
    {"ECEF": [5117118.21, -1087677.05, 3638574.7],  # meter,meter, meter
     "LLA": [35., -12., 1234.]},  # lat lon alt (deg,deg,m)
    {"ECEF": [1193872.96, 1584322.93, -6064737.91],
     "LLA": [-72., 53., 22135.]}]


@pytest.fixture
def simple_position():
    return Position(SIMPLE_LIST[0],
                    SIMPLE_LIST[1],
                    SIMPLE_LIST[2])


def test_creation(simple_position) -> None:
    """Check creation of the Position object with the appropriate fields
    ie. x, y, z
    Args:
        simple_position (NOne): Fixture
    """

    # launch comparisons
    compare_ECEF(simple_position, SIMPLE_LIST)


def test_modif_X(simple_position):
    """x field shall be a float or equivalent (e.g. '1', 1.0, 1"""

    # Error shall be raised (bad value for the interface)
    with pytest.raises(Exception):
        simple_position.x = [1, 2]

    with pytest.raises(Exception):
        simple_position.x = (1, 2)

    with pytest.raises(Exception):
        simple_position.x = "abc"

    # No error shall be raised
    try:
        simple_position.x = 1.6

        assert simple_position.x == 1.6

    except Exception as exc:
        assert False, f"mutation of x raised an exception {exc}"

##############################################################################


def test_toLLA():

    for pos in LLA4ECEF:
        newPos = Position(*pos["ECEF"])

        # check good creation :
        compare_ECEF(newPos, pos["ECEF"])

        # create LLA
        LLA_real = newPos.as_LLA()

        # assess LLA
        compare_LLA(LLA_real, pos["LLA"])


def test_FromLLA():
    for pos in LLA4ECEF:
        newPos = Position.from_LLA(
            np.deg2rad(pos["LLA"][0]),
            np.deg2rad(pos["LLA"][1]),
            pos["LLA"][2])

        # compare ECEF
        compare_ECEF(newPos, pos["ECEF"])

# ------------------------------ OPERATION ------------------------------ #


def test_repr():
    # assert repr feature

    assert (
        repr(Position(0, 0, 0)) ==
        'ECEF Coordinates:\nx : 0.0\ny : 0.0\nz : 0.0')


def test_equality():

    chk = Position.from_LLA(
        np.deg2rad(45),
        np.deg2rad(-45),
        0.) == Position.from_LLA(
        np.deg2rad(45),
        np.deg2rad(-45),
        0.)

    assert chk is True

    chk = Position.from_LLA(
        np.deg2rad(45),
        np.deg2rad(-44),
        0.
        ) == Position.from_LLA(
        np.deg2rad(45),
        np.deg2rad(-45),
        0.)

    assert chk is False

    # check mutation raised error
    with pytest.raises(NotImplementedError):
        Position(0, 0, 0) == 1


def test_sub():
    pos1 = Position(1, 2, 3)
    pos2 = Position(1, 1, 1)

    delta = pos1-pos2

    assert delta == Position(0, 1, 2)

    # check mutation raised error
    with pytest.raises(NotImplementedError):
        Position(0, 0, 0)-1

# -------------------------------- UTILS -------------------------------- #


def compare_ECEF(
        position,
        X_expected,
        absTol=ABSOLUTE_TOLERANCE,
        reltol=RELATIVE_TOLERANCE):
    """Utility function used to compare a position vs the root data"""

    # extract fields
    X = [position.x,
         position.y,
         position.z]

    axes = ["x", "y", "z"]
    for idx in range(3):
        message = f"{axes[idx]} [{X[idx]}] shall be equal to the expected {axes[idx]} [{X_expected[idx]}]\n" + \
                    f"With the Absolute tolerance : {absTol}  and the relative tolerance {reltol}"

        assert X[idx] == pytest.approx(
            X_expected[idx],
            abs=absTol,
            rel=reltol), message


def compare_LLA(LLA_real,
                LLA_expected,
                absTol=ABSOLUTE_TOLERANCE,
                reltol=RELATIVE_TOLERANCE):

    typeLLA = ["Latitude", "Longiture", "Altidue"]

    # change from rad to deg
    LLA_real = [
        np.rad2deg(LLA_real[0]),
        np.rad2deg(LLA_real[1]),
        LLA_real[2]]

    for idx in range(3):
        message = f"{typeLLA[idx]} [{LLA_real[idx]}] shall be equal to the expected {typeLLA[idx]} [{LLA_expected[idx]}]\n" + \
                    f"With the Absolute tolerance : {absTol}  and the relative tolerance {reltol}"

        assert LLA_real[idx] == pytest.approx(
            LLA_expected[idx],
            abs=absTol,
            rel=reltol), message
