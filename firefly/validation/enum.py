
from enum import Enum

class DetailledEnum(Enum):
    """
    A detailed enumeration class that provides additional functionality.

    This class extends the built-in Enum class and provides a custom _missing_ method
    to handle missing enum values.

    Attributes:
        - ...

    Methods:
        - ...
    """

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
                f"{value} is not a valid {cls.__name__}. " \
                f"Valid types: {', '.join([repr(m.value) for m in cls])}")
