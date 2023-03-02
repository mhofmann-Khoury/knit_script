"""Manages branching condition statements"""
from typing import Optional

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class If_Statement(Statement):
    """
        conditional if else branch structure
    """

    def __init__(self, parser_node, condition: Expression, true_statement: Statement, false_statement: Optional[Statement] = None):
        """
        Instantiate
        :param parser_node:
        :param condition: branching condition
        :param true_statement: statement to execute on true
        :param false_statement: statement to execute on false
        """
        super().__init__(parser_node)
        self._condition: Expression = condition
        self._true_statement: Statement = true_statement
        self._false_statement: Optional[Statement] = false_statement

    def execute(self, context: Knit_Script_Context):
        """
        Executes correct branch based on condition result
        :param context:  The current context of the knit_script_interpreter
        """
        condition = self._condition.evaluate(context)
        if condition:
            self._true_statement.execute(context)
        elif self._false_statement is not None:
            self._false_statement.execute(context)

    def __str__(self):
        return f"If({self._condition})->{self._true_statement} else->{self._false_statement}"

    def __repr__(self):
        return str(self)
