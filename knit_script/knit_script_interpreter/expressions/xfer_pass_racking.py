"""Calculates racking for xfers"""

from typing import Optional

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knitting_machine.Machine_State import Machine_State
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.machine_position import Machine_Position


class Xfer_Pass_Racking(Expression):
    """
        structures racking direction
    """

    def __init__(self, parser_node, is_across: bool, distance_expression: Optional[Expression] = None, side: Optional[Expression] = None):
        """
        Instantiate
        :param parser_node:
        :param is_across: true if xfer is directly across beds
        :param distance_expression: the needle offset for xfer
        :param side: offset direction
        """
        super().__init__(parser_node)
        self._side: Optional[Expression] = side
        self._is_across: bool = is_across
        if self._is_across:
            self._distance_expression = 0
        self._distance_expression: Optional[Expression] = distance_expression

    def evaluate(self, context: Knit_Script_Context) -> int:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: racking integer value to align needles
        """
        if self._is_across:
            return 0
        else:
            distance = int(self._distance_expression.evaluate(context))
            direction = self._side.evaluate(context)
            if isinstance(direction, Pass_Direction):
                if direction is Pass_Direction.Leftward:
                    direction = Machine_Position.Left
                else:
                    direction = Machine_Position.Right
            if not isinstance(direction, Machine_Position) or not direction.is_direction:
                raise TypeError(f"KS:{self.line_number}: Expected Left or Right Direction but got {direction}")
            if direction is Machine_Position.Left:
                return Machine_State.get_rack(front_pos=0, back_pos=-1 * distance)
            else:
                return Machine_State.get_rack(front_pos=0, back_pos=distance)

    def __str__(self):
        if self._is_across:
            return "Rack(0)"
        return f'Rack({self._distance_expression} to {self._side})'

    def __repr__(self):
        return str(self)
