"""Print Statements"""
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Comment_Line


class Print(Statement):
    """
        Prints content to python console
    """

    def __init__(self, parser_node, string: Expression):
        """
        Instantiate
        :param parser_node:
        :param string: The strint to print
        """
        super().__init__(parser_node)
        self._string: Expression = string

    def execute(self, context: Knit_Script_Context):
        """
        Prints out the given statement to console
        :param context: The current context of the knit_script_interpreter
        """
        # todo why are strings making spacing errors
        print_str = f"KS: {self._string.evaluate(context)}"
        print(print_str)
        ks_string = print_str.replace("\n", "\n;")
        context.knitout.append(Comment_Line(ks_string))

    def __str__(self):
        return f"Print({self._string})"

    def __repr__(self):
        return str(self)
