"""
Base class of all expression values
"""
from typing import Any, List

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.ks_element import KS_Element


class Expression(KS_Element):
    """
        Super class for all expressions which evaluate to a value
    """
    def __init__(self, parser_node: LRStackNode):
        super().__init__(parser_node)

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """
        :param context: used to evaluate expressions in current program context
        """
        pass


def get_expression_value_list(context: Knit_Script_Context, expressions: List[Expression]):
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
