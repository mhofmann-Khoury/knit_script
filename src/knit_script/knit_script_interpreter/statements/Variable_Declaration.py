"""Statement for declaring a variable"""
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knit_script_interpreter.statements.assignment import Assignment


class Variable_Declaration(Statement):
    """Used to set a variable value at the current or global scope.

    This statement wraps an assignment operation and can optionally declare
    the variable in the global scope rather than the current local scope.
    """

    def __init__(self, parser_node: LRStackNode, assignment: Assignment, is_global: bool = False) -> None:
        """Initialize a variable declaration.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            assignment: The assignment operation that defines the variable
                name and value.
            is_global: If True, declares the variable in the global scope.
                If False, declares in the current local scope.
        """
        super().__init__(parser_node)
        self._is_global = is_global
        self._assignment: Assignment = assignment

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the variable declaration by performing the assignment.

        Evaluates the assignment expression and stores the result in the
        variable scope according to the global/local setting.

        Args:
            context: The current execution context of the knit script interpreter.
        """
        self._assignment.assign_value(context, is_global=self._is_global)

    def __str__(self) -> str:
        """Return string representation of the variable declaration.

        Returns:
            A string showing the assignment with a semicolon.
        """
        return f"{self._assignment};"

    def __repr__(self) -> str:
        """Return detailed string representation of the variable declaration.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)
