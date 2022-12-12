"""manages blocks of code executed in a new scope"""

from typing import List

from KnitScript.knit_script_interpreter.knit_script_context import Knit_Script_Context
from KnitScript.knit_script_interpreter.statements.Statement import Statement


class Code_Block(Statement):
    """Used for executing any block of code in a new scope"""

    def __init__(self, statements: List[Statement]):
        """
        Instantiate
        :param statements: ordered list of statements to execute
        """
        super().__init__()
        self._statements: List[Statement] = statements

    def execute(self, context: Knit_Script_Context):
        """
        Enters a new scope, executes statements in order, then leaves the new scope, returning to prior scope
        :param context: The current context of the knit_script_interpreter
        """
        context.enter_sub_scope()
        had_return = False
        return_value = None
        for statement in self._statements:
            statement.execute(context)
            if context.variable_scope.has_return:  # executed statement updated scope with return value
                had_return = True
                return_value = context.variable_scope.return_value
                break  # don't continue to execute block statements
        context.exit_current_scope()
        if had_return:
            context.variable_scope.has_return = True
            context.variable_scope.return_value = return_value

    def __str__(self):
        values = ""
        for stst in self._statements:
            values += f"{stst};\n"
        values = values[:-2]
        return f"[{values}]"

    def __repr__(self):
        return str(self)