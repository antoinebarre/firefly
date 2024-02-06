import numpy as np
import pytest
from pathlib import Path
from firefly.plot.line import plot_line

# Constants for tests
VALID_X_DATA = np.array([1, 2, 3])
VALID_Y_DATA = np.array([4, 5, 6])
VALID_X_LABEL = "X Axis"
VALID_Y_LABEL = "Y Axis"
VALID_TITLE = "Test Plot"
VALID_FILE_PATH = Path("/tmp/test_plot.png")
VALID_LINE_STYLE = "--"
VALID_COLOR = "blue"
VALID_MARKER_STYLE = "x"

# Parametrized test cases for happy path, edge cases, and error cases
@pytest.mark.parametrize(
    "x_data, y_data, x_label, y_label, title, file, line_style, color, marker_style, test_id",
    [
        # Happy path tests
        (VALID_X_DATA, VALID_Y_DATA, VALID_X_LABEL, VALID_Y_LABEL, VALID_TITLE, VALID_FILE_PATH, VALID_LINE_STYLE, VALID_COLOR, VALID_MARKER_STYLE, "happy_path_default"),
        (VALID_X_DATA, VALID_Y_DATA, VALID_X_LABEL, VALID_Y_LABEL, VALID_TITLE, VALID_FILE_PATH, "-", "red", "*", "happy_path_varied_styles"),

        # Edge cases
        (np.array([]), np.array([]), VALID_X_LABEL, VALID_Y_LABEL, VALID_TITLE, VALID_FILE_PATH, VALID_LINE_STYLE, VALID_COLOR, VALID_MARKER_STYLE, "edge_case_empty_data"),
        (np.array([1]), np.array([1]), VALID_X_LABEL, VALID_Y_LABEL, VALID_TITLE, VALID_FILE_PATH, VALID_LINE_STYLE, VALID_COLOR, VALID_MARKER_STYLE, "edge_case_single_point"),

        # Error cases
        (VALID_X_DATA, np.array([4, 5]), VALID_X_LABEL, VALID_Y_LABEL, VALID_TITLE, VALID_FILE_PATH, VALID_LINE_STYLE, VALID_COLOR, VALID_MARKER_STYLE, "error_case_mismatched_sizes"),
        (VALID_X_DATA, VALID_Y_DATA, VALID_X_LABEL, VALID_Y_LABEL, VALID_TITLE, Path("/tmp/test_plot.jpg"), VALID_LINE_STYLE, VALID_COLOR, VALID_MARKER_STYLE, "error_case_invalid_file_extension"),
    ]
)
def test_plot_line(x_data, y_data, x_label, y_label, title, file, line_style, color, marker_style, test_id):
    # Arrange (omitted if all input values are provided via test parameters)

    # Act
    if "error_case" in test_id:
        with pytest.raises(ValueError):
            plot_line(
                x_data=x_data, y_data=y_data, x_label=x_label, y_label=y_label,
                title=title, file=file, line_style=line_style, color=color, marker_style=marker_style
            )
    else:
        plot_line(
            x_data=x_data, y_data=y_data, x_label=x_label, y_label=y_label,
            title=title, file=file, line_style=line_style, color=color, marker_style=marker_style
        )

    # Assert
    if "happy_path" in test_id or "edge_case" in test_id:
        assert file.exists(), f"File {file} does not exist for test_id {test_id}"
        # Additional assertions can be made here to check the content of the file if necessary
