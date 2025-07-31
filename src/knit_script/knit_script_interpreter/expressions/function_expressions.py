"""Expressions associated with functions"""
from typing import Any

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.assignment import Assignment
from knit_script.knit_script_interpreter.statements.function_dec_statement import Function_Signature


class Function_Call(Expression):
    """A call to a function which must return a value or result in None.

    Attributes:
        kwargs (list[Assignment]): The list of assignments used to set keyword arguments.
        args (list[Expression]): The list of expressions to fill in arguments.
        func_name (Variable_Expression): The name of the function to call.
    """

    def __init__(self, parser_node: LRStackNode, func_name: Variable_Expression, args: list[Expression], kwargs: list[Assignment]) -> None:
        """Initialize the Function_Call.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            func_name (Variable_Expression): Name of the function.
            args (list[Expression]): The list of argument expressions to fill in.
            kwargs (list[Assignment]): The list of assignments to fill in by keywords.
        """
        super().__init__(parser_node)
        self.kwargs: list[Assignment] = kwargs
        self.args: list[Expression] = args
        self.func_name: Variable_Expression = func_name

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """Find function in scope, fill parameters and then execute.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Any: Return value set at function scope before closing.
        """
        if self.func_name.variable_name in context.variable_scope:
            function_signature = context.variable_scope[self.func_name.variable_name]
            if isinstance(function_signature, Function_Signature):
                return_value = function_signature.execute(context, self.args, self.kwargs)
                return return_value
            else:
                args = [arg.evaluate(context) for arg in self.args]
                kwargs = {kwarg.variable_name: kwarg.value(context) for kwarg in self.kwargs}
                # if isinstance(function_signature, Callable):
                if callable(function_signature):
                    return function_signature(*args, **kwargs)
                else:
                    func_str = f"{self.func_name.variable_name}(*args, **kwargs)"
                    return eval(func_str)
        else:
            raise NameError(f"name {self.func_name.variable_name} is not defined.")  # Todo add way of tracking line numbers from statements and expressions

    def __str__(self) -> str:
        values = ""
        for exp in self.args:
            values += f"{exp}, "
        for assign in self.kwargs:
            values += f"{assign}, "
        values = values[:-2]
        return f"{self.func_name.variable_name}({values})"
