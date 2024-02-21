"""Collection of image components."""

from pathlib import Path
import attrs
from firefly.tools.strings import add_unique_suffix
from .components import AdditionalFile
from .components import HTMLComponent
from ._render_tools import create_block

__all__ = ["Image"]

@attrs.define
class Image(HTMLComponent):  # pylint: disable=invalid-name
    """
    Represents an image component that can be displayed in HTML.

    Attributes:
        image_path (Path): The path to the image file to be displayed.
        alt_text (str): The alternative text for the image.
        width (int): The width of the image.
        height (int): The height of the image.
        _unique_filename (str): The unique filename for the image.

    Constants:
        _ImageFolder (str): The folder where the images are stored.
        __valid_extensions (list[str]): The list of valid image file extensions.

    Methods:
        __attrs_post_init__: Performs post-initialization checks and sets the unique filename.
        render: Renders the component and returns the generated HTML string.
        get_additional_files: Returns a list of additional files associated with the image.
    """
    image_path: Path = attrs.field(
        metadata={'description': 'The path to the image file to be displayed'},
        validator=attrs.validators.instance_of(Path),
        kw_only=True)
    alt_text: str = attrs.field(
        metadata={'description': 'The alternative text for the image and legend for the image'},
        validator=attrs.validators.instance_of(str),
        kw_only=True)
    width: int = attrs.field(
        default=None,
        metadata={'description': 'The width of the image'},
        validator=attrs.validators.optional(attrs.validators.instance_of(int)),
        kw_only=True)
    height: int = attrs.field(
        default=None,
        metadata={'description': 'The height of the image'},
        validator=attrs.validators.optional(attrs.validators.instance_of(int)),
        kw_only=True)
    _unique_filename: str = attrs.field(
        metadata={'description': 'The unique filename for the image'},
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        kw_only=True,
        init=False)
    legend: str = attrs.field(
        default=None,
        metadata={'description': 'The legend for the image'},
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        kw_only=True)

    # constants
    _ImageFolder = "images"
    __valid_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]

    def __attrs_post_init__(self):
        # check if the image path is valid
        if not self.image_path.exists():
            raise FileNotFoundError(f"Image file {self.image_path} does not exist")

        # check the image file extension
        if self.image_path.suffix not in self.__valid_extensions:
            raise ValueError(
                f"Image file {self.image_path} has an invalid extension" +
                f"Valid extensions are {', '.join(self.__valid_extensions)}")

        # create the unique filename for the outputs
        self._unique_filename = add_unique_suffix(self.image_path.stem) + self.image_path.suffix

    def render(self) -> str:
        """
        Renders the component and returns the generated HTML string.

        Returns:
            str: The generated HTML string.
        """

        # optional width and height
        width = f' width="{self.width}"' if self.width else ""
        height = f' height="{self.height}"' if self.height else ""

        # create img info
        img_attributes =f'<img src="{self._ImageFolder}/{self._unique_filename}"' + \
                            f' alt="{self.alt_text}"{width}{height}>'

        # create figcaption info
        figcaption = create_block(
            open_prefix="<figcaption>",
            close_suffix="</figcaption>",
            content=self.legend,
            inline=True
        ) if self.legend else ""

        # create the figure
        return create_block(
            open_prefix="<figure>",
            close_suffix="</figure>",
            content=f"{img_attributes}\n{figcaption}",
            inline=False
        )

    def get_additional_files(self) -> list[AdditionalFile]:
        """
        Returns a list of additional files associated with the image.

        Returns:
            list[AdditionalFile]: The list of additional files.
        """
        return [
            AdditionalFile(
                original_path=self.image_path,
                published_directory=self._ImageFolder,
                published_filename=self._unique_filename
            )
        ]
