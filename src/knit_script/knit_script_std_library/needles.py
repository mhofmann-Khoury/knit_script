"""Functions that are automatically imported in knit-script."""
from typing import cast

from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Needle import Needle


def needle(is_front: bool, index: int) -> Needle:
    """Creates a needle with the specified bed position and index.

    Args:
        is_front: Whether the needle is on the front bed (True) or back bed (False).
        index: The position index of the needle on the bed.

    Returns:
        A Needle object with the given position and bed configuration.
    """
    return Needle(is_front, index)


def direction_sorted_needles(needles: list[Needle], direction: Carriage_Pass_Direction = Carriage_Pass_Direction.Rightward, racking: float = 0.0) -> list[Needle]:
    """Sorts a list of needles according to the specified carriage pass direction.

    This function orders needles in the sequence they would be encountered during
    a carriage pass in the given direction, taking into account the machine's
    racking configuration.

    Args:
        needles: The list of needles to sort.
        direction: The carriage pass direction to sort by. Defaults to rightward.
        racking: The racking value of the machine, representing the relative offset between front and back needle beds.
            Defaults to 0.0.

    Returns:
        A new list containing the needles sorted in the order they would be
        encountered during a carriage pass in the specified direction.
    """
    return cast(list[Needle], direction.sort_needles(needles, racking=int(racking)))
