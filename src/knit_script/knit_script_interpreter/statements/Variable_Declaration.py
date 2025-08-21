"""Statement for declaring a variable.

This module provides the Variable_Declaration statement class, which handles variable declaration operations in knit script programs.
It wraps assignment operations with scope-specific behavior for both local and global variable declarations.
"""
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.assignment import Assignment
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Variable_Declaration(Statement):
    """Used to set a variable value at the current or global scope.

    This statement wraps an assignment operation and can optionally declare the variable in the global scope rather than the current local scope.
    It provides explicit variable declaration semantics that can override the normal scoping rules when global declaration is specified.

    Variable declarations are used to establish new variables with specific scope targeting,
    ensuring that variables are created in the intended scope level regardless of existing variable names in parent scopes.

    Attributes:
        _is_global (bool): True if the variable should be declared in global scope.
        _assignment (Assignment): The assignment operation that defines the variable name and value.
    """

    def __init__(self, parser_node: LRStackNode, assignment: Assignment, is_global: bool = False) -> None:
        """Initialize a variable declaration.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            assignment (Assignment): The assignment operation that defines the variable name and value.
            is_global (bool, optional): If True, declares the variable in the global scope. If False, declares in the current local scope. Defaults to False.
        """
        super().__init__(parser_node)
        self._is_global = is_global
        self._assignment: Assignment = assignment

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the variable declaration by performing the assignment.

        Evaluates the assignment expression and stores the result in the variable scope according to the global/local setting, ensuring the variable is created in the intended scope level.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
        """
        self._assignment.assign_value(context, is_global=self._is_global)

    def __str__(self) -> str:
        """Return string representation of the variable declaration.

        Returns:
            str: A string showing the assignment with a semicolon.
        """
        return f"{self._assignment};"

    def __repr__(self) -> str:
        """Return detailed string representation of the variable declaration.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)
