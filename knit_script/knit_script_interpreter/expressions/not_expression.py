"""Expressions for interpreting conditions using Python conventions"""

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Not_Expression(Expression):
    """
        Expression with a "not" negating them
    """

    def __init__(self, parser_node, negated_expression: Expression):
        """
        Instantiate
        :param parser_node:
        :param negated_expression: the expression to negate
        """
        super().__init__(parser_node)
        self._negated_expression: Expression = negated_expression

    def evaluate(self, context: Knit_Script_Context) -> bool:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: Negated expression
        """
        return not self._negated_expression.evaluate(context)

    def __str__(self):
        return f"not {self._negated_expression}"

    def __repr__(self):
        return str(self)
