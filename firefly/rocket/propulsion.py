"""Propulsion module with all objects related to propulsion."""

import timeit
import numpy as np


from firefly.math.interp1D import Interp1D
from firefly.types import FloatInt, Vector

# ============================ MOTOR TIMED DATA ============================ #

# The start time for all timed data
START_TIME = 0.0 # [s]

class GenericTimedData(Interp1D):
    """Generic timed data interpolation for propulsion data"""
    def __init__(self, times: Vector, values: Vector):
        """
        Initialize the GenericTimedData instance.

        Args:
            times (Vector): The time values for the data.
            values (Vector): The values corresponding to the time values.

        Raises:
            ValueError: If the first time value is not 0.
        """

        # validation of the time values
        if times[0] != START_TIME:
            raise ValueError(f"The first time value must be {START_TIME} [s]")

        # NB: the size of the time and value vectors is not checked since it is done by interp1D

        super().__init__(times, values)

    @classmethod
    def create_constant_value(
            cls,
            value:float,
            t_end_combustion:float)-> 'GenericTimedData':
        """
        Create a GenericTimedData instance with a constant value.

        Args:
            value (float): The constant value.
            t_end_combustion (float): The time at which the combustion ends.

        Returns:
            GenericTimedData: An instance of the GenericTimedData class with a constant value.

        """
        return cls(
            times=np.array([START_TIME,t_end_combustion]),
            values=np.array([value,value]))

    @classmethod
    def create_variable_value(
            cls,
            times:Vector,
            values:Vector)-> 'GenericTimedData':
        """
        Create a GenericTimedData instance with variable values.

        Args:
            times (Vector): The time values for the data.
            values (Vector): The values corresponding to the time values.

        Returns:
            GenericTimedData: An instance of the GenericTimedData class with variable values.

        """
        return cls(
            times=times,
            values=values)

    def current_value(
        self,
        current_time: FloatInt,
        **kwargs,
        ) -> float:
        """
        Get the interpolated current value at a given time.

        Args:
            current_time (FloatInt): The time at which to interpolate the current value.
            **kwargs: Additional keyword arguments to pass to np.interp.

        Returns:
            float: The interpolated current value.

        Raises:
            ValueError: If the current_time is less than the start time.

        """

        if float(current_time) < START_TIME:
            raise ValueError("negative time value is not allowed")

        return self.get_value(current_time,allow_extrapolation=False,**kwargs)

# ========================= SPECIFIC IMPULSE OBJECT ======================== #

class SpecificImpulse(GenericTimedData):
    """
    Specific impulse interpolation.
    This class represents an interpolation of specific impulse values over time.
    It inherits from the GenericTimedData class.
    """
    def __init__(self, times: Vector, ISP: Vector):
        """
        Initialize the SpecificImpulse instance.

        Args:
            times (Vector): The time values for the specific impulse data since
                the ignition of the engine.
            ISP (Vector): The specific impulse values corresponding to the time values.

        """
        super().__init__(times, ISP)

    @classmethod
    def create_constant_impulse(
            cls,
            value:float,
            t_end_combustion:float)-> 'SpecificImpulse':
        """
        Create a SpecificImpulse instance with a constant specific impulse value.

        Args:
            value (float): The constant specific impulse value.
            t_end_combustion (float): The time at which the combustion ends.

        Returns:
            SpecificImpulse: An instance of the SpecificImpulse class with a
            constant specific impulse value.

        """
        return cls(
            times=np.array([START_TIME,t_end_combustion]),
            ISP=np.array([value,value]))

    @classmethod
    def create_variable_impulse(
            cls,
            times:Vector,
            ISP:Vector)-> 'SpecificImpulse':
        """
        Create a SpecificImpulse instance with variable specific impulse values.

        Args:
            times (Vector): The time values for the specific impulse data.
            ISP (Vector): The specific impulse values corresponding to the time values.

        Returns:
            SpecificImpulse: An instance of the SpecificImpulse class with variable
            specific impulse values.

        """
        return cls(
            times=times,
            ISP=ISP)

    def current(self, current_time: FloatInt) -> float:
        """
        Get the interpolated specific impulse value at a given time.

        Args:
            current_time (FloatNumber): The time at which to interpolate the specific impulse value.

        Returns:
            float: The interpolated specific impulse value.

        """
        return self.current_value(current_time)

# ========================= FLOW RATE OBJECT ======================== #

class FlowRate(GenericTimedData):
    """
    Flow rate interpolation.
    This class represents an interpolation of flow rate values over time.
    It inherits from the GenericTimedData class.
    """
    def __init__(self, times: Vector, flow_rate: Vector):
        """
        Initialize the FlowRate instance.

        Args:
            times (Vector): The time values for the flow rate data since
                the ignition of the engine.
            flow_rate (Vector): The flow rate values corresponding to the time values.

        """
        super().__init__(times, flow_rate)

    @classmethod
    def create_constant_flow_rate(
            cls,
            value:float,
            t_end_combustion:float)-> 'FlowRate':
        """
        Create a FlowRate instance with a constant flow rate value.

        Args:
            value (float): The constant flow rate value.
            t_end_combustion (float): The time at which the combustion ends.

        Returns:
            FlowRate: An instance of the FlowRate class with a
            constant flow rate value.

        """
        return cls(
            times=np.array([START_TIME,t_end_combustion]),
            flow_rate=np.array([value,value]))

    @classmethod
    def create_variable_flow_rate(
            cls,
            times:Vector,
            flow_rate:Vector)-> 'FlowRate':
        """
        Create a FlowRate instance with variable flow rate values.

        Args:
            times (Vector): The time values for the flow rate data.
            flow_rate (Vector): The flow rate values corresponding to the time values.

        Returns:
            FlowRate: An instance of the FlowRate class with variable
            flow rate values.

        """
        return cls(
            times=times,
            flow_rate=flow_rate)

    def current(self, current_time: FloatInt) -> float:
        """
        Get the interpolated flow rate value at a given time.

        Args:
            current_time (FloatNumber): The time at which to interpolate the flow rate value.

        Returns:
            float: The interpolated flow rate value.

        """
        return self.current_value(current_time)

    def is_valid(
        self,
        total_propelant_mass: float,
        combustion_time:float) -> bool:
        """
        Check if the flow rate is consistent with the propellant mass.

        Args:
            total_propelant_mass (float): The total propellant mass.
            combustion_time (float): The time at which the combustion ends.

        Returns:
            bool: True if the integrated flow rate is less than or equal
            to the total propellant mass, False otherwise.

        Raises:
            ValueError: If the last time value is not equal to the combustion time.

        """

        if self.x[-1] != combustion_time:
            raise ValueError("The last time value must be equal to the combustion time")

        return self.integrate_all() <= total_propelant_mass


if __name__ == "__main__":

    times = np.array([0, 1, 2])
    flow_rate = np.array([10, 15, 20])
    total_propelant_mass = 44
    combustion_time = 2
    
    flow_rate_instance = FlowRate(times, flow_rate)
    print(flow_rate_instance.is_valid(total_propelant_mass, combustion_time))
    
    print(flow_rate_instance.integrate_all())
    