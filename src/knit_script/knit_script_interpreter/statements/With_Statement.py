"""With statement for setting variables in temporary variable space.

This module provides the With_Statement class, which implements temporary variable scoping in knit script programs.
It allows variables to be temporarily assigned new values within a specific scope, then automatically restored when the scope exits.
"""

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.assignment import Assignment
from knit_script.knit_script_interpreter.statements.scoped_statement import Scoped_Statement
from knit_script.knit_script_interpreter.statements.Statement import Statement


class With_Statement(Scoped_Statement):
    """Statement that sets variables for a sub-statement block.

    Creates a temporary scope where specified variables are assigned new values, executes a statement within that scope, then restores the previous values.
    Special handling is provided for machine variables like rack and carrier to ensure proper machine state management.

    This statement is useful for temporarily changing machine configuration or variable values for specific operations without permanently affecting the outer scope.
     It provides a clean way to make scoped changes that are automatically reverted.

    Attributes:
        _assignments (list[Assignment]): List of variable assignments to make in the temporary scope.
    """

    def __init__(self, parser_node: LRStackNode, statement: Statement, assignments: list[Assignment]) -> None:
        """Initialize a with statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            statement (Statement): The statement to execute within the temporary variable scope.
            assignments (list[Assignment]): List of variable assignments to make in the temporary scope before executing the statement.
        """
        super().__init__(parser_node, statement)
        self._assignments = assignments

    def pre_scope_action(self, context: Knit_Script_Context) -> bool:
        """
        Apply all assignments from the with-preamble to the subscope of the with statement.
        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.

        Returns:
            bool: True because the statement using the with-assignments should always be executed.
        """
        for assign in self._assignments:
            assign.assign_value(context)
        return True
