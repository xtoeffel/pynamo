"""Utility functions for creation of FE model properties."""

from numpy import ndarray
from numpy import zeros
from typing import Tuple


def expand_matrix(
    system_matrix: ndarray, element_matrix: ndarray, symmetric: bool = True
) -> ndarray:
    """Expands a system matrix by an element matrix by adding it to the lower right corner with half height and width
    overlap.

    The returned matrix will be greater than the system matrix by half the height and width of the specified matrix.
    This assumes that the system matrix was build using this function with element matrixes of the same shape. Values
    of the system and element matrix will be added for cells where they overlap.

    :param system_matrix: System matrix (to add to)
    :type system_matrix: ndarray
    :param element_matrix: Element matrix (to be added)
    :type element_matrix: ndarray

    :return: New system matrix with added element matrix
    :rtype: ndarray

    :raises ValueError: If shape of element matrix is not symmetric, but desired - if any matrix is of insufficient
                        size - if element matrix has odd shape
    """
    sys_shape: Tuple[int, ...] = system_matrix.shape
    elem_shape: Tuple[int, ...] = element_matrix.shape

    if sys_shape[0] < 2 or sys_shape[1] < 2:
        raise ValueError(f"Insufficient sized system matrix: {sys_shape}")
    if symmetric and elem_shape[0] != elem_shape[1]:
        raise ValueError(f"Element matrix has asymmetric shape: {elem_shape}")
    if elem_shape[0] < 2 or elem_shape[1] < 2:
        raise ValueError(f"Insufficient sized element matrix: {elem_shape}")
    if elem_shape[0] % 2 != 0 or elem_shape[1] % 2 != 0:
        raise ValueError(f"Odd sized element matrix: {elem_shape}")

    new_sys_matrix: ndarray = zeros(
        (sys_shape[0] + int(elem_shape[0] / 2), sys_shape[1] + int(elem_shape[1] / 2))
    )
    new_sys_matrix[0 : sys_shape[0], 0 : sys_shape[1]] += system_matrix
    new_sys_matrix[
        sys_shape[0] - int(elem_shape[0] / 2) :, sys_shape[1] - int(elem_shape[1] / 2) :
    ] += element_matrix

    return new_sys_matrix


def is_equal(val1: float, val2: float, atol: float = 1.0e-12) -> bool:
    """Evaluates if one value equals another considering a absolute tolerance.

    :param val1: first value
    :type val1: float
    :param val2: second value
    :type val2: float
    :param atol: absolute symmetric tolerance
    :type atol: float

    :return: True if val1 == val2 considering atol
    """
    return abs(val1 - val2) <= atol
