"""A pass of drop operations"""
from typing import List

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Carriage_Pass import Carriage_Pass
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction_Type
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.needles import Needle


class Drop_Pass(Statement):
    """
        Executes a set of drops from left to right
    """

    def __init__(self, parser_node, needles: List[Expression]):
        """
        Instantiate
        :param parser_node:
        :param needles: The list of needles to drop from
        """
        super().__init__(parser_node)
        self._needles: List[Expression] = needles

    def execute(self, context: Knit_Script_Context):
        """
        Writes drop operations to knitout
        :param context: The current context of the knit_script_interpreter
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

        needles_to_instruction = {n: Instruction_Type.Drop for n in needles}

        machine_pass = Carriage_Pass(needles_to_instruction, Pass_Direction.Rightward, is_drop_pass=True)

        needle_results = machine_pass.write_knitout(context)
        context.last_carriage_pass_result = [n for n in needle_results.keys()]  # stores needles that were dropped
