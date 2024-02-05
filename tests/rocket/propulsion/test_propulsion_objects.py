import numpy as np
import pytest
from firefly.rocket.propulsion_objects import GenericTimedData, SpecificImpulse, FlowRate


def test_generic_timed_data():
    time_values = np.array([0.0, 1.0, 2.0, 3.0])
    values = np.array([10.0, 20.0, 30.0, 40.0])
    data = GenericTimedData(time_values, values)

    # Test current value at start time
    assert data.current_value(0.0) == 10.0

    # Test current value at middle time
    assert data.current_value(1.5) == 25.0

    # Test current value at end time
    assert data.current_value(3.0) == 40.0

def test_specific_impulse():
    time_values = np.array([0.0, 1.0, 2.0, 3.0])
    isp_values = np.array([200.0, 250.0, 300.0, 350.0])
    isp = SpecificImpulse(time_values, isp_values)

    # Test current value at start time
    assert isp.current(0.0) == 200.0

    # Test current value at middle time
    assert isp.current(1.5) == 275.0

    # Test current value at end time
    assert isp.current(3.0) == 350.0

def test_flow_rate():
    time_values = np.array([0.0, 1.0, 2.0, 3.0])
    flow_rate_values = np.array([5.0, 10.0, 15.0, 20.0])
    flow_rate = FlowRate(time_values, flow_rate_values)

    # Test current value at start time
    assert flow_rate.current(0.0) == 5.0

    # Test current value at middle time
    assert flow_rate.current(1.5) == 12.5

    # Test current value at end time
    assert flow_rate.current(3.0) == 20.0

    # Test is_valid method
    assert flow_rate.is_valid(50.0, 3.0) == True
    assert flow_rate.is_valid(10.0, 3.0) == False

    # Test current_ejected_mass method
    assert flow_rate.current_ejected_mass(0.0) == 0.0
    assert flow_rate.current_ejected_mass(1.5) == 13.125
    assert flow_rate.current_ejected_mass(3.0) == 37.5

