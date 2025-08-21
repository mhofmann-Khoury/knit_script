"""Used to translate lists of knitting instructions in a single carriage pass.

This module provides the In_Direction_Statement class, which handles the execution of multiple needle instructions within a single carriage pass in a specified direction.
It coordinates instruction evaluation, carriage pass creation, and proper handling of special operations like split instructions.
"""
from knitout_interpreter.knitout_operations.knitout_instruction import (
    Knitout_Instruction_Type,
)
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_exceptions.ks_exceptions import (
    No_Declared_Carrier_Exception,
)
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.instruction_expression import (
    Needle_Instruction_Exp,
)
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Carriage_Pass_Specification import (
    Carriage_Pass_Specification,
)
from knit_script.knit_script_interpreter.statements.Statement import Statement


class In_Direction_Statement(Statement):
    """Statement that sets the machine direction for a set of instructions.

    Creates a carriage pass with the specified direction and executes all needle instructions within that pass.
    Handles special cases like split operations that return second needles and provides proper scope management for direction changes.

    This statement is fundamental to knit script execution, as it coordinates multiple needle operations that must be performed together in a single carriage pass.
    It ensures that all operations are compatible and executed in the correct sequence based on the specified direction.

    Attributes:
        _direction (Expression): Expression that evaluates to the carriage pass direction.
        _instructions (list[Needle_Instruction_Exp]): List of needle instruction expressions to execute.
    """

    def __init__(self, parser_node: LRStackNode, direction: Expression, instructions: list[Needle_Instruction_Exp]) -> None:
        """Initialize a directional instruction statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            direction (Expression): Expression that evaluates to the carriage pass direction for executing the instructions.
            instructions (list[Needle_Instruction_Exp]): List of needle instruction expressions to execute in the specified direction.
        """
        super().__init__(parser_node)
        self._direction: Expression = direction
        self._instructions: list[Needle_Instruction_Exp] = instructions

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute all instructions in the specified direction.

        Creates a new scope, evaluates the direction, processes all instructions into a carriage pass specification, and executes the pass.
        Handles special result handling for split operations and stores pass results for potential use by subsequent operations.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.

        Raises:
            No_Declared_Carrier_Exception: If no working carrier is set when instructions require one for yarn-based operations.
        """
        context.enter_sub_scope()  # make sub scope with direction variable change
        if context.carrier is None:
            raise No_Declared_Carrier_Exception(self)
        direction = self._direction.evaluate(context)
        needles_to_instruction: dict[Needle, Knitout_Instruction_Type] = {}

        has_splits = False
        for instruction_exp in self._instructions:
            instruction, needles = instruction_exp.evaluate(context)
            if instruction is Knitout_Instruction_Type.Split:
                has_splits = True
            for needle in needles:
                needles_to_instruction[needle] = instruction

        machine_pass = Carriage_Pass_Specification(self, needles_to_instruction, direction)
        context.last_carriage_pass_result = machine_pass.write_knitout(context)
        if not has_splits:  # no second needle to report
            context.last_carriage_pass_result = [n for n in context.last_carriage_pass_result.keys()]
        context.exit_current_scope()

    def __str__(self) -> str:
        """Return string representation of the directional statement.

        Returns:
            str: A string showing the direction and instructions.
        """
        return f"in {self._direction} -> {self._instructions}"

    def __repr__(self) -> str:
        """Return detailed string representation of the directional statement.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)
