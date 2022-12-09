"""Enumerator of possible pass directions"""
import functools
from enum import Enum
from typing import List

from KnitScript.knitting_machine.machine_components.needles import Needle


class Pass_Direction(Enum):
    """
    An enumerator for the two directions the carriage can pass on the machine
    Needles are oriented on the machine left to right in ascending order:
    Left -> 0 1 2 ... N <- Right
    """
    Right_to_Left_Decreasing = "-"
    Left_to_Right_Increasing = "+"

    def opposite(self):
        """
        :return: the opposite pass direction of this
        """
        if self is Pass_Direction.Right_to_Left_Decreasing:
            return Pass_Direction.Left_to_Right_Increasing
        else:
            return Pass_Direction.Right_to_Left_Decreasing

    def __neg__(self):
        return self.opposite()

    def next_needle_position(self, needle_pos: int):
        """
        Gets the next needle in a given direction
        :param needle_pos: the needle that we are looking for the next neighbor of
        :return: the next needle position in the pass direction
        """
        if self is Pass_Direction.Right_to_Left_Decreasing:
            return needle_pos - 1
        else:
            return needle_pos + 1

    def prior_needle_position(self, needle_pos: int):
        """
        Gets the prior needle in a given direction
        :param needle_pos: the needle that we are looking for the prior neighbor of
        :return: the prior needle position in the pass direction
        """
        if self is Pass_Direction.Right_to_Left_Decreasing:
            return needle_pos + 1
        else:
            return needle_pos - 1

    @staticmethod
    def get_direction(dir_str):
        """
        Returns a Pass direction enum given a valid string
        :param dir_str: string to convert to direction
        :return: Pass direction by string
        """
        if dir_str == "-":
            return Pass_Direction.Right_to_Left_Decreasing
        else:
            return Pass_Direction.Left_to_Right_Increasing

    def sort_needles(self, needles: List[Needle], racking: float = 0.0) -> List[Needle]:
        """
        Return needles sorted in direction at given racking
        :param racking: The racking to sort needles in. Sets back bed offset
        :param needles: needles to be sorted in pass direction.
        :return: List of needles sorted in the pass direction
        """
        if len(needles) == 0:
            return needles
        ascending = self is Pass_Direction.Left_to_Right_Increasing
        position_sorted = sorted(needles,
                                 key=functools.cmp_to_key(lambda x, y: Needle.needle_at_racking_cmp(x, y, racking)),
                                 reverse=not ascending)
        return position_sorted

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
