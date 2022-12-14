"""Statement for declaring a variable"""
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knit_script_interpreter.statements.assignment import Assignment


class Variable_Declaration(Statement):
    """
        Used to set a variable value at current scope
    """

    def __init__(self, assignment: Assignment):
        """
        Instantiate
        :param assignment: assignment to make on execution
        """
        super().__init__()
        self._assignment:Assignment = assignment

    def execute(self, context: Knit_Script_Context):
        """
        Evaluates the expression at current context and puts result into variable scope
        :param context: The current context of the knit_script_interpreter
        """
        self._assignment.assign_value(context)

    def __str__(self):
        return f"{self._assignment};"

    def __repr__(self):
        return str(self)
