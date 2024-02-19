from pathlib import Path
from PIL import Image
import numpy as np

from firefly.validation.fileIO import validate_file_extension, validate_path


def create_random_png(
        filename: Path,
        width=256,
        height=256,):

    # validate the filename
    filename = validate_file_extension(filename, [".png"])

    # Generate an array of random colors
    random_data = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

    # Create an image from the array
    image = Image.fromarray(random_data)

    # Save the image
    image.save(filename)

    return f"Random PNG image created and saved as {filename}"