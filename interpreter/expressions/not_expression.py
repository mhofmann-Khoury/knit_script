"""Expressions for interpreting conditions using Python conventions"""

from interpreter.expressions.expressions import Expression
from interpreter.parser.knit_script_context import Knit_Script_Context


class Not_Expression(Expression):
    """
        Expression with a "not" negating them
    """

    def __init__(self, negated_expression: Expression):
        """
        Instantiate
        :param negated_expression: the expression to negate
        """
        super().__init__()
        self._negated_expression:Expression = negated_expression

    def evaluate(self, context: Knit_Script_Context) -> bool:
        """
        Evaluate the expression
        :param context: The current context of the interpreter
        :return: Negated expression
        """
        return not self._negated_expression.evaluate(context)

    def __str__(self):
        return f"not {self._negated_expression}"

    def __repr__(self):
        return str(self)
