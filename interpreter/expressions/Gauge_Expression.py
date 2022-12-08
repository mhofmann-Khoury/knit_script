"""Expression for getting a sheet at a gauge"""

from interpreter.expressions.expressions import Expression
from interpreter.parser.knit_script_context import Knit_Script_Context
from knitting_machine.machine_components.Sheet_Needle import Sheet_Identifier


class Gauge_Expression(Expression):
    """
        Manages gauge expressions
    """
    def __init__(self, sheet: Expression, gauge: Expression):
        """
        Instantiate
        :param sheet: the sheet position
        :param gauge: the number of sheets
        """
        super().__init__()
        self._sheet: Expression = sheet
        self._gauge: Expression = gauge

    def evaluate(self, context: Knit_Script_Context) -> Sheet_Identifier:
        """
        Evaluate the expression
        :param context: The current context of the interpreter
        :return: the sheet identifier with these parameters
        """
        sheet = self._sheet.evaluate(context)
        gauge = self._gauge.evaluate(context)
        if sheet is None:
            sheet = context.current_sheet
        if gauge is None:
            gauge = context.current_gauge
        if sheet >= gauge:
            sheet = gauge-1
        return Sheet_Identifier(int(sheet), int(gauge))
