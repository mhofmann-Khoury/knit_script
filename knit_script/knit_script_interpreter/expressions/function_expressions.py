"""Expressions associated with functions"""
from typing import List, Optional, Any, Callable

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.assignment import Assignment
from knit_script.knit_script_interpreter.statements.function_dec_statement import Function_Signature


class Function_Call(Expression):
    """
        A call to a function which must return a value or result in None
    ...

    Attributes
    ----------
    kwargs: List[Assignment]
        The list of assignments used to set keyword arguments
    args: List[Expression]
        The list of expressions to fill in arguments
    func_name: Expression
        The name of the function to call
    """

    def __init__(self, parser_node, func_name: Variable_Expression, args: List[Expression], kwargs: List[Assignment]):
        """
        Instantiate
        :param parser_node:
        :param func_name: Name of the function
        :param args: the list of argument expressions to fill in
        :param kwargs: the list of assignments to fill in by keywords
        """
        super().__init__(parser_node)
        self.kwargs: List[Assignment] = kwargs
        self.args: List[Expression] = args
        self.func_name: Variable_Expression = func_name

    def evaluate(self, context: Knit_Script_Context) -> Optional[Any]:
        """
        Finds function in scope, fills parameters and then executes
        :param context: The current context of the knit_script_interpreter
        :return: Return value set at function scope before closing
        """
        if self.func_name.variable_name in context.variable_scope:
            function_signature = context.variable_scope[self.func_name.variable_name]
            if isinstance(function_signature, Function_Signature):
                return_value = function_signature.execute(context, self.args, self.kwargs)
                return return_value
            else:
                args = [arg.evaluate(context) for arg in self.args]
                kwargs = {kwarg.variable_name: kwarg.value(context) for kwarg in self.kwargs}
                if isinstance(function_signature, Callable):
                    return function_signature(*args, **kwargs)
                else:
                    func_str = f"{self.func_name.variable_name}(*args, **kwargs)"
                    return eval(func_str)
        else:
            raise NameError(f"name {self.func_name.variable_name} is not defined.")  # Todo add way of tracking line numbers from statements and expressions

    def __str__(self):
        values = ""
        for exp in self.args:
            values += f"{exp}, "
        for assign in self.kwargs:
            values += f"{assign}, "
        values = values[:-2]
        return f"{self.func_name.variable_name}({values})"
