"""Expressions for interpreting conditions using Python conventions"""
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Not_Expression(Expression):
    """Expression with a "not" negating them."""

    def __init__(self, parser_node: LRStackNode, negated_expression: Expression) -> None:
        """Initialize the Not_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            negated_expression (Expression): The expression to negate.
        """
        super().__init__(parser_node)
        self._negated_expression: Expression = negated_expression

    def evaluate(self, context: Knit_Script_Context) -> bool:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            bool: Negated expression.
        """
        return not self._negated_expression.evaluate(context)

    def __str__(self) -> str:
        return f"not {self._negated_expression}"

    def __repr__(self) -> str:
        return str(self)
