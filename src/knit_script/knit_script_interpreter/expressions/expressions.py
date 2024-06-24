"""
Base class of all expression values
"""

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.ks_element import KS_Element


class Expression(KS_Element):
    """
        Superclass for all expressions which evaluate to a value
    """
    def __init__(self, parser_node: LRStackNode):
        super().__init__(parser_node)

    def evaluate(self, context: Knit_Script_Context):
        """
        :param context: Used to evaluate expressions in the current program context.
        """
        return None


def get_expression_value_list(context: Knit_Script_Context, expressions: list[Expression]) -> list:
    """
    Converts a list of expressions into a list of their values. Extends when expressions produce another list
    :param context: context to evaluate at
    :param expressions: expressions to convert to a list
    :return: Flattened list of values from the expressions
    """
    values = []
    for exp in expressions:
        value = exp.evaluate(context)
        if isinstance(value, list):
            values.extend(value)
        else:
            values.append(value)
    return values
