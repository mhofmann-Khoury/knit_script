"""Try catch execution"""
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Try_Catch_Statement(Statement):
    """
        manage try catch structure
    """

    def __init__(self, try_statement: Statement, catch_statement: Statement):
        """
        Instantiate
        :param try_statement: statement to try to execute
        :param catch_statement: statement to execute on failure
        """
        super().__init__()
        self._catch_statement = catch_statement
        self._try_statement = try_statement

    def execute(self, context: Knit_Script_Context):
        """
        Execute try-catch using python structure
        :param context: The current context of the knit_script_interpreter
        """
        try:
            self._try_statement.execute(context)
        except AssertionError:
            self._catch_statement.execute(context)

    def __str__(self):
        return f"Try({self._try_statement})->Catch({self._catch_statement})"

    def __repr__(self):
        return str(self)
