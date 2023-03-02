"""Accessor for components of the machine state"""
from typing import Optional, Union

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knitting_machine.Machine_State import Machine_State
from knit_script.knitting_machine.machine_components.Sheet_Needle import Sheet_Identifier


class Machine_Accessor(Expression):
    """Used to access machine state directly"""

    def __init__(self, parser_node):
        super().__init__(parser_node)

    def evaluate(self, context: Knit_Script_Context) -> Machine_State:
        """
        :param context:
        :return: the current machine state
        """
        return context.machine_state

    def __str__(self):
        return "machine"

    def __repr__(self):
        return str(self)


class Sheet_Expression(Expression):
    """Identifies sheets"""

    def __init__(self, parser_node, sheet_id: Union[Expression, str], gauge_id: Optional[Expression] = None):
        """
        Instantiate
        :param parser_node:
        :param sheet_id: the identifier of the sheet
        :param gauge_id: the identifier of the gauge, defaults to current gauge
        """
        super().__init__(parser_node)
        self._sheet_id: Union[Expression, str] = sheet_id
        self._gauge_id: Optional[Expression] = gauge_id

    def evaluate(self, context: Knit_Script_Context) -> Sheet_Identifier:
        """
        Evaluate the expression
        :param context: The current context of the knit_script_interpreter
        :return: Identifier for sheet at gauge
        """
        if self._gauge_id is None:
            gauge = context.gauge
        else:
            gauge = int(self._gauge_id.evaluate(context))
        if isinstance(self._sheet_id, str):
            if ":g" in self._sheet_id:
                split = self._sheet_id.find(":g")
                sheet = int(self._sheet_id[1:split])
                gauge = int(self._sheet_id[split + 2:])
            else:
                sheet = int(self._sheet_id[1:])
        else:
            sheet = int(self._sheet_id.evaluate(context))
        return Sheet_Identifier(sheet, gauge)

    def __str__(self):
        if self._gauge_id is None:
            return str(self._sheet_id)
        else:
            return f"Sheet({self._sheet_id} at g{self._gauge_id})"

    def __repr__(self):
        return str(self)
