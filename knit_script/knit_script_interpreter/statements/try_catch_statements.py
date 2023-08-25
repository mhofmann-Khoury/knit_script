"""Try catch execution"""
from typing import List

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knit_script_interpreter.statements.assignment import Assignment


class Try_Catch_Statement(Statement):
    """
        manage try catch structure
    """

    def __init__(self, parser_node, try_statement: Statement, catch_statement: Statement, errors: List[Expression]):
        """
        Instantiate
        :param parser_node:
        :param try_statement: Statement to try to execute.
        :param catch_statement: Statement to execute on failure
        """
        super().__init__(parser_node)
        self._errors = errors
        self._catch_statement = catch_statement
        self._try_statement = try_statement

    def execute(self, context: Knit_Script_Context):
        """
        Execute try-catch using python structure
        :param context: The current context of the knit_script_interpreter
        """
        try:
            self._try_statement.execute(context)
        except Exception as e:
            if len(self._errors) > 0:
                for error_exp in self._errors:
                    if isinstance(error_exp, Assignment):
                        error = error_exp.value(context)
                    else:
                        error = error_exp.evaluate(context)
                    if isinstance(e, error):
                        context.enter_sub_scope()
                        if isinstance(error_exp, Assignment):
                            context.variable_scope[error_exp.variable_name] = e
                        self._catch_statement.execute(context)
                        context.exit_current_scope()
                        break
            else:  # accept all errors
                self._catch_statement.execute(context)

    def __str__(self):
        return f"Try({self._try_statement})->Catch({self._errors} then {self._catch_statement})"

    def __repr__(self):
        return str(self)
