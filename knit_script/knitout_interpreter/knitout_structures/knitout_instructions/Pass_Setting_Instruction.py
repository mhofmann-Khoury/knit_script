from typing import Optional

from knit_script.knitout_interpreter.DAT_Compiler.OP_Line import OP_Line
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.knitout_instruction import Knitout_Instruction, Instruction_Type


class Pass_Setting_Instruction(Knitout_Instruction):
    def __init__(self, instruction_type: Instruction_Type, op_line: OP_Line, comment: str | None = None):
        super().__init__(instruction_type, comment)
        self.op_line = op_line

    def execute(self, machine_state):
        pass

    def op_code_value(self) -> int:
        """
        :return: The op code value corresponding to this operation
        """
        return 0


class Pause_Instruction(Pass_Setting_Instruction):
    def __init__(self, comment: str | None = None):
        super().__init__(Instruction_Type.Pause, OP_Line.Pause, comment)

    def op_code_value(self) -> int:
        return -1  # todo

    def execute(self, machine_state):
        pass


class Stitch_Instruction(Pass_Setting_Instruction):

    def __init__(self, L: float, T: float, comment: str | None = None):
        super().__init__(Instruction_Type.Stitch, OP_Line.Stitch_Number, comment)
        self.T = T
        self.L = L

    def __str__(self):
        return f"{self.instruction_type} {self.L} {self.T}{self.comment_str}"

    def execute(self, machine_state):
        pass

    def op_code_value(self) -> int:
        return -1  # todo
