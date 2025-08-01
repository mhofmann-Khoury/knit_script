"""Statement that swaps layers between two needles"""
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.needles.Needle import Needle
from virtual_knitting_machine.machine_components.needles.Sheet_Needle import Sheet_Identifier

from knit_script.knit_script_interpreter.expressions.expressions import Expression, get_expression_value_list
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Swap_Statement(Statement):
    """Statement that swaps stitch layers between needles.

    This statement exchanges the layer positioning of stitches either between
    specific layer numbers or between needles on different sheets of a
    multi-sheet gauge setup.
    """

    def __init__(self, parser_node: LRStackNode, needles: list[Expression], swap_type: str, value: Expression) -> None:
        """Initialize a swap statement.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            needles: List of expressions that evaluate to needles whose layers
                should be swapped.
            swap_type: Type of swap operation, either "sheet" or "layer".
            value: Expression that evaluates to either a sheet number (for sheet swaps)
                or layer number (for layer swaps).
        """
        super().__init__(parser_node)
        self._needles = needles
        if swap_type == "sheet":
            self._layer: Expression | None = None
            self._sheet: Expression | None = value
        else:
            self._layer: Expression | None = value
            self._sheet: Expression | None = None

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the swap operation on the specified needles.

        For layer swaps, finds needles with the specified layer number and swaps
        their positions. For sheet swaps, swaps layers between needles on
        different sheets at corresponding positions.

        Args:
            context: The current execution context of the knit script interpreter.

        Raises:
            AssertionError: If sheet or layer values are not integers.
        """
        needles = get_expression_value_list(context, self._needles)
        positions = [n.position if isinstance(n, Needle) else int(n) for n in needles]
        if self._layer is None:
            assert isinstance(self._sheet, Expression)
            sheet = self._sheet.evaluate(context)
            if isinstance(sheet, Sheet_Identifier):
                sheet = sheet.sheet
            assert isinstance(sheet, int), f"Expected an integer for a sheet but got {sheet}"
            layer = None
        else:
            layer = self._layer.evaluate(context)
            assert isinstance(layer, int), f"Expected an integer for a layer but got {layer}"
            sheet = None
        for needle_pos in positions:
            if layer is not None:
                positions = [needle_pos + (s - context.sheet.sheet) for s in range(0, context.gauge) if s != context.sheet.sheet]
                for other_position in positions:
                    other_layer = context.gauged_sheet_record.get_layer_at_position(other_position)
                    if other_layer == layer:
                        context.gauged_sheet_record.swap_layer_at_positions(needle_pos, other_layer)
            else:
                other_position = needle_pos + (sheet - context.sheet.sheet)
                other_layer = context.gauged_sheet_record.get_layer_at_position(other_position)
                context.gauged_sheet_record.swap_layer_at_positions(needle_pos, other_layer)

    def __str__(self) -> str:
        """Return string representation of the swap statement.

        Returns:
            A string showing the needles and swap operation type.
        """
        if self._layer is None:
            return f"swap {self._needles} with sheet {self._sheet}"
        else:
            return f"swap {self._needles} with layer {self._layer}"

    def __repr__(self) -> str:
        """Return detailed string representation of the swap statement.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)
