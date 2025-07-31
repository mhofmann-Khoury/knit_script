"""Print Statements"""
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Comment_Line
from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Print(Statement):
    """Prints content to Python console and knitout comments.

    Evaluates an expression and prints the result both to the Python console
    (prefixed with "KS:") and as a comment line in the generated knitout.
    """

    def __init__(self, parser_node: LRStackNode, string: Expression) -> None:
        """Initialize a print statement.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            string: The expression to evaluate and print.
        """
        super().__init__(parser_node)
        self._string: Expression = string

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the print by evaluating and outputting the expression.

        Evaluates the string expression, prints it to the console with "KS:" prefix,
        and adds it as a comment to the knitout with proper line break handling.

        Args:
            context: The current execution context of the knit script interpreter.
        """
        print_str = f"KS: {self._string.evaluate(context)}"
        print(print_str)
        ks_string = print_str.replace("\n", "\n;")
        context.knitout.append(Knitout_Comment_Line(ks_string))

    def __str__(self) -> str:
        """Return string representation of the print statement.

        Returns:
            A string showing the expression to be printed.
        """
        return f"Print({self._string})"

    def __repr__(self) -> str:
        """Return detailed string representation of the print statement.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)
