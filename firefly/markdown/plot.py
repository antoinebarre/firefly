"""Plot Markdown Element."""

from dataclasses import KW_ONLY
from pathlib import Path

from matplotlib.figure import Figure
from pydantic import BaseModel, ConfigDict, Field, field_validator

from firefly.markdown.elements import MarkdownContent, MarkdownElement
from firefly.tools.strings import add_unique_suffix


class PlotMarkdown(MarkdownElement, BaseModel):
    """
    Represents a markdown element that contains a plot.

    Attributes:
        model_config (ConfigDict): The model configuration.
        figure (Figure): The plot figure.
        description (str): The description of the plot.
        _plot_folder (str): The folder where the plot file will be saved.
        filename (str): The filename of the plot file.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    _: KW_ONLY
    figure: Figure
    description: str
    _plot_folder: str = "plots"
    filename:str = Field(default_factory=lambda: add_unique_suffix("plot") + ".png")

    @field_validator('figure')
    @classmethod
    def check_figure(cls, v):
        """
        Check if the input is a matplotlib.figure.Figure instance.

        Parameters:
            v (matplotlib.figure.Figure): The input to be checked.

        Raises:
            ValueError: If v is not a matplotlib.figure.Figure instance.

        Returns:
            matplotlib.figure.Figure: The input if it is a valid Figure instance.
        """
        if v is not None and not isinstance(v, Figure):
            raise ValueError('figure must be a matplotlib.figure.Figure instance')
        return v

    def publish(self) -> MarkdownContent:
        """
        Publishes the plot as a Markdown string.

        Returns:
            MarkdownContent: The published plot.
        """
        return MarkdownContent(
            content=f"![{self.description}]({self._plot_folder}/{self.filename})"
        )

    def export_additional_files(self, directory_path: Path) -> list[Path]:
        """
        Exports the plot file.

        Args:
            directory_path (Path): The directory path where the plot file will be exported.

        Returns:
            list[Path]: The list of exported file paths.
        """
        file_path = directory_path / self._plot_folder / self.filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        self.figure.savefig(file_path)
        return [file_path]

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np
    fig, ax = plt.subplots()
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)
    ax.plot(x, y)
    plot_md = PlotMarkdown(figure=fig, description="Sine Wave")
    print(plot_md.publish())
