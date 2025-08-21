"""Accessor for components of the machine state.

This module provides expression classes for accessing machine state and sheet components in knit script programs.
It includes the Machine_Accessor for direct machine access and Sheet_Expression for referencing specific sheets with gauge configurations.
"""
from parglare.parser import LRStackNode
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.needles.Sheet_Identifier import (
    Sheet_Identifier,
)

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Machine_Accessor(Expression):
    """Used to access machine state directly.

    The Machine_Accessor class provides direct access to the knitting machine state from knit script expressions.
    It serves as the bridge between knit script code and the underlying machine state, allowing scripts to access machine properties and needle collections.

    This accessor is typically used with attribute access operations to get specific machine components like needle sets, carrier systems, or machine configuration parameters.
    """

    def __init__(self, parser_node: LRStackNode) -> None:
        """Initialize the Machine_Accessor.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
        """
        super().__init__(parser_node)

    def evaluate(self, context: Knit_Script_Context) -> Knitting_Machine:
        """Evaluate the expression to get the machine state.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Knitting_Machine: The current machine state from the execution context.
        """
        return context.machine_state

    def __str__(self) -> str:
        return "machine"

    def __repr__(self) -> str:
        return str(self)


class Sheet_Expression(Expression):
    """Identifies sheets.

    The Sheet_Expression class handles the creation and evaluation of sheet identifiers in knit script programs.
    It supports both simple sheet references and complex sheet specifications with custom gauge values, parsing sheet identifier strings and creating appropriate Sheet_Identifier objects.

    This expression type is essential for multi-sheet knitting operations where specific sheets need to be referenced with their gauge configurations.
    It handles various sheet identifier formats including embedded gauge specifications.

    Attributes:
        _sheet_id (Expression | str): The identifier of the sheet, either as an expression or string.
        _gauge_id (Expression | None): Optional gauge identifier expression.
    """

    def __init__(self, parser_node: LRStackNode, sheet_id: Expression | str, gauge_id: Expression | None = None) -> None:
        """Initialize the Sheet_Expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            sheet_id (Expression | str): The identifier of the sheet, which can be a string with embedded gauge information or an expression.
            gauge_id (Expression | None, optional): The identifier of the gauge, defaults to current gauge if not specified. Defaults to None.
        """
        super().__init__(parser_node)
        self._sheet_id: Expression | str = sheet_id
        self._gauge_id: Expression | None = gauge_id

    def evaluate(self, context: Knit_Script_Context) -> Sheet_Identifier:
        """Evaluate the expression to create a sheet identifier.

        Processes the sheet identifier, extracting gauge information if embedded in the string format, and creates a Sheet_Identifier with the appropriate sheet and gauge values.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Sheet_Identifier: Identifier for the sheet at the specified or current gauge.

        Note:
            String sheet identifiers can include embedded gauge information in the format "s<sheet>:g<gauge>" where <sheet> and <gauge> are numeric values.
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

    def __str__(self) -> str:
        if self._gauge_id is None:
            return str(self._sheet_id)
        else:
            return f"Sheet({self._sheet_id} at g{self._gauge_id})"

    def __repr__(self) -> str:
        return str(self)
