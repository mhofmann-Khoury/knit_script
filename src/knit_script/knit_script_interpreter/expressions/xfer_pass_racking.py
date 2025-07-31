"""Calculates racking for xfers"""
from parglare.parser import LRStackNode
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.knit_script_values.Machine_Specification import Xfer_Direction


class Xfer_Pass_Racking(Expression):
    """Structures racking direction."""

    def __init__(self, parser_node: LRStackNode, distance_expression: Expression | None = None, direction_expression: Expression | None = None) -> None:
        """Initialize the Xfer_Pass_Racking.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            distance_expression (Expression | None, optional): The needle offset for xfer.
            direction_expression (Expression | None, optional): Offset direction.
        """
        super().__init__(parser_node)
        self._direction_expression: Expression | None = direction_expression
        self._distance_expression: Expression | None = distance_expression

    @property
    def is_across(self) -> bool:
        """
        Returns:
            True if the xfer occurs with a 0 racking that does not depend on any variables.
        """
        return self._distance_expression is None

    def evaluate(self, context: Knit_Script_Context) -> int:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            int: Racking integer value to align needles.
        """
        if self.is_across:
            return 0
        else:
            assert isinstance(self._distance_expression, Expression)
            distance = int(self._distance_expression.evaluate(context))
            assert isinstance(self._direction_expression, Expression)
            direction = self._direction_expression.evaluate(context)
            if isinstance(direction, Carriage_Pass_Direction):
                if direction is Carriage_Pass_Direction.Leftward:
                    direction = Xfer_Direction.Left
                else:
                    direction = Xfer_Direction.Right
            if not isinstance(direction, Xfer_Direction):
                raise TypeError(f"KS:{self.line_number}: Expected Left or Right Direction but got {direction}")
            if direction is Xfer_Direction.Left:
                return int(Knitting_Machine.get_rack(front_pos=0, back_pos=-1 * distance))
            else:
                return int(Knitting_Machine.get_rack(front_pos=0, back_pos=distance))

    def __str__(self) -> str:
        if self.is_across:
            return "Rack(0)"
        return f'Rack({self._distance_expression} to {self._direction_expression})'

    def __repr__(self) -> str:
        return str(self)
