"""Module to create an overlay plot for firefly package."""

from pathlib import Path

from matplotlib import pyplot as plt
from numpy.typing import NDArray

from firefly.validation.fileIO import increment_file_name, validate_file_extension
from firefly.validation.numpy import validate_numpy_vector

def plot_line(*,
    x_data: NDArray, y_data: NDArray, x_label: str, y_label: str,
    title: str, file: Path,
    line_style: str = '-', color: str = "black",marker_style: str = 'o'
) -> Path:
    """
    Plot a line graph.

    Args:
        x_data (ndarray): The x-axis data.
        y_data (ndarray): The y-axis data.
        x_label (str): The label for the x-axis.
        y_label (str): The label for the y-axis.
        title (str): The title of the graph.
        file (Path): The file path to save the graph.
        line_style (str, optional): The line style. Defaults to '-'.
        color (str, optional): The color of the line. Defaults to "black".
        marker_style (str, optional): The marker style. Defaults to 'o'.

    Returns:
        None
    """
    #validation
    file = validate_file_extension(file, [".png"])
    new_file_path = increment_file_name(file)

    x_data = validate_numpy_vector(x_data)
    y_data = validate_numpy_vector(y_data)
    if x_data.size != y_data.size:
        raise ValueError(
            f"x_data and y_data must have the same size. Got {x_data.size} and {y_data.size}")

    #plot
    plt.figure()
    plt.plot(
        x_data, y_data,
        linestyle=line_style, color=color, linewidth=3,
        markersize=6, marker=marker_style,)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid()
    plt.savefig(new_file_path)
    plt.close()
    return new_file_path
