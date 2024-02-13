

from pathlib import Path
import attrs


@attrs.define
class AdditionalFile():
    original_path: Path = attrs.field(
        validator=attrs.validators.instance_of(Path),
        metadata={'description': 'Original path of the file'},
        kw_only=True)
    published_directory: str = attrs.field(
        validator=attrs.validators.instance_of(str),
        metadata={
            'description': 'Directory where the file will be published within the HTML report'
            },
        kw_only=True)

    @property
    def filename(self) -> str:
        """
        Returns the name of the file associated with this object.

        :return: The name of the file.
        :rtype: str
        """
        return self.original_path.name
