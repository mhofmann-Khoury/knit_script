"""Carrier expression"""
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import Yarn_Carrier

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Carrier_Expression(Expression):
    """
        Used for processing carrier strings
    """

    def __init__(self, parser_node, carrier_str: str):
        """
        Instantiate
        :param parser_node:
        :param carrier_str: the string to identify the carrier from
        """
        super().__init__(parser_node)
        self._carrier_str: str = carrier_str

    def evaluate(self, context: Knit_Script_Context) -> Yarn_Carrier:
        """
        :param context:
        :return: carrier with given integer
        """
        return Yarn_Carrier(int(self._carrier_str[1:]))

    def __str__(self):
        return self._carrier_str

    def __repr__(self):
        return str(self)
