from knit_script.knitout_optimization.knitout_structures.knitout_instructions.instruction import Instruction, Instruction_Type


class Rack_Instruction(Instruction):

    def __init__(self, rack: float):
        super().__init__(Instruction_Type.Rack)
        self.rack = rack

    def __str__(self):
        return f"{self.instruction_type} {self.rack};{self.comment_str}\n"
