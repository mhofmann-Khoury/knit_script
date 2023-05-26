"""Structure for Instructions"""
from enum import Enum
from typing import Optional


class Instruction_Type(Enum):
    """
        Knitout Instruction types
    """
    In = "in"
    Inhook = "inhook"
    Releasehook = "releasehook"
    Out = "out"
    Outhook = "outhook"
    Stitch = "stitch"
    Rack = "rack"
    Knit = "knit"
    Tuck = "tuck"
    Split = "split"
    Drop = "drop"
    Amiss = "amiss"
    Xfer = "xfer"
    Miss = "miss"
    Pause = "pause"
    X = "x-"

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)


class Instruction:
    """
        Super class for knitout operations
    """

    def __init__(self, instruction_type: Instruction_Type):
        self.instruction_type = instruction_type
        self.comment = None

    @property
    def has_comment(self) -> bool:
        """
        :return: True if comment is present
        """
        return self.comment is not None

    @property
    def comment_str(self) -> str:
        """
        :return: comment as a string
        """
        if not self.has_comment:
            return ""
        else:
            return self.comment

    def __str__(self):
        return f"{self.instruction_type};{self.comment_str}\n"

    def __repr__(self):
        return str(self)
