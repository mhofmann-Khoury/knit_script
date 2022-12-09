"""Expressions associated with functions"""
from typing import List, Optional, Any

from interpreter.expressions.expressions import Expression
from interpreter.expressions.variables import Variable_Expression
from interpreter.parser.knit_script_context import Knit_Script_Context
from interpreter.statements.assignment import Assignment
from interpreter.statements.function_dec_statement import Function_Signature


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

    def __init__(self, func_name: Variable_Expression, args: List[Expression],
                 kwargs: List[Assignment]):
        """
        Instantiate
        :param func_name: name of the function
        :param args: the list of argument expressions to fill in
        :param kwargs: the list of assignments to fill in by keywords
        """
        super().__init__()
        self.kwargs: List[Assignment] = kwargs
        self.args: List[Expression] = args
        self.func_name: Variable_Expression = func_name

    def evaluate(self, context: Knit_Script_Context) -> Optional[Any]:
        """
        Finds function in scope, fills parameters and then executes
        :param context: The current context of the interpreter
        :return: Return value set at function scope before closing
        """
        if self.func_name.variable_name in context.variable_scope:
            function_signature = context.variable_scope[self.func_name.variable_name]
            assert isinstance(function_signature, Function_Signature), \
                f"{self.func_name.variable_name} is non-callable value {function_signature}"
            return_value = function_signature.execute(context, self.args, self.kwargs)
            return return_value
        else:
            try:
                args_str = ""
                args = []
                for arg_exp in self.args:
                    arg = arg_exp.evaluate(context)
                    args_str += f"{arg}, "
                    args.append(arg)
                kwargs = {}
                for kwarg_assign in self.kwargs:
                    kwarg_value = kwarg_assign.value(context)
                    args_str += f"{kwarg_assign.variable_name} = {kwarg_value}, "
                    kwargs[kwarg_assign.variable_name] = kwarg_value
                args_str = args_str[:-2]  # remove last ", "
                func_str = f"{self.func_name.variable_name}({args_str})"
                func_str = f"{self.func_name.variable_name}(*args, **kwargs)"
                return eval(func_str)
            except NameError as error:
                raise RuntimeError(f"KnitPass: Could not find function by name {self.func_name.variable_name}") from error

    def __str__(self):
        values = ""
        for exp in self.args:
            values += f"{exp}, "
        for assign in self.kwargs:
            values += f"{assign}, "
        values = values[:-2]
        return f"{self.func_name.variable_name}({values})"
