from knit_script.knitout_optimization.knitout_structures.knitout_instructions.instruction import Instruction, Instruction_Type


class Stitch_Instruction(Instruction):

    def __init__(self, L: float, T: float):
        super().__init__(Instruction_Type.Stitch)
        self.T = T
        self.L = L

    def __str__(self):
        return f"{self.instruction_type} {self.L} {self.T};{self.comment_str}\n"
