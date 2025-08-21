"""Try catch execution.

This module provides the Try_Catch_Statement class, which implements exception handling control flow in knit script programs.
It allows programs to gracefully handle errors and exceptions that may occur during knitting operations, providing robust error recovery mechanisms.
"""
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.assignment import Assignment
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Try_Catch_Statement(Statement):
    """Manages try-catch exception handling structure.

    Executes a statement within a try block, and if specified exceptions occur, executes a catch block.
    Supports filtering by specific exception types and binding caught exceptions to variables for inspection and handling.

    This statement provides robust error handling capabilities for knit script programs, allowing developers to anticipate and handle potential issues
    like machine configuration errors, invalid operations, or resource constraints.
    The try-catch mechanism ensures that programs can recover gracefully from errors rather than terminating unexpectedly.

    Attributes:
        _try_statement (Statement): The statement to execute within the try block.
        _catch_statement (Statement): The statement to execute if an exception occurs.
        _errors (list[Expression]): List of expressions that evaluate to exception types to catch.
    """

    def __init__(self, parser_node: LRStackNode, try_statement: Statement, catch_statement: Statement, errors: list[Expression]) -> None:
        """Initialize a try-catch statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            try_statement (Statement): The statement to execute within the try block.
            catch_statement (Statement): The statement to execute if a matching exception occurs.
            errors (list[Expression]): List of expressions that evaluate to exception types to catch.
            Can include Assignment expressions to bind the exception to a variable. If empty, catches all exceptions.
        """
        super().__init__(parser_node)
        self._errors: list[Expression] = errors
        self._catch_statement: Statement = catch_statement
        self._try_statement: Statement = try_statement

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the try-catch block using Python's exception handling.

        Attempts to execute the try statement. If an exception occurs and matches one of the specified error types (or if no types are specified), executes the catch statement.
        If the error expression is an Assignment, binds the exception to the specified variable name in a new scope.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
        """
        try:
            self._try_statement.execute(context)
        except Exception as e:
            if len(self._errors) > 0:
                for error_exp in self._errors:
                    if isinstance(error_exp, Assignment):
                        error = error_exp.value(context)
                    else:
                        error = error_exp.evaluate(context)
                    if isinstance(e, error):
                        context.enter_sub_scope()
                        if isinstance(error_exp, Assignment):
                            context.variable_scope[error_exp.variable_name] = e
                        self._catch_statement.execute(context)
                        context.exit_current_scope(collapse_into_parent=True)  # Anything done during the except should affect external scope
                        break
            else:  # accept all errors
                self._catch_statement.execute(context)

    def __str__(self) -> str:
        """Return string representation of the try-catch statement.

        Returns:
            str: A string showing the try statement, error types, and catch statement.
        """
        return f"Try({self._try_statement})->Catch({self._errors} then {self._catch_statement})"

    def __repr__(self) -> str:
        """Return detailed string representation of the try-catch statement.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)
