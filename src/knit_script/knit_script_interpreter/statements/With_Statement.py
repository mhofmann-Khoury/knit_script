"""With statement for setting variables in temporary variable space.

This module provides the With_Statement class, which implements temporary variable scoping in knit script programs.
It allows variables to be temporarily assigned new values within a specific scope, then automatically restored when the scope exits.
"""

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.assignment import Assignment
from knit_script.knit_script_interpreter.statements.Statement import Statement


class With_Statement(Statement):
    """Statement that sets variables for a sub-statement block.

    Creates a temporary scope where specified variables are assigned new values, executes a statement within that scope, then restores the previous values.
    Special handling is provided for machine variables like rack and carrier to ensure proper machine state management.

    This statement is useful for temporarily changing machine configuration or variable values for specific operations without permanently affecting the outer scope.
     It provides a clean way to make scoped changes that are automatically reverted.

    Attributes:
        _statement (Statement): The statement to execute within the temporary variable scope.
        _assignments (list[Assignment]): List of variable assignments to make in the temporary scope.
    """

    def __init__(self, parser_node: LRStackNode, statement: Statement, assignments: list[Assignment]) -> None:
        """Initialize a with statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            statement (Statement): The statement to execute within the temporary variable scope.
            assignments (list[Assignment]): List of variable assignments to make in the temporary scope before executing the statement.
        """
        super().__init__(parser_node)
        self._statement = statement
        self._assignments = assignments

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the statement within a temporary variable scope.

        Creates a new scope, applies all assignments, executes the statement, then restores machine variables to their previous states.
        Machine variables are handled specially to ensure proper state restoration and consistency.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
        """
        context.enter_sub_scope()  # make sub scope with variable changes
        for assign in self._assignments:
            assign.assign_value(context)
        self._statement.execute(context)
        context.exit_current_scope()  # exit scope with variable changes excluding machine specific changes

    def __str__(self) -> str:
        """Return string representation of the with statement.

        Returns:
            str: A string showing the assignments and statement.
        """
        return f"With({self._assignments} -> {self._statement})"

    def __repr__(self) -> str:
        """Return detailed string representation of the with statement.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)
