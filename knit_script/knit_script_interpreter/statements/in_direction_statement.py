"""Used to translate lists of knitting instructions in a single carriage pass"""
from typing import List, Dict

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.instruction_expression import Needle_Instruction_Exp, Needle_Instruction
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Carriage_Pass import Carriage_Pass
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knitting_machine.machine_components.needles import Needle


class In_Direction_Statement(Statement):
    """
        Statement that sets the machine direction for a set of instructions
    """

    def __init__(self, direction: Expression, instructions: List[Needle_Instruction_Exp]):
        """
        Instantiate
        :param direction: direction to execute operations in
        :param instructions: instruction sets to execute
        """
        super().__init__()
        self._direction: Expression = direction
        self._instructions: List[Needle_Instruction_Exp] = instructions

    def execute(self, context: Knit_Script_Context):
        """
        Creates sub-scope to set direction and executes instructions
        :param context:  The current context of the knit_script_interpreter
        """

        context.enter_sub_scope()  # make sub scope with direction variable change
        assert context.current_carrier is not None, f"Cannot execute directed pass without active carrier"
        direction = self._direction.evaluate(context)
        needles_to_instruction: Dict[Needle, Needle_Instruction] = {}

        for instruction_exp in self._instructions:
            instruction, needles = instruction_exp.evaluate(context)
            for needle in needles:
                needles_to_instruction[needle] = instruction

        machine_pass = Carriage_Pass(needles_to_instruction, direction)
        machine_pass.write_knitout(context)
        context.exit_current_scope()

    def __str__(self):
        return f"in {self._direction} -> {self._instructions}"

    def __repr__(self):
        return str(self)
