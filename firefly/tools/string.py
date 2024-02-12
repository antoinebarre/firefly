"""Collection of tools for working with strings."""

import random
import string
import time

from firefly.validation.int import validate_positive_integer


def generate_random_string(length: int) -> str:
    """
    Generate a random string of a given length.

    :param length: The length of the string to generate.
    :return: A random string of the given length.
    """
    length = validate_positive_integer(length)

    return ''.join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(length))

def add_unique_suffix(str2modify: str) -> str:
    """
    Adds a unique suffix to a string.

    Args:
        str2modify (str): The string to modify.

    Returns:
        str: The modified string with a unique suffix.
    """
    perf_counter = str(time.perf_counter()).replace('.', '')
    return f"{str2modify}_{perf_counter}"
