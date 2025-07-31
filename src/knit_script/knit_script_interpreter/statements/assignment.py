"""Assignment structure"""
from typing import Any

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.ks_element import KS_Element
from knit_script.knit_script_interpreter.scope.machine_scope import Machine_Variables


class Assignment(KS_Element):
    """Class for managing assignment expressions.

    Handles the assignment of values to variables in the knit script language,
    supporting both local and global variable assignment.
    """

    def __init__(self, parser_node: LRStackNode, var_name: str, value_expression: Expression) -> None:
        """Initialize an assignment operation.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            var_name: The name of the variable to assign to.
            value_expression: The expression whose value will be assigned to the variable.
        """
        super().__init__(parser_node)
        self._value_expression: Expression = value_expression
        self.variable_name: str = var_name

    def assign_value(self, context: Knit_Script_Context, is_global: bool = False) -> Any:
        """Assign the evaluated value to the variable.

        Args:
            context: The current execution context of the knit script interpreter.
            is_global: If True, assigns the variable to the global scope.
                Otherwise, assigns to the current local scope.

        Returns:
            The value that was assigned to the variable.
        """
        value = self.value(context)
        if Machine_Variables.in_machine_variables(self.variable_name):  # shortcut for always global variables
            Machine_Variables[self.variable_name].set_value(context, value)
        elif is_global:
            context.variable_scope.set_global(self.variable_name, value)
        else:
            context.variable_scope[self.variable_name] = value
        return value

    def value(self, context: Knit_Script_Context) -> Any:
        """Get the value to be assigned by evaluating the expression.

        Args:
            context: The current execution context to evaluate the value expression.

        Returns:
            The evaluated value that will be assigned to the variable.
        """
        if not isinstance(self._value_expression, Expression):
            expression_result = self._value_expression
        else:
            expression_result = self._value_expression.evaluate(context)
        return expression_result

    def __str__(self) -> str:
        """Return string representation of the assignment.

        Returns:
            A string showing the variable name and value expression.
        """
        return f"Assign({self.variable_name} <- {self._value_expression})"

    def __repr__(self) -> str:
        """Return detailed string representation of the assignment.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)
