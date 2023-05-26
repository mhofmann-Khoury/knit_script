from knit_script.knitout_optimization.knitout_structures.knitout_instructions.instruction import Instruction, Instruction_Type


class Pause_Instruction(Instruction):
    def __init__(self):
        super().__init__(Instruction_Type.Pause)

