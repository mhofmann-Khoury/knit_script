from typing import Optional

from knit_script.knitout_optimization.knitout_structures.knitout_instructions.instruction import Instruction, Instruction_Type


class Pause_Instruction(Instruction):
    def __init__(self, comment: Optional[str]):
        super().__init__(Instruction_Type.Pause, comment)

