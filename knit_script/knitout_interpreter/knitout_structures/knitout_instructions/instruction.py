"""Structure for Instructions"""
from enum import Enum
from typing import Optional
from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Knitout_Line


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


class Instruction(Knitout_Line):
    """
        Super class for knitout operations
    """

    def __init__(self, instruction_type: Instruction_Type, comment: Optional[str]):
        super().__init__(comment)
        self.instruction_type = instruction_type

    def __str__(self):
        return f"{self.instruction_type}{self.comment_str}"

    def execute(self, machine_state) -> bool:
        return False
