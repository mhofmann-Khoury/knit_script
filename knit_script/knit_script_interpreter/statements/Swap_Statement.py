"""
    Statement that swaps layers between two needles
"""
from typing import List, Optional

from knit_script.knit_script_interpreter.expressions.expressions import Expression, get_expression_value_list
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knitting_machine.machine_components.needles import Needle


class Swap_Statement(Statement):
    """
        Statement that swaps layers between two needles
    """

    def __init__(self, parser_node, needles: List[Expression], swap_type: str, value: Expression):
        super().__init__(parser_node)
        self._needles = needles
        if swap_type == "sheet":
            self._layer: Optional[Expression] = None
            self._sheet: Optional[Expression] = value
        else:
            self._layer: Optional[Expression] = value
            self._sheet: Optional[Expression] = None

    def execute(self, context: Knit_Script_Context):
        """
        :param context:
        """
        needles = get_expression_value_list(context, self._needles)
        positions = [n.position if isinstance(n, Needle) else int(n) for n in needles]
        if self._layer is None:
            sheet = self._sheet.evaluate(context)
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
                    other_layer = context.machine_state.get_layer_at_position(other_position)
                    if other_layer == layer:
                        context.machine_state.swap_layer_at_positions(needle_pos, other_layer)
            else:
                other_position = needle_pos + (sheet - context.sheet.sheet)
                other_layer = context.machine_state.get_layer_at_position(other_position)
                context.machine_state.swap_layer_at_positions(needle_pos, other_layer)

    def __str__(self):
        if self._layer is None:
            return f"swap {self._needles} with sheet {self._sheet}"
        else:
            return f"swap {self._needles} with layer {self._layer}"

    def __repr__(self):
        return str(self)
