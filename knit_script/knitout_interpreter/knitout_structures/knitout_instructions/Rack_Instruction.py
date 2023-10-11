import math
from typing import Optional

from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.knitout_instruction import Knitout_Instruction, Instruction_Type


class Rack_Instruction(Knitout_Instruction):
    LEFT_RACK = 10
    RIGHT_RACK = 11
    def __init__(self, rack: float, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Rack, comment)
        self.rack: float = rack

    def __str__(self):
        return f"{self.instruction_type} {self.rack}{self.comment_str}"

    def execute(self, machine_state):
        machine_state.racking = self.rack

    def racking_offset(self) -> int:
        """
        :return: integer value of total offset for racking
        """
        return abs(math.floor(self.rack))

    def racking_alignment(self) -> int:
        """
        :return: 0 if racking is full alignment, 1 for all needle alignment
        """
        if self.rack - math.floor(self.rack) == 0.0:
            return 0
        else:
            return 1

    def racking_direction(self) -> int:
        """
        :return: op line value corresponding to left or right racking
        """
        if self.rack == 0:
            return 0
        elif self.rack < 0:  # todo check these with DATS
            return Rack_Instruction.LEFT_RACK
        else:
            return Rack_Instruction.RIGHT_RACK
