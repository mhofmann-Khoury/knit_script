"""Statements for asserting conditions"""
from parglare.parser import LRStackNode

from knit_script.knit_script_exceptions.ks_exceptions import Knit_Script_Assertion_Exception
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Assertion(Statement):
    """Includes python style assertions in language.

    This class provides assertion functionality similar to Python's assert statement,
    allowing conditions to be tested during script execution with optional error messages.
    """

    def __init__(self, parser_node: LRStackNode, condition: Expression, error_str: Expression | None = None) -> None:
        """Initialize an Assertion statement.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            condition: The condition expression to test for truthiness.
            error_str: Optional error message expression to display when assertion fails.
                If None, a default error message will be generated.
        """
        super().__init__(parser_node)
        self._error_str: Expression | None = error_str
        self._condition: Expression = condition

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the assertion by evaluating the condition.

        Args:
            context: The current execution context of the knit script interpreter.

        Raises:
            Knit_Script_Assertion_Exception: If the condition evaluates to False.
                Includes the condition and optional error message.
        """
        condition = self._condition.evaluate(context)
        if not condition:
            if self._error_str is None:
                raise Knit_Script_Assertion_Exception(self._condition, condition)
            else:
                raise Knit_Script_Assertion_Exception(self._condition, condition, self._error_str.evaluate(context))

    def __str__(self) -> str:
        """Return string representation of the assertion.

        Returns:
            A string showing the condition and optional error message.
        """
        return f"Assert({self._condition} -> {self._error_str})"

    def __repr__(self) -> str:
        """Return detailed string representation of the assertion.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)
