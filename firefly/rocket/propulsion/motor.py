


from pydantic import BaseModel
from firefly.rocket.elements import BasicElement

from firefly.rocket.propulsion.specific_impulse import SpecificImpulse


class Motor(BasicElement,BaseModel):
    motor_name: str
    motor_description: str = ""
    vacuum_specific_impulse: SpecificImpulse
    