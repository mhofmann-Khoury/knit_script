"""Accesses machine directions.

This module provides the Pass_Direction_Expression class, which handles the parsing and evaluation of carriage pass direction expressions in knit script code.
It supports various direction keywords and contextual direction references, converting them into the appropriate Carriage_Pass_Direction objects.
"""
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import (
    Carriage_Pass_Direction,
)

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Pass_Direction_Expression(Expression):
    """Expression of a Machine Pass Direction.

    The Pass_Direction_Expression class handles the conversion of direction keywords in knit script source code into Carriage_Pass_Direction objects.
    It supports both explicit direction keywords (like "Leftward", "Rightward") and contextual references (like "current", "reverse") that depend on the current machine state.

    This expression type is essential for carriage pass operations where the direction of needle processing must be specified.
    It provides flexibility in how directions are specified while ensuring they resolve to the correct machine direction values.

    Attributes:
        _dir_word (str): The direction keyword from the source code.
    """

    def __init__(self, parser_node: LRStackNode, dir_word: str) -> None:
        """Initialize the Pass_Direction_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            dir_word (str): Keyword for the direction, such as "Leftward", "Rightward", "current", or "reverse".
        """
        super().__init__(parser_node)
        self._dir_word: str = dir_word

    def evaluate(self, context: Knit_Script_Context) -> Carriage_Pass_Direction:
        """Evaluate the expression to get the corresponding carriage pass direction.

        Converts the direction keyword into the appropriate Carriage_Pass_Direction object, handling both explicit directions and contextual references that depend on the current machine state.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Carriage_Pass_Direction: The carriage pass direction corresponding to the keyword.

        Note:
            Supported keywords:
            - "Leftward", "Decreasing": Returns leftward direction
            - "Rightward", "Increasing": Returns rightward direction
            - "current": Returns the current direction from context
            - "reverse": Returns the opposite of the current direction
        """
        if self._dir_word in ["Leftward", "Decreasing"]:
            return Carriage_Pass_Direction.Leftward
        elif self._dir_word in ["Rightward", "Increasing"]:
            return Carriage_Pass_Direction.Rightward
        elif self._dir_word.lower() == "current":
            return context.direction
        elif self._dir_word.lower() == "reverse":
            return context.direction.opposite()

    def __str__(self) -> str:
        return f"{self._dir_word}"

    def __repr__(self) -> str:
        return str(self)
