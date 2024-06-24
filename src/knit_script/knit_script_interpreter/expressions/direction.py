"""Accesses machine directions"""
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Pass_Direction_Expression(Expression):
    """
    Expression of a Machine Pass Direction
    """

    def __init__(self, parser_node, dir_word: str):
        """
        Instantiate
        :param parser_node:
        :param dir_word: keyword for the direction
        """
        super().__init__(parser_node)
        self._dir_word: str = dir_word

    def evaluate(self, context: Knit_Script_Context) -> Carriage_Pass_Direction:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: Pass_Direction from evaluation
        """
        if self._dir_word in ["Leftward", "Decreasing", "<--"]:
            return Carriage_Pass_Direction.Leftward
        elif self._dir_word in ["Rightward", "Increasing", "-->"]:
            return Carriage_Pass_Direction.Rightward
        elif self._dir_word.lower() == "current":
            return context.direction
        elif self._dir_word.lower() == "reverse":
            return context.direction.opposite()

    def __str__(self):
        return f"{self._dir_word}"

    def __repr__(self):
        return str(self)
