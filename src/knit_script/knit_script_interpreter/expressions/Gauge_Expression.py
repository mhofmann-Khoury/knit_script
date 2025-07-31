"""Expression for getting a sheet at a gauge"""
from __future__ import annotations
from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.needles.Sheet_Needle import Sheet_Identifier

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Gauge_Expression(Expression):
    """Manages gauge expressions."""

    def __init__(self, parser_node: LRStackNode, sheet: Expression, gauge: Expression) -> None:
        """Initialize the Gauge_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            sheet (Expression): The sheet position.
            gauge (Expression): The number of sheets.
        """
        super().__init__(parser_node)
        self._sheet: Expression = sheet
        self._gauge: Expression = gauge

    def evaluate(self, context: Knit_Script_Context) -> Sheet_Identifier:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Sheet_Identifier: The sheet identifier with these parameters.
        """
        sheet = self._sheet.evaluate(context)
        gauge = self._gauge.evaluate(context)
        if sheet is None:
            sheet = context.sheet
        if gauge is None:
            gauge = context.gauge
        if sheet >= gauge:
            sheet = gauge-1
        return Sheet_Identifier(int(sheet), int(gauge))
