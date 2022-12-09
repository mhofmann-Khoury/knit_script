"""Basic statement structures"""

from KnitScript.knit_script_interpreter.expressions.expressions import Expression
from KnitScript.knit_script_interpreter.knit_script_context import Knit_Script_Context


class Statement:
    """
        Super class for all operations that do not produce a value
    """

    def __init__(self):
        pass

    def execute(self, context: Knit_Script_Context):
        """
        Executes the instruction at the current machine context
        :param context:
        """
        pass


class Expression_Statement(Statement):
    """
        Statement with no effect on program state but creates and does not use an expression
    """
    def __init__(self, expression: Expression):
        """
        Instantiate
        :param expression: expression being read in statement
        """
        super().__init__()
        self._expression: Expression = expression

    @property
    def expression(self) -> Expression:
        """
        :return: expression in the statement
        """
        return self._expression

    def __str__(self):
        return str(self._expression)

    def __repr__(self):
        return str(self)

    def execute(self, context: Knit_Script_Context):
        """
        Evaluates but doesn't do anything with expression. Implies indirection actions
        :param context: The current context of the knit_script_interpreter
        """
        _ = self._expression.evaluate(context)
