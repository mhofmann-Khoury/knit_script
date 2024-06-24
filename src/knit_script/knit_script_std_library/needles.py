"""Functions that are automatically imported in knit-script"""
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Needle import Needle


def needle(is_front: bool, index: int):
    """
    :param index:
    :param is_front:
    :return: Returns a Needle with given position and bed
    """
    return Needle(is_front, index)


def direction_sorted_needles(needles: list[Needle], direction: Carriage_Pass_Direction = Carriage_Pass_Direction.Rightward, racking: float = 0.0) -> list[Needle]:
    """
    :param racking: racking of machine
    :param needles: the needles to sort
    :param direction: the direction to sort by
    :return: list of needles sorted by given direction
    """
    return direction.sort_needles(needles, racking=int(racking))
