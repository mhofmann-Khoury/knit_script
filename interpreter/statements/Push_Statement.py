"""Statements that change the layer position of needles"""
from typing import Union, Tuple, List

from interpreter.expressions.expressions import Expression, get_expression_value_list
from interpreter.parser.knit_pass_context import Knit_Script_Context
from interpreter.statements.Statement import Statement
from knitting_machine.machine_components.needles import Needle


class Push_Statement(Statement):
    """
        Pushes a layer to a specified position in hierarchy
    """

    def __init__(self, needles: List[Expression],
                 push_val: Union[str, Expression, Tuple[Expression, str]]):
        """
        Instantiate
        :param needles: needles to change layering
        :param push_val: direction, set to value, or direction with a given value
        """
        super().__init__()
        self.needles: List[Expression] = needles
        self.push_val: Union[str, Expression, Tuple[Expression, str]] = push_val

    def execute(self, context: Knit_Script_Context):
        """
        Pushes specified needle layers by parameters
        :param context: The current context of the interpreter
        """
        needles = get_expression_value_list(context, self.needles)
        positions = []
        for n in needles:
            if isinstance(n, Needle):
                positions.append(n.position)
            else:
                positions.append(int(n))

        for needle_pos in positions:
            if isinstance(self.push_val, Expression):
                pos = int(self.push_val.evaluate(context))
                context.machine_state.set_layer_position(needle_pos, pos)
            elif self.push_val == "Front":
                context.machine_state.set_layer_to_front(needle_pos)
            elif self.push_val == "Back":
                context.machine_state.set_layer_to_back(needle_pos)
            else:
                assert isinstance(self.push_val, tuple)
                dist = int(self.push_val[0].evaluate(context))
                direction = self.push_val[1]
                if direction == "Forward":
                    context.machine_state.push_layer_forward(needle_pos, dist)
                else:
                    context.machine_state.push_layer_backward(needle_pos, dist)
        context.knitout.extend(context.machine_state.reset_sheet(context.current_sheet.sheet))
