

from abc import ABC, abstractmethod
from dataclasses import KW_ONLY, dataclass
from typing import Optional

from firefly.rocket.guidance import GuidanceLaw


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


# @dataclass
# class RocketStage():
#     _: KW_ONLY
#     stage_name: Optional[str] = None
#     motor: str
#     guidance: GuidanceLaw
#     drymass: float