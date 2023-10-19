"""Functions that are automatically imported in knit-script"""

from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.needles import Needle


def needle(is_front: bool, index: int):
    """
    :param index:
    :param is_front:
    :return: Returns a Needle with given position and bed
    """
    return Needle(is_front, index)


def direction_sorted_needles(needles: list[Needle], direction: Pass_Direction = Pass_Direction.Rightward, racking: float = 0.0) -> list[Needle]:
    """
    :param racking: racking of machine
    :param needles: the needles to sort
    :param direction: the direction to sort by
    :return: list of needles sorted by given direction
    """
    return direction.sort_needles(needles, racking=racking)
