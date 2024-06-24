"""Statements that change the layer position of needles"""
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_interpreter.expressions.expressions import Expression, get_expression_value_list
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Push_Statement(Statement):
    """
        Pushes a layer to a specified position in hierarchy
    """

    def __init__(self, parser_node, needles: list[Expression], push_val: str | Expression | tuple[Expression, str]):
        """
        Instantiate
        :param parser_node:
        :param needles: Needles to change layering.
        :param push_val: Direction, set to value, or direction with a given value
        """
        super().__init__(parser_node)
        self._needles: list[Expression] = needles
        self._push_val: str | Expression | tuple[Expression, str] = push_val

    def execute(self, context: Knit_Script_Context):
        """
        Pushes specified needle layers by parameters
        :param context: The current context of the knit_script_interpreter
        """
        needles = get_expression_value_list(context, self._needles)
        positions = [n.position if isinstance(n, Needle) else int(n) for n in needles]

        for needle_pos in positions:
            if isinstance(self._push_val, Expression):
                pos = int(self._push_val.evaluate(context))
                context.machine_state.set_layer_position(needle_pos, pos)
            elif isinstance(self._push_val, str):
                if self._push_val.lower() == "front":
                    context.machine_state.set_layer_to_front(needle_pos)
                elif self._push_val.lower() == "back":
                    context.machine_state.set_layer_to_back(needle_pos)
            else:
                assert isinstance(self._push_val, tuple)
                dist = int(self._push_val[0].evaluate(context))
                direction = self._push_val[1].lower()
                if direction == "forward":
                    context.machine_state.push_layer_forward(needle_pos, dist)
                else:
                    context.machine_state.push_layer_backward(needle_pos, dist)
        context.knitout.extend(context.machine_state.reset_sheet(context.sheet.sheet))

    def __str__(self):
        return f"push {self._needles} {self._push_val}"

    def __repr__(self):
        return str(self)
