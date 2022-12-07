"""Manages branching condition statements"""
from typing import Optional

from interpreter.expressions.expressions import Expression
from interpreter.parser.knit_pass_context import Knit_Script_Context
from interpreter.statements.Statement import Statement


class If_Statement(Statement):
    """
        conditional if else branch structure
    """

    def __init__(self, condition: Expression, true_statement: Statement,
                 false_statement: Optional[Statement] = None):
        """
        Instantiate
        :param condition: branching condition
        :param true_statement: statement to execute on true
        :param false_statement: statement to execute on false
        """
        super().__init__()
        self._condition: Expression = condition
        self._true_statement: Statement = true_statement
        self._false_statement: Optional[Statement] = false_statement

    def execute(self, context: Knit_Script_Context):
        """
        Executes correct branch based on condition result
        :param context:  The current context of the interpreter
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
