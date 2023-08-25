"""Expression for identifying needles"""
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knitting_machine.machine_components.needles import Needle


class Needle_Expression(Expression):
    """
        Expression that evaluates to a Needle
    """

    def __init__(self, parser_node, needle_str: str):
        """
        Instantiate
        :param parser_node:
        :param needle_str: string to parse to a needle
        """
        super().__init__(parser_node)
        self._needle_str:str = needle_str

    def evaluate(self, context: Knit_Script_Context) -> Needle:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: Evaluation of the Needle Expression
        """
        is_front = "f" in self._needle_str
        slider = "s" in self._needle_str
        num_str = self._needle_str[1:]  # cut bed off
        if slider:
            num_str = num_str[1:]  # cut slider off
        pos = int(num_str)
        return context.get_needle(is_front, pos, slider)

    def __str__(self):
        return self._needle_str

    def __repr__(self):
        return str(self)
