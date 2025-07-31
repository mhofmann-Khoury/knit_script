"""Base class of all expression values"""
from __future__ import annotations
from typing import Any

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.ks_element import KS_Element


class Expression(KS_Element):
    """Superclass for all expressions which evaluate to a value."""

    def __init__(self, parser_node: LRStackNode) -> None:
        super().__init__(parser_node)

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): Used to evaluate expressions in the current program context.

        Returns:
            Any: The evaluated result.
        """
        return None


def get_expression_value_list(context: Knit_Script_Context, expressions: list[Expression]) -> list[Any]:
    """Convert a list of expressions into a list of their values.

    Extends when expressions produce another list.

    Args:
        context (Knit_Script_Context): Context to evaluate at.
        expressions (list[Expression]): Expressions to convert to a list.

    Returns:
        list[Any]: Flattened list of values from the expressions.
    """
    values = []
    for exp in expressions:
        value = exp.evaluate(context)
        if isinstance(value, list):
            values.extend(value)
        else:
            values.append(value)
    return values
