from knit_script.knitout_optimization.knitout_structures.knitout_instructions.instruction import Instruction, Instruction_Type
from knit_script.knitout_optimization.knitout_structures.knitout_values.Carrier_Set import Carrier_Set


class Carrier_Instruction(Instruction):

    def __init__(self, instruction_type: Instruction_Type, cs: Carrier_Set):
        super().__init__(instruction_type)
        self.cs = cs

    def __str__(self):
        return f"{self.instruction_type} {self.cs};{self.comment_str}\n"


class In_Instruction(Carrier_Instruction):

    def __init__(self, cs: Carrier_Set):
        super().__init__(Instruction_Type.In, cs)


class Inhook_Instruction(Carrier_Instruction):

    def __init__(self, cs: Carrier_Set):
        super().__init__(Instruction_Type.Inhook, cs)


class Releasehook_Instruction(Carrier_Instruction):

    def __init__(self, cs: Carrier_Set):
        super().__init__(Instruction_Type.Releasehook, cs)


class Out_Instruction(Carrier_Instruction):

    def __init__(self, cs: Carrier_Set):
        super().__init__(Instruction_Type.Out, cs)


class Outhook_Instruction(Carrier_Instruction):

    def __init__(self, cs: Carrier_Set):
        super().__init__(Instruction_Type.Outhook, cs)
