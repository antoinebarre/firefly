# -*- coding: utf-8 -*-
"""Module for validating and working with lists."""

from typing import Any, Type, TypeVar

def is_1d_list(
    data: Any
    ) -> bool:
    """
    Check if the input is a 1D list.

    Args:
        data (Any): The input data to check.

    Returns:
        bool: True if the input is a 1D list, False otherwise.

    """
    if not isinstance(data, list):
        return False
    return all((not isinstance(element, list) for element in data))

# create a variable type
T = TypeVar("T")

def validate_list(
    data: Any,
    element_type: Type[T],
    ) -> list[T]:
    """
    Validate a list by checking if it is a 1D list and if its elements are of the correct type.

    Args:
        data (Any): The input list to validate.
        element_type (Type[T]): The expected type of the elements in the list.

    Returns:
        list[T]: The validated list.

    Raises:
        TypeError: If the element_type is not a type or if the input is not a 1D
        list or if the elements are not of the correct type.

    """
    # validate input
    if not isinstance(element_type, type):
        raise TypeError(
            f"element_type must be a type. Got {element_type} - {type(element_type)}")

    # validate 1D list
    if not is_1d_list(data):
        raise TypeError(f"Input must be a 1D list. Got {data} - {type(data)}")

    # validate elements are of the correct type
    if not all((isinstance(element, element_type) for element in data)):
        # detect the first element that is not of the correct type
        for i, element in enumerate(data):
            if not isinstance(element, element_type):
                msg = (
                    f"All elements must be of type {element_type}.",
                    f"Received: {data}",
                    f"Element {i}: {element}, type {type(element)}"
                )
                raise TypeError(msg)
    return data

if __name__=="__main__":

    value = [1, 2, 3]

    a = validate_list(value, float)
    print(a)
