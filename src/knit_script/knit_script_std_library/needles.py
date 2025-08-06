"""Functions that are automatically imported in knit-script.

This module provides essential needle-related utility functions that are automatically available in the knit script environment.
These functions offer convenient ways to create needle objects and sort needle collections according to carriage pass requirements.
The functions are designed to simplify common needle operations and provide intuitive interfaces for needle manipulation in knit script programs.
"""
from typing import cast

from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Needle import Needle


def needle(is_front: bool, index: int) -> Needle:
    """Create a needle with the specified bed position and index.

    This function provides a convenient way to create Needle objects with the specified bed position and index location.
    It serves as a factory function for needle creation and is commonly used throughout knit script programs for referencing specific needles on the knitting machine.

    Args:
        is_front (bool): Whether the needle is on the front bed (True) or back bed (False). The front bed is typically the bed closest to the operator.
        index (int): The position index of the needle on the specified bed. This represents the physical position of the needle along the bed.

    Returns:
        Needle: A Needle object with the given position and bed configuration, ready for use in knitting operations.
    """
    return Needle(is_front, index)


def direction_sorted_needles(needles: list[Needle], direction: Carriage_Pass_Direction = Carriage_Pass_Direction.Rightward, racking: float = 0.0) -> list[Needle]:
    """Sort a list of needles according to the specified carriage pass direction.

    This function orders needles in the sequence they would be encountered during a carriage pass in the given direction, taking into account the machine's racking configuration.
    This sorting is essential for proper carriage pass execution, as needles must be processed in the correct order to avoid conflicts and ensure proper yarn handling.

    The sorting algorithm considers both the direction of carriage movement and the racking offset between front and back needle beds.
    This ensures that needles are processed in the physically correct sequence as the carriage moves across the machine.

    Args:
        needles (list[Needle]): The list of needles to sort. Can contain needles from both front and back beds.
        direction (Carriage_Pass_Direction, optional): The carriage pass direction to sort by. Determines whether needles are ordered for left-to-right or right-to-left carriage movement.
        Defaults to Carriage_Pass_Direction.Rightward.
        racking (float, optional): The racking value of the machine, representing the relative offset between front and back needle beds.
        This affects the relative positioning of front and back needles during sorting. Defaults to 0.0.

    Returns:
        list[Needle]: A new list containing the needles sorted in the order they would be encountered during a carriage pass in the specified direction. The original list is not modified.

    Note:
        The racking parameter is converted to an integer for the underlying sorting algorithm.
        This represents the standard practice in knitting machine operations where racking is typically specified in whole needle positions.
    """
    return cast(list[Needle], direction.sort_needles(needles, racking=int(racking)))
