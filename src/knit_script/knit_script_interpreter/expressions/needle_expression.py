"""Expression for identifying needles.

This module provides the Needle_Expression class, which handles the parsing and evaluation of needle identifier strings in knit script programs.
It converts needle string literals into actual Needle objects that respect the current gauging configuration.
"""
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Needle_Expression(Expression):
    """Expression that evaluates to a Needle.

    The Needle_Expression class handles the conversion of needle string identifiers in knit script source code into actual Needle objects.
    It parses needle identifiers that specify bed position, slider status, and needle position, creating the appropriate needle type based on the current gauging configuration.

    Needle identifiers follow the format: [bed][slider][position] where:
    - bed: 'f' for front bed, 'b' for back bed
    - slider: 's' for slider needles (optional)
    - position: numeric position on the bed

    Examples: "f5" (front needle 5), "bs3" (back slider needle 3), "f10" (front needle 10)

    Attributes:
        _needle_str (str): The original needle string identifier from the source code.
    """

    def __init__(self, parser_node: LRStackNode, needle_str: str) -> None:
        """Initialize the Needle_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            needle_str (str): String to parse into a needle identifier, following the format [bed][slider][position].
        """
        super().__init__(parser_node)
        self._needle_str: str = needle_str

    def evaluate(self, context: Knit_Script_Context) -> Needle:
        """Evaluate the expression to create a needle object.

        Parses the needle string identifier to extract bed position, slider status, and needle position,
         then creates the appropriate Needle object using the current gauging configuration from the context.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Needle: The evaluated Needle object based on the string identifier and current gauging configuration.

        Note:
            The needle type (regular or sheet needle) depends on the current gauge setting in the context. The position is interpreted relative to the current sheet and gauge configuration.
        """
        is_front = "f" in self._needle_str
        slider = "s" in self._needle_str
        num_str = self._needle_str[1:]  # cut bed off
        if slider:
            num_str = num_str[1:]  # cut slider off
        pos = int(num_str)
        return context.get_needle(is_front, pos, slider)

    def __str__(self) -> str:
        return self._needle_str

    def __repr__(self) -> str:
        return str(self)
