"""Assignment structure.

This module provides the Assignment class, which handles variable assignment operations in knit script programs.
It manages the binding of values to variable names, supporting both local and global variable assignment with proper scope handling.
"""
from typing import Any

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.ks_element import KS_Element


class Assignment(KS_Element):
    """Class for managing assignment expressions.

    Handles the assignment of values to variables in the knit script language, supporting both local and global variable assignment.
     The Assignment class evaluates the value expression in the current context and binds the result to the specified variable name according to the knit script scoping rules.

    This class serves as both a standalone assignment operation and as a component in other language constructs like variable declarations, function parameters, and keyword arguments.

    Attributes:
        _value_expression (Expression): The expression whose value will be assigned to the variable.
        variable_name (str): The name of the variable to assign to.
    """

    def __init__(self, parser_node: LRStackNode, var_name: str, value_expression: Expression) -> None:
        """Initialize an assignment operation.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            var_name (str): The name of the variable to assign to. Must be a valid identifier.
            value_expression (Expression): The expression whose value will be assigned to the variable.
        """
        super().__init__(parser_node)
        self._value_expression: Expression = value_expression
        self.variable_name: str = var_name

    def assign_value(self, context: Knit_Script_Context, is_global: bool = False) -> Any:
        """Assign the evaluated value to the variable.

        Evaluates the value expression and assigns the result to the variable in the appropriate scope.
        The assignment respects the knit script scoping hierarchy and can target either local or global scope.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
            is_global (bool, optional): If True, assigns the variable to the global scope. Otherwise, assigns to the current local scope following normal scoping rules. Defaults to False.

        Returns:
            Any: The value that was assigned to the variable.
        """
        value = self.value(context)
        if is_global:
            context.variable_scope.set_global(self.variable_name, value)
        else:
            context.variable_scope[self.variable_name] = value
        return value

    def value(self, context: Knit_Script_Context) -> Any:
        """Get the value to be assigned by evaluating the expression.

        Evaluates the value expression in the current context to determine what value should be assigned to the variable.

        Args:
            context (Knit_Script_Context): The current execution context to evaluate the value expression.

        Returns:
            Any: The evaluated value that will be assigned to the variable.
        """
        if not isinstance(self._value_expression, Expression):
            expression_result = self._value_expression
        else:
            expression_result = self._value_expression.evaluate(context)
        return expression_result

    def __str__(self) -> str:
        """Return string representation of the assignment.

        Returns:
            str: A string showing the variable name and value expression.
        """
        return f"Assign({self.variable_name} <- {self._value_expression})"

    def __repr__(self) -> str:
        """Return detailed string representation of the assignment.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)
