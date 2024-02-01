

from pydantic import BaseModel, Field, validator,field_validator

# element status
from enum import StrEnum, auto, Enum

class ElementStatus(StrEnum):
    """Enum class for element status."""
    ACTIVE = auto()
    INACTIVE = auto()
    EJECTED = auto()



class RocketElement(BaseModel):
    """Base class for all rocket elements."""
    name: str = Field(...,
                      description="Name of the element.")
    dry_mass: float = Field(...,
                            description="Dry mass of the element.")
    status: ElementStatus = Field(
        default=ElementStatus.INACTIVE,
        description="Status of the element.")

    @field_validator('dry_mass')
    @classmethod
    def dry_mass_must_be_positive(cls, v):
        """Validator to check if dry mass is positive."""
        if v <= 0:
            raise ValueError('dry mass must be positive')
        return v

    def activate(self):
        """Activate the element."""
        self.status = ElementStatus.ACTIVE

    def eject(self):
        """Eject the element."""
        self.status = ElementStatus.EJECTED

    def total_mass(self):
        """Return the total mass of the element."""
        return self.dry_mass

class Propeler(RocketElement):
    """Propeler class"""
    thrust: float = Field(...,
                          description="Thrust of the propeler.")
    @field_validator('thrust')
    @classmethod
    def thrust_must_be_positive(cls, v):
        """Validator to check if thrust is positive."""
        if v <= 0:
            raise ValueError('thrust must be positive')
        return v

    def total_mass(self):
        """Return the total mass of the element."""
        return self.dry_mass + self.thrust

if __name__ == "__main__":

    elt1 = RocketElement(name="test", dry_mass=1.0)
    print(elt1)
    elt1.activate()
    print(elt1)
    
    elt2 = Propeler(name="test propeler", dry_mass=1.0, thrust=2.0)
    print(elt2)
    print(elt2.total_mass())
