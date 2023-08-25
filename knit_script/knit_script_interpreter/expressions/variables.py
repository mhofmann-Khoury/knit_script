"""Expression for accessing variables"""
from typing import Any

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Variable_Expression(Expression):
    """
        A structure for accessing variables by name from the current context scope
    """

    def __init__(self, parser_node, variable_name: str):
        """
        Instantiate
        :param parser_node:
        :param variable_name: Name of variable
        """
        super().__init__(parser_node)
        self._variable_name: str = variable_name

    @property
    def variable_name(self) -> str:
        """
        :return: name of variable
        """
        return self._variable_name

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: The lowest scope value of the variable by that name
        """
        return context.variable_scope[self.variable_name]

    def __str__(self):
        return self._variable_name

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.variable_name)
