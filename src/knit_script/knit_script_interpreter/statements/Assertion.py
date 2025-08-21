"""Statements for asserting conditions.

This module provides the Assertion statement class, which implements Python-style assertion functionality in knit script programs.
It allows developers to test conditions during script execution and raise exceptions when those conditions are not met, providing a mechanism for runtime validation and debugging.
"""
from parglare.parser import LRStackNode

from knit_script.knit_script_exceptions.ks_exceptions import (
    Knit_Script_Assertion_Exception,
)
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Assertion(Statement):
    """Includes python style assertions in language.

    This class provides assertion functionality similar to Python's assert statement, allowing conditions to be tested during script execution with optional error messages.
    Assertions are useful for validating assumptions, checking preconditions, and debugging knit script programs by ensuring that expected conditions hold true during execution.

    When an assertion fails, it raises a Knit_Script_Assertion_Exception with detailed information about the failed condition and any provided error message,
     helping developers identify and fix issues in their knit script programs.

    Attributes:
        _condition (Expression): The condition expression to test for truthiness.
        _error_str (Expression | None): Optional error message expression to display when assertion fails.
    """

    def __init__(self, parser_node: LRStackNode, condition: Expression, error_str: Expression | None = None) -> None:
        """Initialize an Assertion statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            condition (Expression): The condition expression to test for truthiness. Will be evaluated and converted to boolean.
            error_str (Expression | None, optional): Optional error message expression to display when assertion fails. If None, a default error message will be generated. Defaults to None.
        """
        super().__init__(parser_node)
        self._error_str: Expression | None = error_str
        self._condition: Expression = condition

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the assertion by evaluating the condition.

        Evaluates the condition expression and raises an exception if the result is falsy.
        The assertion follows Python's truthiness conventions where empty collections, None, zero values, and False are considered false.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.

        Raises:
            Knit_Script_Assertion_Exception: If the condition evaluates to False or any other falsy value.
            The exception includes the original condition, the actual value that caused the failure, and any optional error message.
        """
        condition = self._condition.evaluate(context)
        if not condition:
            if self._error_str is None:
                raise Knit_Script_Assertion_Exception(self, self._condition, condition)
            else:
                raise Knit_Script_Assertion_Exception(self, self._condition, condition, self._error_str.evaluate(context))

    def __str__(self) -> str:
        """Return string representation of the assertion.

        Returns:
            str: A string showing the condition and optional error message.
        """
        return f"Assert({self._condition} -> {self._error_str})"

    def __repr__(self) -> str:
        """Return detailed string representation of the assertion.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)
