"""Functions that are automatically imported in knitscript"""

from knitting_machine.machine_components.needles import Needle


def needle(is_front: bool, index: int):
    """
    :param index:
    :param is_front:
    :return: Returns a Needle with given position and bed
    """
    return Needle(is_front, index)