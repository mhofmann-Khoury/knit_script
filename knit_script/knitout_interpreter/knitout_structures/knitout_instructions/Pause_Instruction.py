from typing import Optional

from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction, Instruction_Type


class Pause_Instruction(Instruction):
    def __init__(self, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Pause, comment)

    def execute(self, machine_state):
        pass
