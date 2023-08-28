"""Enumerator used to define the two pull direction of a loop through other loops"""
from enum import Enum


class Pull_Direction(Enum):
    """An enumerator of the two pull directions of a loop"""
    BtF = "Knit"
    FtB = "Purl"

    def opposite(self):
        """
        :return: returns the opposite pull direction of self
        """
        if self is Pull_Direction.BtF:
            return Pull_Direction.FtB
        else:
            return Pull_Direction.BtF

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
