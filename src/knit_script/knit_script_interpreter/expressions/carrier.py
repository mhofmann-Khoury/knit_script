"""Carrier expression"""
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import Yarn_Carrier

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Carrier_Expression(Expression):
    """Used for processing carrier strings."""

    def __init__(self, parser_node: LRStackNode, carrier_str: str) -> None:
        """Initialize the Carrier_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            carrier_str (str): The string to identify the carrier from.
        """
        super().__init__(parser_node)
        self._carrier_str: str = carrier_str

    def evaluate(self, context: Knit_Script_Context) -> Yarn_Carrier:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Yarn_Carrier: Carrier with given integer.
        """
        carrier = Yarn_Carrier(int(self._carrier_str[1:]))
        return context.machine_state[carrier]

    def __str__(self) -> str:
        return self._carrier_str

    def __repr__(self) -> str:
        return str(self)
