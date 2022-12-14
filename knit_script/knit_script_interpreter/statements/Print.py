"""Print Statements"""
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Print(Statement):
    """
        Prints content to python console
    """

    def __init__(self, string: Expression):
        """
        Instantiate
        :param string: the strint to print
        """
        super().__init__()
        self._string: Expression = string

    def execute(self, context: Knit_Script_Context):
        """
        Prints out given statement to console
        :param context: The current context of the knit_script_interpreter
        """
        print_str = f"KP Printout: {self._string.evaluate(context)}"
        print(print_str)
        context.knitout.append(f";{print_str}\n")

    def __str__(self):
        return f"Print({self._string})"

    def __repr__(self):
        return str(self)
