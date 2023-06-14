from typing import Optional

from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction, Instruction_Type


class Stitch_Instruction(Instruction):

    def __init__(self, L: float, T: float, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Stitch, comment)
        self.T = T
        self.L = L

    def __str__(self):
        return f"{self.instruction_type} {self.L} {self.T}{self.comment_str}"

    def execute(self, machine_state):
        pass
