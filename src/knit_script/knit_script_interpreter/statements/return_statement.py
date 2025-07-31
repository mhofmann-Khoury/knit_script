"""Used for storing results of function returns"""
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Return_Statement(Statement):
    """Statement that breaks out of function scope with a returned value.

    When executed, this statement evaluates an expression and sets it as the
    return value for the current function, then signals that execution should
    exit the function scope.
    """

    def __init__(self, parser_node: LRStackNode, exp: Expression) -> None:
        """Initialize a return statement.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            exp: The expression to evaluate and return as the function result.
        """
        super().__init__(parser_node)
        self._exp: Expression = exp

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the return by setting the return value and return flag.

        Evaluates the return expression and stores the result in the current
        variable scope, then sets the return flag to signal that function
        execution should terminate.

        Args:
            context: The current execution context of the knit script interpreter.
        """
        value = self._exp.evaluate(context)
        context.variable_scope.return_value = value
        context.variable_scope.has_return = True

    def __str__(self) -> str:
        """Return string representation of the return statement.

        Returns:
            A string showing the return keyword and expression.
        """
        return f"return {self._exp}"

    def __repr__(self) -> str:
        """Return detailed string representation of the return statement.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)
