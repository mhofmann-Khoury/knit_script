"""Accesses machine directions"""
from interpreter.expressions.expressions import Expression
from interpreter.parser.knit_script_context import Knit_Script_Context
from knitting_machine.machine_components.machine_pass_direction import Pass_Direction


class Pass_Direction_Expression(Expression):
    """
    Expression of a Machine Pass Direction
    """

    def __init__(self, dir_word: str):
        """
        Instantiate
        :param dir_word: keyword for the direction
        """
        super().__init__()
        self._dir_word:str = dir_word

    def evaluate(self, context: Knit_Script_Context) -> Pass_Direction:
        """
        Evaluate the expression
        :param context: The current context of the interpreter
        :return: Pass_Direction from evaluation
        """
        if self._dir_word in ["Leftward", "Decreasing", "<--"]:
            return Pass_Direction.Right_to_Left_Decreasing
        elif self._dir_word in ["Rightward", "Increasing", "-->"]:
            return Pass_Direction.Left_to_Right_Increasing
        elif self._dir_word.lower() == "current" or self._dir_word.lower() == "repeat":
            return context.current_direction
        elif self._dir_word.lower() == "opposite" or self._dir_word.lower() == "reverse":
            return context.current_direction.opposite()

    def __str__(self):
        return f"{self._dir_word}"

    def __repr__(self):
        return str(self)
