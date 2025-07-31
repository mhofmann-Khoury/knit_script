"""Basic statement structures"""
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.ks_element import KS_Element


class Statement(KS_Element):
    """Superclass for all operations that do not produce a value.

    This is the base class for all executable statements in the knit script
    language. Statements perform actions or side effects but do not return
    values (unlike expressions).
    """

    def __init__(self, parser_node: LRStackNode):
        """Initialize a statement.

        Args:
            parser_node: The parser node from the abstract syntax tree.
        """
        super().__init__(parser_node)

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the statement at the current machine context.

        This is the main method that subclasses override to implement their
        specific behavior. The base implementation does nothing.

        Args:
            context: The current execution context of the knit script interpreter.
        """
        pass


class Expression_Statement(Statement):
    """Statement that evaluates an expression without using its result.

    This statement type is used when an expression is written as a standalone
    statement. The expression is evaluated for its side effects, but the
    result is discarded.
    """

    def __init__(self, parser_node: LRStackNode, expression: Expression) -> None:
        """Initialize an expression statement.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            expression: The expression to evaluate when the statement executes.
        """
        super().__init__(parser_node)
        self._expression: Expression = expression

    @property
    def expression(self) -> Expression:
        """Get the expression contained in this statement.

        Returns:
            The expression that will be evaluated when this statement executes.
        """
        return self._expression

    def __str__(self) -> str:
        """Return string representation of the expression statement.

        Returns:
            String representation of the contained expression.
        """
        return str(self._expression)

    def __repr__(self) -> str:
        """Return detailed string representation of the expression statement.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)

    def execute(self, context: Knit_Script_Context) -> None:
        """Evaluate the expression and discard the result.

        This allows expressions with side effects (like function calls) to be
        used as statements, even though their return values are not needed.

        Args:
            context: The current execution context of the knit script interpreter.
        """
        _ = self._expression.evaluate(context)
