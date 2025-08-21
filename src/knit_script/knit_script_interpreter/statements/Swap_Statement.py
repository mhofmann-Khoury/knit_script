"""Statement that swaps layers between two needles.

This module provides the Swap_Statement class, which handles layer position exchanges between needles in multi-sheet gauge configurations.
It supports both layer-based swapping and sheet-based swapping for complex stitch organization.
"""
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.needles.Needle import Needle
from virtual_knitting_machine.machine_components.needles.Sheet_Identifier import (
    Sheet_Identifier,
)

from knit_script.knit_script_exceptions.python_style_exceptions import (
    Knit_Script_TypeError,
)
from knit_script.knit_script_interpreter.expressions.expressions import (
    Expression,
    get_expression_value_list,
)
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Swap_Statement(Statement):
    """Statement that swaps stitch layers between needles.

    This statement exchanges the layer positioning of stitches either between specific layer numbers or between needles on different sheets of a multi-sheet gauge setup.
    The swap operation allows for complex stitch organization and layer management in advanced knitting patterns.

    The statement supports two types of swapping: layer swaps that exchange positions with needles at specific layer indices,
     and sheet swaps that exchange positions between corresponding needles on different sheets.

    Attributes:
        _needles (list[Expression]): List of expressions that evaluate to needles whose layers should be swapped.
        _layer (Expression | None): Expression for layer-based swapping.
        _sheet (Expression | None): Expression for sheet-based swapping.
    """

    def __init__(self, parser_node: LRStackNode, needles: list[Expression], swap_type: str, value: Expression) -> None:
        """Initialize a swap statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            needles (list[Expression]): List of expressions that evaluate to needles whose layers should be swapped.
            swap_type (str): Type of swap operation, either "sheet" for swapping between sheets or "layer" for swapping with specific layer positions.
            value (Expression): Expression that evaluates to either a sheet number (for sheet swaps) or layer number (for layer swaps).
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

        For layer swaps, finds needles with the specified layer number and swaps their positions with the target needles.
         For sheet swaps, swaps layers between needles on different sheets at corresponding positions within the gauge configuration.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.

        Raises:
            TypeError: If sheet or layer values are not integers.
        """
        needles = get_expression_value_list(context, self._needles)
        positions = [n.position if isinstance(n, Needle) else int(n) for n in needles]
        if self._layer is None:
            assert isinstance(self._sheet, Expression)
            sheet = self._sheet.evaluate(context)
            if isinstance(sheet, Sheet_Identifier):
                sheet = sheet.sheet
            if not isinstance(sheet, int):
                raise Knit_Script_TypeError(f"Expected an integer for a sheet but got {sheet}", self)
            layer = None
        else:
            layer = self._layer.evaluate(context)
            if not isinstance(layer, int):
                raise Knit_Script_TypeError(f"Expected an integer for a layer but got {layer}", self)
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
            str: A string showing the needles and swap operation type.
        """
        if self._layer is None:
            return f"swap {self._needles} with sheet {self._sheet}"
        else:
            return f"swap {self._needles} with layer {self._layer}"

    def __repr__(self) -> str:
        """Return detailed string representation of the swap statement.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)
