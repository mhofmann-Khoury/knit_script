"""Calculates racking for xfers"""

from typing import Optional

from interpreter.expressions.expressions import Expression
from interpreter.expressions.values import Bed_Side
from interpreter.parser.knit_pass_context import Knit_Script_Context
from knitting_machine.Machine_State import Machine_State


class Xfer_Pass_Racking(Expression):
    """
        structures racking direction
    """

    def __init__(self, is_across: bool,
                 distance_expression: Optional[Expression] = None,
                 side: Optional[Expression] = None):
        """
        Instantiate
        :param is_across: true if xfer is directly across beds
        :param distance_expression: the needle offset for xfer
        :param side: offset direction
        """
        super().__init__()
        self._side: Optional[Expression] = side
        self._is_across:bool = is_across
        if self._is_across:
            self._distance_expression = 0
        self._distance_expression: Optional[Expression] = distance_expression

    def evaluate(self, context: Knit_Script_Context) -> int:
        """
        Evaluate the expression
        :param context: The current context of the interpreter
        :return: racking integer value to align needles
        """
        if self._is_across:
            return 0
        else:
            distance = int(self._distance_expression.evaluate(context))
            direction = self._side.evaluate(context)
            assert isinstance(direction, Bed_Side), f"Expected Left or Right Direction but got {direction}"
            if direction is Bed_Side.Left:
                return Machine_State.get_rack(front_pos=0, back_pos=distance)
            else:
                return Machine_State.get_rack(front_pos=0, back_pos=-1 * distance)

    def __str__(self):
        if self._is_across:
            return "Rack(0)"
        return f'Rack({self._distance_expression} to {self._side})'

    def __repr__(self):
        return str(self)
