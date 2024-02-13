


from abc import ABC, abstractmethod
from pathlib import Path

import attrs

from ..tools.additionalFile import AdditionalFile

@attrs.define
class HTMLComponent(ABC):
    """
    Base class for HTML components.
    """
    _indent_value: int = 4

    @abstractmethod
    def render(self) -> str:
        """
        Renders the HTML component.

        Returns:
            str: The rendered HTML.
        """

    @abstractmethod
    def publish_additional_files(self, path:Path) -> list[AdditionalFile]:
        """
        Publishes additional files required by the HTML component.

        Args:
            path (Path): The path where the additional files should be published.
        """