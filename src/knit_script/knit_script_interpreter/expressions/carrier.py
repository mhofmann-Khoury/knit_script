"""Carrier expression.

This module provides the Carrier_Expression class, which handles the parsing and evaluation of carrier string literals in knit script code.
It converts carrier string identifiers (like "c1", "c2", etc.) into the corresponding Yarn_Carrier objects from the knitting machine's carrier system.
"""
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import (
    Yarn_Carrier,
)

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Carrier_Expression(Expression):
    """Used for processing carrier strings.

    The Carrier_Expression class handles the conversion of carrier string literals in knit script source code into actual Yarn_Carrier objects.
    It parses carrier identifiers that follow the pattern "c" followed by a number (e.g., "c1", "c2", "c10") and retrieves the corresponding carrier from the knitting machine's carrier system.

    This expression type is essential for yarn carrier operations in knit script programs, allowing developers to reference specific carriers by their conventional string identifiers.

    Attributes:
        _carrier_str (str): The original carrier string identifier from the source code.
    """

    def __init__(self, parser_node: LRStackNode, carrier_str: str) -> None:
        """Initialize the Carrier_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            carrier_str (str): The string to identify the carrier from, typically in the format "c" followed by a number (e.g., "c1", "c2").
        """
        super().__init__(parser_node)
        self._carrier_str: str = carrier_str

    def evaluate(self, context: Knit_Script_Context) -> Yarn_Carrier:
        """Evaluate the expression to get the corresponding yarn carrier.

        Parses the carrier string to extract the carrier ID number and retrieves the corresponding Yarn_Carrier object from the knitting machine's carrier system.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Yarn_Carrier: The carrier object with the specified ID from the machine's carrier system.

        Raises:
            ValueError: If the carrier string format is invalid or cannot be parsed.
            KeyError: If the extracted carrier ID does not exist in the machine's carrier system.
        """
        carrier = Yarn_Carrier(int(self._carrier_str[1:]))
        return context.machine_state[carrier]

    def __str__(self) -> str:
        return self._carrier_str

    def __repr__(self) -> str:
        return str(self)
