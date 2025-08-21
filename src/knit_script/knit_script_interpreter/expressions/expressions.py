"""Base class of all expression values.

This module provides the Expression base class, which serves as the foundation for all expression types in the knit script language.
It also includes utility functions for working with expression collections and converting them to value lists for execution.
"""
from __future__ import annotations

from typing import Any

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.ks_element import KS_Element


class Expression(KS_Element):
    """Superclass for all expressions which evaluate to a value.

    The Expression class provides the base functionality for all evaluable elements in knit script programs.
    It extends KS_Element to include evaluation capabilities, allowing expressions to be processed within a knit script execution context to produce values.

    All knit script expressions inherit from this class and must implement the evaluate method to define how they produce their values during program execution.
     This includes literals, variables, function calls, operators, and complex compound expressions.
    """

    def __init__(self, parser_node: LRStackNode) -> None:
        """Initialize the base expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree that created this expression.
        """
        super().__init__(parser_node)

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """Evaluate the expression to produce a value.

        This method must be overridden by subclasses to define how the expression produces its value during program execution. The base implementation returns None and should not be used directly.

        Args:
            context (Knit_Script_Context): The execution context used to evaluate expressions, containing variable scopes, machine state, and other runtime information.

        Returns:
            Any: The evaluated result of the expression. The specific type depends on the expression implementation.
        """
        return None


def get_expression_value_list(context: Knit_Script_Context, expressions: list[Expression]) -> list[Any]:
    """Convert a list of expressions into a list of their values.

    This utility function evaluates a list of expressions and flattens the results into a single list.
    If any expression evaluates to a list, its elements are extended into the result rather than being added as a nested list.

    Args:
        context (Knit_Script_Context): The execution context to evaluate expressions in.
        expressions (list[Expression]): The list of expressions to convert to values.

    Returns:
        list[Any]: Flattened list of values from the expressions, with list results extended rather than nested.

    Note:
        This function is commonly used in contexts where expressions might evaluate to collections that should be flattened, such as in function argument processing or collection construction.
    """
    values = []
    for exp in expressions:
        value = exp.evaluate(context)
        if isinstance(value, list):
            values.extend(value)
        else:
            values.append(value)
    return values
