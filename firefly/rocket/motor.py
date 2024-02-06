"""
Module for defining the Motor class and related models.
"""


from dataclasses import KW_ONLY

from pydantic import BaseModel, Field
from firefly.rocket.flow_rate import ConstantFlowRate, FlowRate
from firefly.rocket.specific_impulse import ConstantSpecificImpulse, SpecificImpulse


class MotorParameter(BaseModel):
    """
    Represents the parameters of a rocket motor.

    Attributes:
        time (float): The time of the motor parameter.
        total_mass (float): The total mass of the motor parameter.
        specific_impulse (float): The specific impulse of the motor parameter.
        flow_rate (float): The flow rate of the motor parameter.
        burn_time (float): The burn time of the motor parameter.
        consummed_propellant_mass (float): The consumed propellant mass of the motor parameter.
        nozzle_exit_area (float): The nozzle exit area of the motor parameter.
    """

    _: KW_ONLY
    time: float = Field(ge=0)
    total_mass: float  = Field(ge=0)
    specific_impulse: float  = Field(ge=0)
    flow_rate: float  = Field(ge=0)
    burn_time: float  = Field(ge=0)
    consummed_propellant_mass: float  = Field(ge=0)
    nozzle_exit_area: float  = Field(ge=0)

    @property
    def vacuum_thrust(self):
        """
        Calculate the vacuum thrust of the motor.

        Returns:
            float: The vacuum thrust of the motor.
        """
        return self.specific_impulse * self.flow_rate

class Motor(BaseModel):
    """
    Represents a rocket motor.

    Attributes:
        motor_name (str): The name of the motor.
        nozzle_exit_area (float): The area of the nozzle exit.
        vaccum_specific_impulse_data (SpecificImpulse): The specific impulse data in vacuum.
        flow_rate_data (FlowRate): The flow rate data.
        dry_mass (float): The dry mass of the motor in kilograms.
    """

    _: KW_ONLY
    motor_name: str = Field(default="Test Motor", validate_default=True)
    nozzle_exit_area: float = Field(ge=0, default=0.0, validate_default=True)
    vaccum_specific_impulse_data: SpecificImpulse
    flow_rate_data: FlowRate
    dry_mass: float = Field(ge=0, default=0.0, validate_default=True)# kg

    @property
    def maximum_combustion_duration(self) -> float:
        """
        Get the maximum combustion duration.

        Returns:
            float: The maximum combustion duration.

        """
        return self.flow_rate_data.max_combustion_duration

    def current_motor_parameter(
        self,
        time,
        ) -> MotorParameter:
        """
        Get the current motor parameter at a given time.

        Args:
            time (float): The time at which to get the motor parameter.

        Returns:
            MotorParameter: The current motor parameter.

        """
        return MotorParameter(
            time=time,
            total_mass=self.dry_mass,
            specific_impulse=self.vaccum_specific_impulse_data.get_current(time),
            flow_rate=self.flow_rate_data.get_current(time),
            consummed_propellant_mass=self.flow_rate_data.get_current_used_propellant_mass(time),
            burn_time=time,
            nozzle_exit_area=self.nozzle_exit_area,
        )


if __name__=="__main__":
    print("This is the motor module.")

    m1 = Motor(
        motor_name="Test Motor",
        vaccum_specific_impulse_data=ConstantSpecificImpulse(specific_impulse=100.0),
        flow_rate_data=ConstantFlowRate(flow_rate=10.0, combustion_duration=100.0),
        dry_mass=100.0,
    )

    print(m1)

    print(m1.current_motor_parameter(15.0))
