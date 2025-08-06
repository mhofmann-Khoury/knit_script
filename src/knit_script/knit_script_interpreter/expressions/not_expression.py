"""Expressions for interpreting conditions using Python conventions.

This module provides the Not_Expression class, which implements logical negation operations in knit script programs. It follows Python's truthiness conventions for evaluating and negating expressions.
"""
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Not_Expression(Expression):
    """Expression with a "not" operator negating them.

    The Not_Expression class implements logical negation operations following Python's conventions for truthiness evaluation.
    It takes any expression and returns the logical negation of its evaluated result, converting the result to a boolean using Python's standard truthiness rules.

    This expression type is essential for conditional logic in knit script programs,
     allowing developers to negate boolean conditions, check for empty collections, None values, and other false conditions.

    Attributes:
        _negated_expression (Expression): The expression to logically negate.
    """

    def __init__(self, parser_node: LRStackNode, negated_expression: Expression) -> None:
        """Initialize the Not_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            negated_expression (Expression): The expression to apply logical negation to.
        """
        super().__init__(parser_node)
        self._negated_expression: Expression = negated_expression

    def evaluate(self, context: Knit_Script_Context) -> bool:
        """Evaluate the expression to get the logical negation result.

        Evaluates the contained expression and returns its logical negation, following Python's truthiness conventions where empty collections, None, zero values, and False are considered false.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            bool: The logical negation of the evaluated expression result.
        """
        return not self._negated_expression.evaluate(context)

    def __str__(self) -> str:
        return f"not {self._negated_expression}"

    def __repr__(self) -> str:
        return str(self)
