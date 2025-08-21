"""Functions that are automatically imported in knit-script.

This module provides essential needle-related utility functions that are automatically available in the knit script environment.
These functions offer convenient ways to create needle objects and sort needle collections according to carriage pass requirements.
The functions are designed to simplify common needle operations and provide intuitive interfaces for needle manipulation in knit script programs.
"""
from typing import cast

from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import (
    Carriage_Pass_Direction,
)
from virtual_knitting_machine.machine_components.needles.Needle import Needle
from virtual_knitting_machine.machine_components.needles.Slider_Needle import (
    Slider_Needle,
)
from virtual_knitting_machine.machine_constructed_knit_graph.Machine_Knit_Loop import (
    Machine_Knit_Loop,
)


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


def loops_to_current_needles(machine_state: Knitting_Machine) -> dict[Machine_Knit_Loop, Needle]:
    """
    Access the current location of loops on the knitting machine needles (excluding sliders).
    Args:
        machine_state (Knitting_Machine): The current state of the knitting machine.

    Returns:
        dict[Machine_Knit_Loop, Needle]: A dictionary of all loops currently held on a needle keyed to the needle that holds them.
    """
    result: dict[Machine_Knit_Loop, Needle] = {}
    for n in machine_state.all_loops():
        result.update({loop: n for loop in n.held_loops})
    return result


def loops_to_current_sliders(machine_state: Knitting_Machine) -> dict[Machine_Knit_Loop, Slider_Needle]:
    """
    Access the current location of loops on the knitting machine slider needles.
    Args:
        machine_state (Knitting_Machine): The current state of the knitting machine.

    Returns:
        dict[Machine_Knit_Loop, Slider_Needle]: A dictionary of all loops currently held on a slider needle keyed to the slider that holds them.
    """
    result: dict[Machine_Knit_Loop, Slider_Needle] = {}
    for n in machine_state.all_slider_loops():
        result.update({loop: n for loop in n.held_loops})
    return result
