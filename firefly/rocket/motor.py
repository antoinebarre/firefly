
from abc import ABC, abstractmethod
from dataclasses import dataclass, KW_ONLY
from typing import Optional

from pydantic import BaseModel, validator
from firefly.rocket.flow_rate import ConstantFlowRate, FlowRate
from firefly.rocket.specific_impulse import ConstantSpecificImpulse, SpecificImpulse




class Motor(BaseModel):
    _: KW_ONLY
    motor_name: str
    vaccum_specific_impulse: SpecificImpulse
    flow_rate: FlowRate
    dry_mass: float # kg
    propellant_mass: float # kg
    combustion_duration: float # seconds
    time_since_ignition: float = 0.0 # seconds


    @validator('vaccum_specific_impulse')
    @classmethod
    def validate_vaccum_specific_impulse(cls, v):
        """
        Validate the vacuum specific impulse.

        Parameters:
        - v (SpecificImpulse): The vacuum specific impulse to validate.

        Returns:
        - SpecificImpulse: The validated vacuum specific impulse.

        Raises:
        - TypeError: If v is not an instance of SpecificImpulse.
        """
        if not isinstance(v, SpecificImpulse):
            raise TypeError('vaccum_specific_impulse must be a SpecificImpulse instance')
        # Add more validation if needed
        return v

    @validator('flow_rate')
    @classmethod
    def validate_flow_rate(cls, v):
        """
        Validate the flow rate.

        Parameters:
        - v (FlowRate): The flow rate to validate.

        Returns:
        - FlowRate: The validated flow rate.

        Raises:
        - TypeError: If v is not an instance of FlowRate.
        """
        if not isinstance(v, FlowRate):
            raise TypeError('flow_rate must be a FlowRate instance')
        # Add more validation if needed
        return v

#     @abstractmethod
#     def get_propulsion_force(
#         self,
#         time_since_ignition: float
#         ) -> float:
#         """
#         Abstract method to get the propulsion force at a given time since ignition.

#         Args:
#             time_since_ignition (float): The time since ignition.

#         Returns:
#             float: The propulsion force at the given time since ignition.
#         """

# class NoMotor(Motor):
#     def __init__(
#         self,
#         *,
#         motor_name: Optional[str] = None,
#         dry_mass: float = 0.0,
#         ):
#         super().__init__(
#             motor_name=motor_name,
#             vaccum_specific_impulse=SpecificImpulse.create_constant_impulse(0.0, 0.0),
#             flow_rate=FlowRate.create_constant_flow_rate(0.0,0.0),
#             dry_mass=dry_mass,
#             propellant_mass=0.0,
#             combustion_duration=0.0
#             )

#     def get_propulsion_force(
#         self,
#         time_since_ignition: float
#         ) -> float:
#         return 0.0

class ConcreteFlowRate(ConstantFlowRate):
    def __init__(self, flow_rate: float, combustion_duration: float):
        super().__init__(flow_rate, combustion_duration)

    def calculate_flow(self, time_since_ignition: float) -> float:
        # Implement the calculation logic for the flow rate
        pass

if __name__=="__main__":
    print("This is the motor module.")

    m1 = Motor(
        motor_name="Test Motor",
        vaccum_specific_impulse=ConstantSpecificImpulse(specific_impulse=100.0),
        flow_rate=ConcreteFlowRate(flow_rate=10.0, combustion_duration=100.0),
        dry_mass=100.0,
        propellant_mass=100.0,
        combustion_duration=100.0
    )
