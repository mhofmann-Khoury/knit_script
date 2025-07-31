"""Expression for identifying needles"""
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Needle_Expression(Expression):
    """Expression that evaluates to a Needle."""

    def __init__(self, parser_node: LRStackNode, needle_str: str) -> None:
        """Initialize the Needle_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            needle_str (str): String to parse to a needle.
        """
        super().__init__(parser_node)
        self._needle_str: str = needle_str

    def evaluate(self, context: Knit_Script_Context) -> Needle:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Needle: Evaluation of the Needle Expression.
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
