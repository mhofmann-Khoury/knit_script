"""Statements that produce knitout for machine level instructions"""
from knitout_interpreter.knitout_operations.Pause_Instruction import Pause_Instruction
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Pause_Statement(Statement):
    """An instruction that pauses the knitting machine.

    Generates a pause instruction in the knitout, causing the machine
    to stop execution until manually resumed.
    """

    def __init__(self, parser_node: LRStackNode) -> None:
        """Initialize a pause statement.

        Args:
            parser_node: The parser node from the abstract syntax tree.
        """
        super().__init__(parser_node)

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the pause by writing a pause instruction to knitout.

        Args:
            context: The current execution context of the knit script interpreter.
        """
        context.knitout.append(Pause_Instruction())

    def __str__(self) -> str:
        """Return string representation of the pause statement.

        Returns:
            A string indicating this is a pause operation.
        """
        return "Pause"

    def __repr__(self) -> str:
        """Return detailed string representation of the pause statement.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)
