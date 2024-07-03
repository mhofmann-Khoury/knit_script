"""Statements for asserting conditions"""
from knit_script.knit_script_exceptions.Knit_Script_Exception import Knit_Script_Assertion_Exception
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Assertion(Statement):
    """
        Includes python style assertions in language
    """

    def __init__(self, parser_node, condition: Expression, error_str: Expression | None = None):
        """
        Instantiate
        :param parser_node:
        :param condition: Condition to test
        :param error_str: error to report
        """
        super().__init__(parser_node)
        self._error_str: Expression | None = error_str
        self._condition: Expression = condition

    def execute(self, context: Knit_Script_Context):
        """
        Assert condition
        :param context: The current context of the knit_script_interpreter
        """
        condition = self._condition.evaluate(context)
        if not condition:
            if self._error_str is None:
                raise Knit_Script_Assertion_Exception(self._condition, condition)
            else:
                raise Knit_Script_Assertion_Exception(self._condition, condition, self._error_str.evaluate(context))

    def __str__(self):
        return f"Assert({self._condition} -> {self._error_str})"

    def __repr__(self):
        return str(self)
