"""A pass of drop operations"""
from knitout_interpreter.knitout_operations.knitout_instruction import Knitout_Instruction_Type
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Carriage_Pass_Specification import Carriage_Pass_Specification
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Drop_Pass(Statement):
    """
        Executes a set of drops from left to right
    """

    def __init__(self, parser_node, needles: list[Expression]):
        """
        Instantiate
        :param parser_node:
        :param needles: The list of needles to drop from
        """
        super().__init__(parser_node)
        self._needles: list[Expression] = needles

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
            if not isinstance(n, Needle):
                raise TypeError(f"Expected to drop needles but got {n} in {self._needles} <{needles}>")

        needles_to_instruction = {n: Knitout_Instruction_Type.Drop for n in needles}

        machine_pass = Carriage_Pass_Specification(needles_to_instruction, Carriage_Pass_Direction.Rightward, is_drop_pass=True)

        needle_results = machine_pass.write_knitout(context)
        context.last_carriage_pass_result = [n for n in needle_results.keys()]  # stores needles that were dropped
