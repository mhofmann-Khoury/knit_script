"""Produces formatted strings"""
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Formatted_String_Value(Expression):
    """Follows python fstring conventions."""

    def __init__(self, parser_node: LRStackNode, expressions: list[Expression]) -> None:
        """Initialize the Formatted_String_Value.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            expressions (list[Expression]): List of expressions in order in formatting.
        """
        super().__init__(parser_node)
        self.expressions: list[Expression] = expressions

    def evaluate(self, context: Knit_Script_Context) -> str:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            str: Evaluates series of string expressions and concatenates them.
        """
        string = ""
        for exp in self.expressions:
            string += str(exp.evaluate(context))
        return string

    def __str__(self) -> str:
        return f"Formatted_Str({self.expressions})"
