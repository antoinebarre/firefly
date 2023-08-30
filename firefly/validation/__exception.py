"""Firefly - Generic Exception for the validation"""

from typing import Any, Type
from firefly.exception import FireflyException

class FireflyTypeError(FireflyException):
    def __init__(
            self,
            currentValue: Any,
            expectedValueType : Type
            ) -> None:

        msg = (
            "The argument type is not valid. "
            f"[Expect type : {expectedValueType}, "
            f"Current type :{type(currentValue)}\n"
            )
        self.message = msg
        super().__init__(self.message)
    
class FireflyValueError(FireflyException):
    def __init__(
            self,
            currentValue: Any,
            expectedProperty : str
            ) -> None:

        msg = (
            "The argument property is not valid. "
            f"[Expect type : {expectedProperty}, "
            f"Current type :{currentValue}\n"
            )
        self.message = msg
        super().__init__(self.message)