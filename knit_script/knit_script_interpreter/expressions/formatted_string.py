"""Produces formatted strings"""
from typing import List

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Formatted_String_Value(Expression):
    """
        Follows python fstring conventions
    """

    def __init__(self, parser_node, expressions: List[Expression]):
        """List of expressions in order in formatting
        :param parser_node:
        """
        super().__init__(parser_node)
        self.expressions: List[Expression] = expressions

    def evaluate(self, context: Knit_Script_Context) -> str:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: Evaluates series of string expressions and concatenates them
        """
        # todo: Why are formatted strings messing up spacing
        string = ""
        for exp in self.expressions:
            string += str(exp.evaluate(context))
        return string

    def __str__(self):
        return f"Formatted_Str({self.expressions})"
