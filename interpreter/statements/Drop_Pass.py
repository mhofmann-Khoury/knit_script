"""A pass of drop operations"""
from typing import List

from interpreter.expressions.expressions import Expression
from interpreter.expressions.instruction_expression import Needle_Instruction
from interpreter.parser.knit_pass_context import Knit_Script_Context
from interpreter.statements.Machine_Pass import Carriage_Pass
from interpreter.statements.Statement import Statement
from knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knitting_machine.machine_components.needles import Needle


class Drop_Pass(Statement):
    """
        Executes a set of drops from left to right
    """
    def __init__(self, needles: List[Expression]):
        """
        Instantiate
        :param needles: the list of needles to drop from
        """
        super().__init__()
        self._needles: List[Expression] = needles

    def execute(self, context: Knit_Script_Context):
        """
        Writes drop operations to knitout
        :param context: The current context of the interpreter
        """
        needles = []
        for needle in self._needles:
            n = needle.evaluate(context)
            if isinstance(n, list):
                needles.extend(n)
            else:
                needles.append(n)
        for n in needles:
            assert isinstance(n, Needle), \
                f"Expected drop from needles but got {n}"

        needles_to_instruction = {n: Needle_Instruction.drop for n in needles}

        machine_pass = Carriage_Pass(needles_to_instruction, Pass_Direction.Left_to_Right_Increasing)

        machine_pass.write_knitout(context)
