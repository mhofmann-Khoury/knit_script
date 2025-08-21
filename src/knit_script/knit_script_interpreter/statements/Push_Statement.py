"""Statements that change the layer position of needles.

This module provides the Push_Statement class, which handles layer position modifications for needles in multi-sheet gauge configurations.
It allows control over the stacking hierarchy of stitches, enabling complex knitting patterns that require specific layer arrangements.
"""
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_interpreter.expressions.expressions import (
    Expression,
    get_expression_value_list,
)
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Push_Statement(Statement):
    """Pushes needles to specified layer positions in the stacking hierarchy.

    This statement modifies the layering order of stitches on needles, allowing control over which stitches appear in front or back of others in the final knitted fabric.
    Supports absolute positioning to specific layers, relative movement by distance, and convenient front/back positioning.

    The push operation is essential for complex multi-sheet knitting where the layer ordering affects the final fabric structure and appearance.
    After modifying layer positions, the statement automatically resets to the current sheet to ensure the changes are properly applied.

    Attributes:
        _needles (list[Expression]): List of expressions that evaluate to needles whose layers should be repositioned.
        _push_val (str | Expression | tuple[Expression, str]): The positioning instruction specification.
    """

    def __init__(self, parser_node: LRStackNode, needles: list[Expression], push_val: str | Expression | tuple[Expression, str]) -> None:
        """Initialize a push statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            needles (list[Expression]): List of expressions that evaluate to needles whose layers should be repositioned.
            push_val (str | Expression | tuple[Expression, str]): The positioning instruction, which can be a string for absolute positioning ("front" or "back"),
            an Expression for absolute layer position as integer, or a tuple of (distance_expression, direction_string) for relative movement where direction is "forward" or "backward".
        """
        super().__init__(parser_node)
        self._needles: list[Expression] = needles
        self._push_val: str | Expression | tuple[Expression, str] = push_val

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the push operation on the specified needles.

        Evaluates all needle expressions and applies the positioning operation to each needle's layer in the gauged sheet record.
        Supports absolute positioning, relative movement, and convenient front/back shortcuts. After all modifications, resets to the current sheet to apply changes.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
        """
        needles = get_expression_value_list(context, self._needles)
        positions = [n.position if isinstance(n, Needle) else int(n) for n in needles]

        for needle_pos in positions:
            if isinstance(self._push_val, Expression):
                pos = int(self._push_val.evaluate(context))
                context.gauged_sheet_record.set_layer_position(needle_pos, pos)
            elif isinstance(self._push_val, str):
                if self._push_val.lower() == "front":
                    context.gauged_sheet_record.set_layer_to_front(needle_pos)
                elif self._push_val.lower() == "back":
                    context.gauged_sheet_record.set_layer_to_back(needle_pos)
            else:
                assert isinstance(self._push_val, tuple)
                dist = int(self._push_val[0].evaluate(context))
                direction = self._push_val[1].lower()
                if direction == "forward":
                    context.gauged_sheet_record.push_layer_forward(needle_pos, dist)
                else:
                    context.gauged_sheet_record.push_layer_backward(needle_pos, dist)
        context.knitout.extend(context.gauged_sheet_record.reset_to_sheet(context.sheet.sheet))

    def __str__(self) -> str:
        """Return string representation of the push statement.

        Returns:
            str: A string showing the needles and push operation.
        """
        return f"push {self._needles} {self._push_val}"

    def __repr__(self) -> str:
        """Return detailed string representation of the push statement.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)
