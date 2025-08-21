"""Expressions associated with functions.

This module provides the Function_Call class, which handles function call expressions in knit script programs.
It supports both knit script user-defined functions and Python callable objects, with parameter passing through positional and keyword arguments.
"""
from typing import Any

from parglare.parser import LRStackNode

from knit_script.knit_script_exceptions.python_style_exceptions import (
    Knit_Script_NameError,
)
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.variables import (
    Variable_Expression,
)
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.statements.assignment import Assignment
from knit_script.knit_script_interpreter.statements.function_dec_statement import (
    Function_Signature,
)


class Function_Call(Expression):
    """A call to a function which must return a value or result in None.

    The Function_Call class handles the execution of function calls in knit script programs.
    It supports both user-defined knit script functions (represented by Function_Signature objects) and Python callable objects.
    The class manages parameter passing through both positional arguments and keyword arguments, evaluating them in the current context before passing them to the target function.

    This class provides the bridge between knit script function call syntax and the underlying function execution mechanisms,
    whether they are knit script functions with their own scopes or Python functions integrated into the knit script environment.

    Attributes:
        kwargs (list[Assignment]): The list of assignments used to set keyword arguments.
        args (list[Expression]): The list of expressions to fill in positional arguments.
        func_name (Variable_Expression): The name of the function to call.
    """

    def __init__(self, parser_node: LRStackNode, func_name: Variable_Expression, args: list[Expression], kwargs: list[Assignment]) -> None:
        """Initialize the Function_Call.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            func_name (Variable_Expression): Name of the function to call.
            args (list[Expression]): The list of argument expressions to evaluate and pass as positional parameters.
            kwargs (list[Assignment]): The list of assignments to evaluate and pass as keyword parameters.
        """
        super().__init__(parser_node)
        self.kwargs: list[Assignment] = kwargs
        self.args: list[Expression] = args
        self.func_name: Variable_Expression = func_name

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """Find function in scope, fill parameters and then execute.

        Locates the function in the current variable scope, evaluates all arguments, and executes the function with the provided parameters.
         Handles both knit script functions and Python callable objects.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Any: Return value set at function scope before closing, or the result of the Python function call.

        Raises:
            NameError: If the function name is not defined in the current scope.
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
            raise Knit_Script_NameError(f"name {self.func_name.variable_name} is not defined.", self)

    def __str__(self) -> str:
        values = ""
        for exp in self.args:
            values += f"{exp}, "
        for assign in self.kwargs:
            values += f"{assign}, "
        values = values[:-2]
        return f"{self.func_name.variable_name}({values})"
