"""Statements that produce knitout for machine level instructions.

This module provides statement classes for machine-level operations that generate specific knitout instructions.
It includes statements for pausing machine execution and other machine control operations that operate at the machine level rather than on specific needles.
"""
from knitout_interpreter.knitout_operations.Pause_Instruction import Pause_Instruction
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Pause_Statement(Statement):
    """An instruction that pauses the knitting machine.

    Generates a pause instruction in the knitout, causing the machine to stop execution until manually resumed.
    This is useful for manual interventions, inspection points, or when operator input is required during the knitting process.

    The pause statement provides a way to create breakpoints in the knitting process where the machine will halt and wait for operator intervention before continuing with the remaining instructions.
    """

    def __init__(self, parser_node: LRStackNode) -> None:
        """Initialize a pause statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
        """
        super().__init__(parser_node)

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the pause by writing a pause instruction to knitout.

        Generates a pause instruction and adds it to the knitout output, which will cause the knitting machine to halt execution at this point.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
        """
        context.knitout.append(Pause_Instruction())

    def __str__(self) -> str:
        """Return string representation of the pause statement.

        Returns:
            str: A string indicating this is a pause operation.
        """
        return "Pause"

    def __repr__(self) -> str:
        """Return detailed string representation of the pause statement.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)
