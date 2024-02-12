


from pydantic import BaseModel, Field
from firefly.rocket.elements import RocketElement
import firefly.rocket.propulsion.flow_rate as FlowRate
import firefly.rocket.propulsion.specific_impulse as SpecificImpulse

# Constant Values
G0 = 9.80665 # gravity for the thrust calculation


class Motor(RocketElement,BaseModel):
    motor_name: str
    motor_description: str = ""
    vacuum_specific_impulse: SpecificImpulse.SpecificImpulse
    flow_rate: FlowRate.FlowRate
    dry_mass: float = Field(..., gt=0, description="The dry mass of the motor in kg.")
    nozzle_exit_area: float = Field(..., gt=0, description="The nozzle exit area in m^2.")

    # unmutable parameter
    g0 : float = 9.80665

    def publish(self) -> str:
        return "toto"

    def initial_mass(self) -> float:
        return self.dry_mass

    @property
    def combustion_duration(self):
        """
        Returns the maximum combustion duration of the motor's flow rate.
        """
        return self.flow_rate.max_combustion_duration

    @property
    def total_consummed_propellant_mass(self):
        """
        Calculates the total mass of propellant consumed by the motor.

        Returns:
            The total mass of propellant consumed by the motor.
        """
        return self.flow_rate.get_total_propellant_mass()


    def vacuum_thrust(self, time_since_ignition: float) -> float:
        """
        Calculate the vacuum thrust of the motor at a given time since ignition.

        Parameters:
        - time_since_ignition (float): The time elapsed since the motor ignition.

        Returns:
        - float: The vacuum thrust of the motor.
        """
        return G0 * \
            self.flow_rate.get_current(time_since_ignition) * \
                self.vacuum_specific_impulse.get_current(time_since_ignition)

    def thrust(self, time_since_ignition: float, ambient_pressure: float = 101325) -> float:
        """
        Calculate the thrust produced by the motor.

        Parameters:
        - time_since_ignition (float): The time since the motor ignition in seconds.
        - ambient_pressure (float): The ambient pressure in Pascals. Default value is 101325.

        Returns:
        - float: The thrust produced by the motor in Newtons.
        """
        return self.vacuum_thrust(time_since_ignition) - ambient_pressure * self.nozzle_exit_area

    def consummed_propellant_mass(self, time_since_ignition: float) -> float:
        return self.flow_rate.get_current_used_propellant_mass(
            time_since_ignition=time_since_ignition
        )

if __name__ == "__main__":
    motor = Motor(
        motor_name="AeroTech K535",
        vacuum_specific_impulse=SpecificImpulse.ConstantSpecificImpulse(specific_impulse=250),
        flow_rate=FlowRate.ConstantFlowRate(flow_rate=0.5,combustion_duration=100),
        dry_mass= 100,
        nozzle_exit_area=0.01)
    print(motor)
    print(motor.motor_name)
    print(motor.motor_description)
    print(motor.vacuum_specific_impulse)
    print(motor.flow_rate)
    print(motor.thrust(105))