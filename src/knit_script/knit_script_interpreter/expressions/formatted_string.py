"""Produces formatted strings.

This module provides the Formatted_String_Value class, which implements formatted string expressions following Python f-string conventions.
It handles the evaluation and concatenation of mixed string literals and expressions within formatted string contexts.
"""
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Formatted_String_Value(Expression):
    """Follows python fstring conventions.

    The Formatted_String_Value class implements formatted string expressions that mirror Python's f-string functionality.
    It takes a list of expressions that represent the components of a formatted string (both literal string parts and embedded expressions)
    and evaluates them in sequence to produce a concatenated result.

    This allows knit script programs to use dynamic string formatting similar to Python f-strings,
     where expressions can be embedded within string literals and evaluated at runtime to produce formatted output.

    Attributes:
        expressions (list[Expression]): List of expressions in order for string formatting, including both string literals and embedded expressions.
    """

    def __init__(self, parser_node: LRStackNode, expressions: list[Expression]) -> None:
        """Initialize the Formatted_String_Value.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            expressions (list[Expression]): List of expressions in order for string formatting, representing the components of the formatted string.
        """
        super().__init__(parser_node)
        self.expressions: list[Expression] = expressions

    def evaluate(self, context: Knit_Script_Context) -> str:
        """Evaluate the expression to produce a formatted string.

        Evaluates each component expression in sequence and concatenates their string representations to produce the final formatted string result.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            str: The concatenated result of evaluating all component expressions and converting them to strings.
        """
        string = ""
        for exp in self.expressions:
            string += str(exp.evaluate(context))
        return string

    def __str__(self) -> str:
        return f"Formatted_Str({self.expressions})"
