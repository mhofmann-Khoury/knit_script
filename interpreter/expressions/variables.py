"""Expression for accessing variables"""
from typing import Any

from interpreter.expressions.expressions import Expression
from interpreter.parser.knit_script_context import Knit_Script_Context


class Variable_Expression(Expression):
    """
        A structure for accessing variables by name from the current context scope
    """

    def __init__(self, variable_name: str):
        """
        Instantiate
        :param variable_name: name of variable
        """
        super().__init__()
        self._variable_name:str = variable_name

    @property
    def variable_name(self)->str:
        """
        :return: name of variable
        """
        return self._variable_name

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """
        Evaluate the expression
        :param context: The current context of the interpreter
        :return: The lowest scope value of the variable by that name
        """
        return context.variable_scope[self.variable_name]

    def __str__(self):
        return f"Var({self.variable_name})"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.variable_name)
