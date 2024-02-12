

from abc import ABC, abstractmethod


class BasicElement(ABC):
    """
    Abstract base class for all rocket elements.
    """
    @abstractmethod
    def publish(self) -> str:
        """
        Publishes the description of the element.

        Returns:
            str: The published element.
        """

class RocketElement(BasicElement):
    """
    Represents a rocket element.
    """

    @abstractmethod
    def initial_mass(self) -> float:
        """
        Returns the initial mass of the element.

        Returns:
            float: The initial mass of the element.
        """

# @dataclass
# class RocketStage():
#     _: KW_ONLY
#     stage_name: Optional[str] = None
#     motor: str
#     guidance: GuidanceLaw
#     drymass: float