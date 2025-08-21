"""Used for storing results of function returns.

This module provides the Return_Statement class, which handles function return operations in knit script programs.
It evaluates return expressions and manages the return value propagation through the scope hierarchy.
"""
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Return_Statement(Statement):
    """Statement that breaks out of function scope with a returned value.

    When executed, this statement evaluates an expression and sets it as the return value for the current function, then signals that execution should exit the function scope.
    The return statement provides the mechanism for functions to produce results and terminate execution early.

    The return value is propagated through the scope hierarchy to reach the appropriate function scope,
    and execution of the current function terminates immediately after the return statement is processed.

    Attributes:
        _exp (Expression): The expression to evaluate and return as the function result.
    """

    def __init__(self, parser_node: LRStackNode, exp: Expression) -> None:
        """Initialize a return statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            exp (Expression): The expression to evaluate and return as the function result.
        """
        super().__init__(parser_node)
        self._exp: Expression = exp

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the return by setting the return value and return flag.

        Evaluates the return expression and stores the result in the current variable scope, then sets the return flag to signal that function execution should terminate immediately.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
        """
        value = self._exp.evaluate(context)
        context.variable_scope.return_value = value

    def __str__(self) -> str:
        """Return string representation of the return statement.

        Returns:
            str: A string showing the return keyword and expression.
        """
        return f"return {self._exp}"

    def __repr__(self) -> str:
        """Return detailed string representation of the return statement.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)
