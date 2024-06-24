"""Statement for declaring a variable"""
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knit_script_interpreter.statements.assignment import Assignment


class Variable_Declaration(Statement):
    """
        Used to set a variable value at current scope
    """

    def __init__(self, parser_node, assignment: Assignment, is_global: bool = False):
        """
        Instantiate
        :param parser_node:
        :param assignment: Assignment to make on execution
        """
        super().__init__(parser_node)
        self._is_global = is_global
        self._assignment: Assignment = assignment

    def execute(self, context: Knit_Script_Context):
        """
        Evaluates the expression at current context and puts result into variable scope
        :param context: The current context of the knit_script_interpreter
        """
        self._assignment.assign_value(context, is_global=self._is_global)

    def __str__(self):
        return f"{self._assignment};"

    def __repr__(self):
        return str(self)
