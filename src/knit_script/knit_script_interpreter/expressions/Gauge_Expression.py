"""Expression for getting a sheet at a gauge.

This module provides the Gauge_Expression class, which handles the creation of sheet identifiers with specific gauge configurations.
It allows knit script programs to specify sheet and gauge combinations for multi-sheet knitting operations.
"""
from __future__ import annotations

from parglare.parser import LRStackNode
from virtual_knitting_machine.machine_components.needles.Sheet_Identifier import (
    Sheet_Identifier,
)

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Gauge_Expression(Expression):
    """Manages gauge expressions.

    The Gauge_Expression class handles the creation of Sheet_Identifier objects with specified sheet and gauge values.
    It provides a way to explicitly specify both the sheet number and gauge configuration, with automatic bounds checking and fallback to context values when needed.

    This expression type is essential for multi-sheet knitting operations where different sheets need to be referenced with specific gauge configurations.
    It ensures that sheet numbers are valid for the specified gauge and provides sensible defaults from the execution context.

    Attributes:
        _sheet (Expression): The expression that evaluates to the sheet position.
        _gauge (Expression): The expression that evaluates to the number of sheets (gauge).
    """

    def __init__(self, parser_node: LRStackNode, sheet: Expression, gauge: Expression) -> None:
        """Initialize the Gauge_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            sheet (Expression): The expression that evaluates to the sheet position.
            gauge (Expression): The expression that evaluates to the number of sheets in the gauge configuration.
        """
        super().__init__(parser_node)
        self._sheet: Expression = sheet
        self._gauge: Expression = gauge

    def evaluate(self, context: Knit_Script_Context) -> Sheet_Identifier:
        """Evaluate the expression to create a sheet identifier.

        Evaluates the sheet and gauge expressions and creates a Sheet_Identifier with the resulting values.
        Provides fallback to context values when expressions evaluate to None and performs bounds checking to ensure the sheet number is valid for the gauge.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Sheet_Identifier: The sheet identifier with the specified sheet and gauge parameters.

        Note:
            If the sheet number is greater than or equal to the gauge, it will be automatically adjusted to gauge-1 to ensure validity.
        """
        sheet = self._sheet.evaluate(context)
        gauge = self._gauge.evaluate(context)
        if sheet is None:
            sheet = context.sheet
        if gauge is None:
            gauge = context.gauge
        if sheet >= gauge:
            sheet = gauge - 1
        return Sheet_Identifier(int(sheet), int(gauge))
