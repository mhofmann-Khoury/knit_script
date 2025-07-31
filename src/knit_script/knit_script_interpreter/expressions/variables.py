"""Expression for accessing variables"""
from typing import Any

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Variable_Expression(Expression):
    """A structure for accessing variables by name from the current context scope."""

    def __init__(self, parser_node: LRStackNode, variable_name: str) -> None:
        """Initialize the Variable_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            variable_name (str): Name of variable.
        """
        super().__init__(parser_node)
        self._variable_name: str = variable_name

    @property
    def variable_name(self) -> str:
        """Get name of variable.

        Returns:
            str: Name of variable.
        """
        return self._variable_name

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Any: The lowest scope value of the variable by that name.
        """
        return context.variable_scope[self.variable_name]

    def __str__(self) -> str:
        return self._variable_name

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(self.variable_name)
