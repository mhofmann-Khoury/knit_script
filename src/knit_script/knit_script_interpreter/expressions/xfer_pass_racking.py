"""Calculates racking for xfers"""
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.knit_script_values.Machine_Specification import Machine_Position


class Xfer_Pass_Racking(Expression):
    """
        structures racking direction.
    """

    def __init__(self, parser_node, is_across: bool, distance_expression: Expression | None = None, side: Expression | None = None):
        """
        Instantiate
        :param parser_node:
        :param is_across: true if xfer is directly across beds
        :param distance_expression: the needle offset for xfer
        :param side: offset direction
        """
        super().__init__(parser_node)
        self._side: Expression | None = side
        self._is_across: bool = is_across
        if self._is_across:
            self._distance_expression = 0
        self._distance_expression: Expression | None = distance_expression

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
            if isinstance(direction, Carriage_Pass_Direction):
                if direction is Carriage_Pass_Direction.Leftward:
                    direction = Machine_Position.Left
                else:
                    direction = Machine_Position.Right
            if not isinstance(direction, Machine_Position) or not direction.is_direction:
                raise TypeError(f"KS:{self.line_number}: Expected Left or Right Direction but got {direction}")
            if direction is Machine_Position.Left:
                return Knitting_Machine.get_rack(front_pos=0, back_pos=-1 * distance)
            else:
                return Knitting_Machine.get_rack(front_pos=0, back_pos=distance)

    def __str__(self):
        if self._is_across:
            return "Rack(0)"
        return f'Rack({self._distance_expression} to {self._side})'

    def __repr__(self):
        return str(self)
