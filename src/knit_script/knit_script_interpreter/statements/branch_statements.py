"""Manages branching condition statements"""
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class If_Statement(Statement):
    """Conditional if-else branch structure.

    Implements conditional execution where one of two statement branches
    is executed based on the evaluation of a boolean condition.
    """

    def __init__(self, parser_node: LRStackNode, condition: Expression, true_statement: Statement, false_statement: Statement | None = None) -> None:
        """Initialize an if-else statement.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            condition: The boolean expression that determines which branch to execute.
            true_statement: The statement to execute when the condition is True.
            false_statement: The statement to execute when the condition is False.
                If None, no action is taken when the condition is False.
        """
        super().__init__(parser_node)
        self._condition: Expression = condition
        self._true_statement: Statement = true_statement
        self._false_statement: Statement | None = false_statement

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the appropriate branch based on the condition result.

        Args:
            context: The current execution context of the knit script interpreter.
        """
        condition = self._condition.evaluate(context)
        if condition:
            self._true_statement.execute(context)
        elif self._false_statement is not None:
            self._false_statement.execute(context)

    def __str__(self) -> str:
        """Return string representation of the if statement.

        Returns:
            A string showing the condition and both statement branches.
        """
        return f"If({self._condition})->{self._true_statement} else->{self._false_statement}"

    def __repr__(self) -> str:
        """Return detailed string representation of the if statement.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)
