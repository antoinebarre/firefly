"""Collection of tools for working with strings."""

import random
import string
import textwrap
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

def indent(
    text:str,
    amount:int,
    ch: str =' '):
    """
    Indents the given text by the specified amount using the specified character.

    Args:
        text (str): The text to be indented.
        amount (int): The number of times the character should be repeated for
            each indentation level.
        ch (str, optional): The character used for indentation. Defaults to a space (' ').

    Returns:
        str: The indented text.
    """
    return textwrap.indent(text, amount * ch)
