"""Statements that change the layer position of needles"""
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_interpreter.expressions.expressions import Expression, get_expression_value_list
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Push_Statement(Statement):
    """Pushes needles to specified layer positions in the stacking hierarchy.

    This statement modifies the layering order of stitches on needles, allowing
    control over which stitches appear in front or back of others in the final
    knitted fabric. Supports absolute positioning, relative movement, and
    front/back positioning.
    """

    def __init__(self, parser_node: LRStackNode, needles: list[Expression], push_val: str | Expression | tuple[Expression, str]) -> None:
        """Initialize a push statement.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            needles: List of expressions that evaluate to needles whose layers
                should be repositioned.
            push_val: The positioning instruction, which can be:
                - str: "front" or "back" for absolute positioning
                - Expression: Absolute layer position as integer
                - tuple: (distance_expression, direction_string) for relative movement
                  where direction is "forward" or "backward"
        """
        super().__init__(parser_node)
        self._needles: list[Expression] = needles
        self._push_val: str | Expression | tuple[Expression, str] = push_val

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the push operation on the specified needles.

        Evaluates all needle expressions and applies the positioning operation
        to each needle's layer in the gauged sheet record.

        Args:
            context: The current execution context of the knit script interpreter.
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
            A string showing the needles and push operation.
        """
        return f"push {self._needles} {self._push_val}"

    def __repr__(self) -> str:
        """Return detailed string representation of the push statement.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)
