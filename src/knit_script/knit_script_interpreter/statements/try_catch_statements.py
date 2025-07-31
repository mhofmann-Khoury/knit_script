"""Try catch execution"""
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knit_script_interpreter.statements.assignment import Assignment


class Try_Catch_Statement(Statement):
    """Manages try-catch exception handling structure.

    Executes a statement within a try block, and if specified exceptions occur,
    executes a catch block. Supports filtering by specific exception types and
    binding caught exceptions to variables.
    """

    def __init__(self, parser_node: LRStackNode, try_statement: Statement, catch_statement: Statement, errors: list[Expression]) -> None:
        """Initialize a try-catch statement.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            try_statement: The statement to execute within the try block.
            catch_statement: The statement to execute if an exception occurs.
            errors: List of expressions that evaluate to exception types to catch.
                Can include Assignment expressions to bind the exception to a variable.
                If empty, catches all exceptions.
        """
        super().__init__(parser_node)
        self._errors: list[Expression] = errors
        self._catch_statement: Statement = catch_statement
        self._try_statement: Statement = try_statement

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the try-catch block using Python's exception handling.

        Attempts to execute the try statement. If an exception occurs and matches
        one of the specified error types (or if no types are specified), executes
        the catch statement. If the error expression is an Assignment, binds the
        exception to the specified variable name.

        Args:
            context: The current execution context of the knit script interpreter.
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
                        context.exit_current_scope()
                        break
            else:  # accept all errors
                self._catch_statement.execute(context)

    def __str__(self) -> str:
        """Return string representation of the try-catch statement.

        Returns:
            A string showing the try statement, error types, and catch statement.
        """
        return f"Try({self._try_statement})->Catch({self._errors} then {self._catch_statement})"

    def __repr__(self) -> str:
        """Return detailed string representation of the try-catch statement.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)
