from typing import Optional

from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction, Instruction_Type


class Rack_Instruction(Instruction):

    def __init__(self, rack: float, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Rack, comment)
        self.rack = rack

    def __str__(self):
        return f"{self.instruction_type} {self.rack}{self.comment_str}"

    def execute(self, machine_state):
        machine_state.racking = self.rack
