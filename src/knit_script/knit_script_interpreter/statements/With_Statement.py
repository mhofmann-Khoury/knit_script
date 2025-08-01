"""With statement for setting variables in temporary variable space"""

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knit_script_interpreter.statements.assignment import Assignment


class With_Statement(Statement):
    """Statement that sets variables for a sub-statement block.

    Creates a temporary scope where specified variables are assigned new values,
    executes a statement within that scope, then restores the previous values.
    Special handling is provided for machine variables like rack and carrier.
    """

    def __init__(self, parser_node: LRStackNode, statement: Statement, assignments: list[Assignment]) -> None:
        """Initialize a with statement.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            statement: The statement to execute within the temporary variable scope.
            assignments: List of variable assignments to make in the temporary scope.
        """
        super().__init__(parser_node)
        self._statement = statement
        self._assignments = assignments

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the statement within a temporary variable scope.

        Creates a new scope, applies all assignments, executes the statement,
        then restores machine variables to their previous states. Machine
        variables are restored in a specific order to maintain consistency.

        Args:
            context: The current execution context of the knit script interpreter.
        """
        context.enter_sub_scope()  # make sub scope with variable changes
        for assign in self._assignments:
            assign.assign_value(context)
        self._statement.execute(context)
        context.exit_current_scope()  # exit scope with variable changes excluding machine specific changes

    def __str__(self) -> str:
        """Return string representation of the with statement.

        Returns:
            A string showing the assignments and statement.
        """
        return f"With({self._assignments} -> {self._statement})"

    def __repr__(self) -> str:
        """Return detailed string representation of the with statement.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)
