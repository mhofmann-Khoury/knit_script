"""Expression for accessing variables.

This module provides the Variable_Expression class, which handles variable access operations in knit script programs.
It provides the mechanism for retrieving variable values from the current execution scope, following the scope resolution hierarchy established by the knit script context system.
"""
import warnings
from typing import Any

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_warnings.Knit_Script_Warning import (
    Knit_Script_Warning,
    Shadow_Variable_Warning,
)


class Variable_Expression(Expression):
    """A structure for accessing variables by name from the current context scope.

    The Variable_Expression class implements variable access operations in knit script programs.
    It stores a variable name and retrieves the corresponding value from the current execution context using the scope resolution system.
    This includes searching through local scopes, parent scopes, module scopes, and global scopes as defined by the knit script scoping rules.

    This expression type is fundamental to knit script programs, enabling access to all types of variables including user-defined variables,
    function parameters, machine state variables, and built-in constants.

    Attributes:
        _variable_name (str): The name of the variable to access from the current scope.
    """

    def __init__(self, parser_node: LRStackNode, variable_name: str) -> None:
        """Initialize the Variable_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            variable_name (str): Name of the variable to access from the execution context.
        """
        super().__init__(parser_node)
        self._variable_name: str = variable_name

    @property
    def variable_name(self) -> str:
        """Get the name of the variable to access.

        Returns:
            str: The name of the variable that this expression will retrieve from the current scope.
        """
        return self._variable_name

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """Evaluate the expression to retrieve the variable value.

        Performs variable lookup in the current execution context using the scope resolution system.
         This follows the knit script scoping hierarchy, searching through local scopes, parent scopes, module scopes, and global scopes to find the variable.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Any: The value of the variable found in the lowest applicable scope level.
        """
        new_warnings = []
        with warnings.catch_warnings(record=True) as w:
            variable_value = context.variable_scope[self.variable_name]
            for warning in w:
                if isinstance(warning.message, Shadow_Variable_Warning):
                    new_warnings.append(warning.message.__class__(warning.message.variable_name, self))
                else:
                    new_warnings.append(warning)
        for new_warning in new_warnings:
            warnings.warn(new_warning)
        return variable_value

    def __str__(self) -> str:
        return self._variable_name

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(self.variable_name)
