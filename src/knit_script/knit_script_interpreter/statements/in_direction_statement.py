"""Used to translate lists of knitting instructions in a single carriage pass"""
from knitout_interpreter.knitout_operations.knitout_instruction import Knitout_Instruction_Type
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_exceptions.Knit_Script_Exception import No_Declared_Carrier_Exception
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.instruction_expression import Needle_Instruction_Exp
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Carriage_Pass_Specification import Carriage_Pass_Specification
from knit_script.knit_script_interpreter.statements.Statement import Statement


class In_Direction_Statement(Statement):
    """
        Statement that sets the machine direction for a set of instructions
    """

    def __init__(self, parser_node, direction: Expression, instructions: list[Needle_Instruction_Exp]):
        """
        Instantiate
        :param parser_node:
        :param direction: Direction to execute operations in.
        :param instructions: Instruction sets to execute.
        """
        super().__init__(parser_node)
        self._direction: Expression = direction
        self._instructions: list[Needle_Instruction_Exp] = instructions

    def execute(self, context: Knit_Script_Context):
        """
        Creates sub-scope to set the direction and executes instructions
        :param context:  The current context of the knit_script_interpreter
        """

        context.enter_sub_scope()  # make sub scope with direction variable change
        if context.carrier is None:
            raise No_Declared_Carrier_Exception()
        direction = self._direction.evaluate(context)
        needles_to_instruction: dict[Needle, Knitout_Instruction_Type] = {}

        has_splits = False
        for instruction_exp in self._instructions:
            instruction, needles = instruction_exp.evaluate(context)
            if instruction is Knitout_Instruction_Type.Split:
                has_splits = True
            for needle in needles:
                needles_to_instruction[needle] = instruction

        machine_pass = Carriage_Pass_Specification(needles_to_instruction, direction)
        context.last_carriage_pass_result = machine_pass.write_knitout(context)
        if not has_splits:  # no second needle to report
            context.last_carriage_pass_result = [n for n in context.last_carriage_pass_result.keys()]
        context.exit_current_scope()

    def __str__(self):
        return f"in {self._direction} -> {self._instructions}"

    def __repr__(self):
        return str(self)
