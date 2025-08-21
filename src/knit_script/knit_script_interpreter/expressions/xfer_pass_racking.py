"""Calculates racking for xfers.

This module provides the Xfer_Pass_Racking class, which handles the calculation of racking values for transfer operations in knit script programs.
It supports both direct across-bed transfers (zero racking) and offset transfers with specified distances and directions.
"""
from parglare.parser import LRStackNode
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import (
    Carriage_Pass_Direction,
)

from knit_script.knit_script_exceptions.python_style_exceptions import (
    Knit_Script_TypeError,
)
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Xfer_Pass_Racking(Expression):
    """Structures racking direction for transfer operations.

    The Xfer_Pass_Racking class calculates the appropriate racking value for transfer operations between needle beds.
    It supports both direct across-bed transfers (where needles are directly opposite each other) and offset transfers where needles are shifted by a specified distance in a particular direction.

    Transfer operations require precise racking calculations to ensure that loops are transferred to the correct target needles.
    This class handles the complexity of converting directional distance specifications into the numeric racking values required by the knitting machine.

    Attributes:
        _distance_expression (Expression | None): Optional expression for the needle offset distance.
        _direction_expression (Expression | None): Optional expression for the offset direction.
    """

    def __init__(self, parser_node: LRStackNode, distance_expression: Expression | None = None, direction_expression: Expression | None = None) -> None:
        """Initialize the Xfer_Pass_Racking expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            distance_expression (Expression | None, optional): The needle offset distance expression for transfer operations. If None, indicates a direct across-bed transfer. Defaults to None.
            direction_expression (Expression | None, optional): The direction expression indicating which way the offset should be applied.
            Required when distance_expression is provided. Defaults to None.
        """
        super().__init__(parser_node)
        self._direction_expression: Expression | None = direction_expression
        self._distance_expression: Expression | None = distance_expression

    @property
    def is_across(self) -> bool:
        """Check if this represents a direct across-bed transfer.

        Returns:
            bool: True if the transfer occurs with zero racking (directly across beds) and does not depend on any variable expressions.
        """
        return self._distance_expression is None

    def evaluate(self, context: Knit_Script_Context) -> int:
        """Evaluate the expression to calculate the racking value.

        Calculates the appropriate racking value for the transfer operation. For across-bed transfers, returns zero.
        For offset transfers, evaluates the distance and direction expressions and calculates the racking needed to align the source and target needles.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            int: The racking integer value needed to align needles for the transfer operation.

        Raises:
            TypeError: If the direction expression does not evaluate to a Carriage_Pass_Direction.
            AssertionError: If distance_expression is None when is_across is False, or if direction_expression is None when distance is specified.
        """
        if self.is_across:
            return 0
        else:
            assert isinstance(self._distance_expression, Expression)
            distance = int(self._distance_expression.evaluate(context))
            assert isinstance(self._direction_expression, Expression)
            direction = self._direction_expression.evaluate(context)
            if not isinstance(direction, Carriage_Pass_Direction):
                raise Knit_Script_TypeError(f"Expected Left or Right Direction but got {direction}", self)
            if direction is Carriage_Pass_Direction.Leftward:
                return int(Knitting_Machine.get_rack(front_pos=0, back_pos=-1 * distance))
            else:
                return int(Knitting_Machine.get_rack(front_pos=0, back_pos=distance))

    def __str__(self) -> str:
        if self.is_across:
            return "Rack(0)"
        return f'Rack({self._distance_expression} to {self._direction_expression})'

    def __repr__(self) -> str:
        return str(self)
