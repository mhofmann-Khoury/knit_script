"""Components for managing headers"""

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.values import Header_ID_Value
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Header_Statement(Statement):
    """
        Header statements update variables of the machine state and knitout
    """

    def __init__(self, parser_node, type_id: Header_ID_Value, value: Expression):
        super().__init__(parser_node)
        self._value: Expression = value
        self._type_id: Header_ID_Value = type_id

    def execute(self, context: Knit_Script_Context):
        """
        Set the header value and update machine state
        :param context: context to get header and machine state from
        """
        value = self._value.evaluate(context)
        type_id = self._type_id.evaluate(context)
        context.header.set_value(type_id, value)
        context.machine_state = context.header.machine_state()
