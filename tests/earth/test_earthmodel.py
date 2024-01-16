"""UNIT TEST FOR EARTH MODEL"""

#Import Module
import pytest
from firefly.earth.earth_model import EarthModel


EXPECTED_VALUES = [
    {"name":"WGS84",
     "a": 6378137.0 ,
     "f": 1/298.257223563,
     "b":6356752.314245179497563967,
     "e": 0.081819190842622,
     "mu":3.986005E+14,
     "j2":1.08263E-3, # SOURCE : https://fr.wikipedia.org/wiki/WGS_84
     "mean_radius": 6371008.7714 # source : https://en.wikipedia.org/wiki/Earth_radius
    }
]



ABSOLUTE_TOLERANCE = 1e-12
RELATIVE_TOLERANCE = 1e-6


def test_earthmodel():
    for model in EXPECTED_VALUES:
        #create EarthModel object

        try:
            model2test = EarthModel(model["name"])
        except Exception as exc:

            assert False, f'creation of the model {model["name"]} raised an error {exc}'


        #check Earth rotation rate
        msg = 'Inapropriate earth rotational rate'
        assert model2test.earth_rotation_rate == pytest.approx(
            7.292115E-5,
                    abs = ABSOLUTE_TOLERANCE,
                    rel=RELATIVE_TOLERANCE), msg

        # check general graivtational constant
        msg = 'Inapropriate gravitational constant'
        assert model2test.mu == pytest.approx(
            model["mu"],
            abs=ABSOLUTE_TOLERANCE,
            rel=RELATIVE_TOLERANCE), msg

        #check j2 gravity
        msg = 'Inapropriate second gravitational constant'
        assert model2test.j2 == pytest.approx(
            model["j2"],
            abs=ABSOLUTE_TOLERANCE,
            rel=RELATIVE_TOLERANCE), msg

        # assert semi major axis
        msg = f'Inapropriate Semi major value for {model["name"]}'
        assert model2test.a== pytest.approx(
            model["a"],abs=ABSOLUTE_TOLERANCE,
            rel=RELATIVE_TOLERANCE), msg

        # assert semi minor axis
        msg = f'Inapropriate Semi minor value for {model["name"]}'
        assert model2test.b== pytest.approx(
            model["b"],abs=ABSOLUTE_TOLERANCE,
            rel=RELATIVE_TOLERANCE), msg

        # assert flattening
        msg = f'Inapropriate flattening value for {model["name"]}'
        assert model2test.f== pytest.approx(model["f"],abs=ABSOLUTE_TOLERANCE,\
            rel=RELATIVE_TOLERANCE), msg

        # assert excentricity axis
        msg = f'Inapropriate excentricity value for {model["name"]}'
        assert model2test.e== pytest.approx(model["e"],\
            abs=ABSOLUTE_TOLERANCE,rel=RELATIVE_TOLERANCE), msg

        # assert mean radius
        msg = f'Inapropriate mean radius value for {model["name"]}'
        assert model2test.mean_radius== pytest.approx(model["mean_radius"],\
            abs=ABSOLUTE_TOLERANCE,rel=RELATIVE_TOLERANCE), msg


def test_earthmodel_error():
    """ assess all possible error of the Earth model"""

    # bad type
    with pytest.raises(ValueError):
        EarthModel(0) # type: ignore

    with pytest.raises(ValueError):
        EarthModel("toto")

    # no error
    EarthModel()
