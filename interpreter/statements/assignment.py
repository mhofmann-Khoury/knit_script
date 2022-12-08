"""Assignment structure"""
from typing import Any

from interpreter.expressions.expressions import Expression
from interpreter.parser.knit_script_context import Knit_Script_Context
from knitting_machine.machine_components.Sheet_Needle import Sheet_Identifier


class Assignment:
    """
        Class for managing assignment expressions
    """

    def __init__(self, var_name: str, var_expression: Expression):
        """
        Instantiate
        :param var_name: name of variable
        :param var_expression: value to assign
        """
        super().__init__()
        self._var_expression: Expression = var_expression
        self._variable_name: str = var_name

    @property
    def variable_name(self) -> str:
        """
        :return: Name of variable being assigned
        """
        return self._variable_name
    def assign_value(self, context: Knit_Script_Context) -> Any:
        """
        Assign the value to the variable
        :param context:  The current context of the interpreter
        :return: result of assignment expression
        """
        value = self.value(context)
        if self.variable_name == "Carrier":
            context.current_carrier = value  # manages in and inhook operations
        elif self.variable_name == "Racking":
            context.current_racking = value  # writes appropriate knitout in setter
        elif self.variable_name == "Sheet":
            if isinstance(value, Sheet_Identifier):
                context.current_gauge = value.gauge
                context.current_sheet = value.sheet
            elif value is None:
                context.current_sheet = value
            else:
                context.current_sheet = int(value)
        elif self.variable_name == "Gauge":
            context.current_gauge = value
            if context.current_sheet.sheet >= context.current_gauge:
                context.current_sheet = context.current_gauge - 1  # set to back sheet if gauge was past sheet
        else:  # Non-built in variables
            context.variable_scope[self.variable_name] = value
        return value

    def value(self, context) -> Any:
        """
        Get the value to be assigned
        :param context: the current context to evaluate value at
        :return: Value that is being assigned to variable
        """
        expression_result = self._var_expression.evaluate(context)
        return expression_result

    def __str__(self):
        return f"Assign({self.variable_name} <- {self._var_expression})"

    def __repr__(self):
        return str(self)
