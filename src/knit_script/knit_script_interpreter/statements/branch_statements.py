"""Manages branching condition statements.

This module provides the If_Statement class, which implements conditional execution control flow in knit script programs.
It allows programs to execute different code paths based on boolean condition evaluation, supporting the fundamental control flow needed for complex knitting logic.
"""
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class If_Statement(Statement):
    """Conditional if-else branch structure.

    Implements conditional execution where one of two statement branches is executed based on the evaluation of a boolean condition.
    The If_Statement class provides the fundamental branching control flow for knit script programs, allowing different knitting operations to be performed based on runtime conditions.

    This statement supports both simple if statements and if-else structures, with the else branch being optional.
    The condition is evaluated using Python's truthiness conventions, where empty collections, None, zero values, and False are considered falsy.

    Attributes:
        _condition (Expression): The boolean expression that determines which branch to execute.
        _true_statement (Statement): The statement to execute when the condition is True.
        _false_statement (Statement | None): The statement to execute when the condition is False.
    """

    def __init__(self, parser_node: LRStackNode, condition: Expression, true_statement: Statement, false_statement: Statement | None = None) -> None:
        """Initialize an if-else statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            condition (Expression): The boolean expression that determines which branch to execute. Will be evaluated and converted to boolean using Python truthiness rules.
            true_statement (Statement): The statement to execute when the condition evaluates to a truthy value.
            false_statement (Statement | None, optional): The statement to execute when the condition evaluates to a falsy value.
             If None, no action is taken when the condition is False. Defaults to None.
        """
        super().__init__(parser_node)
        self._condition: Expression = condition
        self._true_statement: Statement = true_statement
        self._false_statement: Statement | None = false_statement

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the appropriate branch based on the condition result.

        Evaluates the condition expression and executes either the true statement or false statement based on the result. The condition evaluation follows Python's truthiness conventions.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
        """
        condition = self._condition.evaluate(context)
        if condition:
            self._true_statement.execute(context)
        elif self._false_statement is not None:
            self._false_statement.execute(context)

    def __str__(self) -> str:
        """Return string representation of the if statement.

        Returns:
            str: A string showing the condition and both statement branches.
        """
        return f"If({self._condition})->{self._true_statement} else->{self._false_statement}"

    def __repr__(self) -> str:
        """Return detailed string representation of the if statement.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)
