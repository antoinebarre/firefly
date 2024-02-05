

from dataclasses import KW_ONLY, dataclass
from typing import Optional

from firefly.rocket.guidance import GuidanceLaw


@dataclass
class RocketStage():
    _: KW_ONLY
    stage_name: Optional[str] = None
    motor: Motor
    guidance: GuidanceLaw
    drymass: float