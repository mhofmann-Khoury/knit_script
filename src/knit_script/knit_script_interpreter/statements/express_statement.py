"""Module containing the Expression_Statement class"""

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Expression_Statement(Statement):
    """Statement that evaluates an expression without using its result.

    This statement type is used when an expression is written as a standalone statement. The expression is evaluated for its side effects, but the result is discarded.
    This is common for function calls that are executed for their actions rather than their return values.

    Expression statements bridge the gap between expressions and statements, allowing any expression to be used as a statement by simply discarding its return value.
    This enables the use of function calls, assignments, and other expressions as standalone operations.

    """

    def __init__(self, parser_node: LRStackNode, expression: Expression) -> None:
        """Initialize an expression statement.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            expression (Expression): The expression to evaluate when the statement executes.
        """
        super().__init__(parser_node)
        self._expression: Expression = expression

    @property
    def expression(self) -> Expression:
        """Get the expression contained in this statement.

        Returns:
            Expression: The expression that will be evaluated when this statement executes.
        """
        return self._expression

    def execute(self, context: Knit_Script_Context) -> None:
        """Evaluate the expression and discard the result.

        This allows expressions with side effects (like function calls) to be used as statements, even though their return values are not needed.
         The expression is evaluated in the current context but the result is ignored.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
        """
        _ = self._expression.evaluate(context)
