"""Loop control structures"""
from collections.abc import Iterable
from typing import List, Union, Optional

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.Statement import Statement


class While_Statement(Statement):
    """
        While loop execution structure
    """

    def __init__(self, parser_node, condition: Expression, statement: Statement):
        """
        Instantiate
        :param parser_node:
        :param condition: condition to evaluate on while
        :param statement: the statement to execute with each iteration
        """
        super().__init__(parser_node)
        self._condition: Expression = condition
        self._statement: Statement = statement

    def execute(self, context: Knit_Script_Context):
        """
        Executes the Statement
        :param context: The current context of the knit_script_interpreter
        """
        condition = self._condition.evaluate(context)
        while condition:
            self._statement.execute(context)
            condition = self._condition.evaluate(context)

    def __str__(self):
        return f"While({self._condition} -> {self._statement})"

    def __repr__(self):
        return str(self)


class For_Each_Statement(Statement):
    """
        Statements that give access to iterable variable over an iterable element (lists)
    """

    def __init__(self, parser_node, variables: List[Variable_Expression], iter_expression: Union[Expression, List[Expression]], statement: Statement):
        """
        Instantiate
        :param parser_node:
        :param variables: to assign on each iteration of iterable.
        :param iter_expression: iterable to iterate over
        :param statement: statement to execute with each iteration
        """
        super().__init__(parser_node)
        self._variables: List[Variable_Expression] = variables
        if len(self._variables) == 1:
            self.var_name: Optional[str] = self._variables[0].variable_name
        else:
            self.var_name: Optional[str] = None  # todo var name may be able to be removed
        self._iter_expression: Union[Expression, List[Expression]] = iter_expression
        self._statement = statement

    def execute(self, context: Knit_Script_Context):
        """
        Execute iteration over iterable express with local scope
        :param context:  The current context of the knit_script_interpreter
        """
        iterable = self._iter_expression.evaluate(context)
        assert isinstance(iterable, Iterable), f'Cannot iterate over non-iterable value {iterable}'
        context.enter_sub_scope()  # create new scope that holds iterator variable
        for var in iterable:
            if self.var_name is not None:
                context.variable_scope[self.var_name] = var  # update iterator variable in scope
            else:  # multiple vars to unpack
                iterated_var = [*var]
                assert len(iterated_var) == len(self._variables), "Unpacked values do not match variables provided"
                for var_name, var_val in zip(self._variables, iterated_var):
                    context.variable_scope[var_name.variable_name] = var_val

            self._statement.execute(context)
        context.exit_current_scope()  # exit scope, removing access to iterator variable

    def __str__(self):
        return f"for {self.var_name} in {self._iter_expression} -> {self._statement}"

    def __repr__(self):
        return str(self)
