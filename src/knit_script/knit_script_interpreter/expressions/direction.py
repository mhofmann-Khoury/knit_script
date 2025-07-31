"""Accesses machine directions"""
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Pass_Direction_Expression(Expression):
    """Expression of a Machine Pass Direction."""

    def __init__(self, parser_node: LRStackNode, dir_word: str) -> None:
        """Initialize the Pass_Direction_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            dir_word (str): Keyword for the direction.
        """
        super().__init__(parser_node)
        self._dir_word: str = dir_word

    def evaluate(self, context: Knit_Script_Context) -> Carriage_Pass_Direction:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Carriage_Pass_Direction: Pass_Direction from evaluation.
        """
        if self._dir_word in ["Leftward", "Decreasing", "<--"]:
            return Carriage_Pass_Direction.Leftward
        elif self._dir_word in ["Rightward", "Increasing", "-->"]:
            return Carriage_Pass_Direction.Rightward
        elif self._dir_word.lower() == "current":
            return context.direction
        elif self._dir_word.lower() == "reverse":
            return context.direction.opposite()

    def __str__(self) -> str:
        return f"{self._dir_word}"

    def __repr__(self) -> str:
        return str(self)
