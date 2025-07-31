"""Structures for declaring functions"""
import warnings
from typing import Any

from parglare.parser import LRStackNode

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.scope.local_scope import Knit_Script_Scope
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knit_script_interpreter.statements.assignment import Assignment
from knit_script.knit_script_warnings.Knit_Script_Warning import Shadow_Variable_Warning


class Function_Signature:
    """Function object which processes parameter values and executes function calls.

    Handles parameter binding, scope management, and execution of user-defined
    functions in the knit script language.
    """

    def __init__(self, name: str, parameter_names: list[str], body: Statement, defaults: dict[str, Any], module_scope: Knit_Script_Scope):
        """Initialize a function signature.

        Args:
            name: The name of the function.
            parameter_names: List of parameter names in order.
            body: The statement body to execute when the function is called.
            defaults: Dictionary mapping parameter names to their default values.
            module_scope: The scope in which the function was defined.
        """
        self._name: str = name
        self._parameter_names: list[str] = parameter_names
        self._body: Statement = body
        self._defaults: dict[str, Any] = defaults
        self._module_scope: Knit_Script_Scope = module_scope

    def execute(self, context: Knit_Script_Context, args: list[Expression], kwargs: list[Assignment]) -> Any:
        """Execute the function with the given arguments.

        Creates a new function scope, binds parameters to arguments,
        executes the function body, and returns the result.

        Args:
            context: The current execution context of the knit script interpreter.
            args: Positional arguments passed to the function.
            kwargs: Keyword arguments passed as assignment objects.

        Returns:
            The return value of the function, or None if no return statement was executed.

        Raises:
            NameError: If an unexpected keyword argument is provided.
            TypeError: If required parameters are missing values.
        """
        context.enter_sub_scope(function_name=self._name, module_scope=self._module_scope)  # enter function scope
        filled_params = set()
        for param, arg in self._defaults.items():  # assign defaults, may get overridden
            context.variable_scope[param] = arg
            filled_params.add(param)
        for param, exp in zip(self._parameter_names, args):
            if isinstance(exp, Assignment):  # passed keyword argument
                key = exp.variable_name
                arg = exp.value(context)
                assert key in self._parameter_names, f"Unexpected key {key} given to function {self._name}"
                context.variable_scope[key] = arg
            else:
                arg = exp.evaluate(context)
                context.variable_scope[param] = arg
                filled_params.add(param)
        for assignment in kwargs:
            key = assignment.variable_name
            if key not in self._parameter_names:
                raise NameError(f"Unexpected key {key} given to function {self._name}")
            assignment.assign_value(context)
            filled_params.add(key)
        missing_parameters = [p for p in self._parameter_names if p not in filled_params]
        if len(missing_parameters) > 0:
            raise TypeError(f"Knit Script function {self._name} expected a value(s) for parameters: {missing_parameters}")

        self._body.execute(context)  # execute function body
        return_value = context.variable_scope.return_value  # store return value before exiting scope
        context.exit_current_scope()  # leave parameter scope
        return return_value


class Function_Declaration(Statement):
    """Statement structure for declaring functions.

    Creates a function signature and adds it to the current variable scope,
    making it available for later function calls.
    """

    def __init__(self, parser_node: LRStackNode, func_name: str, args: list[Variable_Expression], kwargs: list[Assignment], body: Statement) -> None:
        """Initialize a function declaration.

        Args:
            parser_node: The parser node from the abstract syntax tree.
            func_name: The name of the function being declared.
            args: List of variable expressions representing positional parameters.
            kwargs: List of assignment objects representing keyword parameters with defaults.
            body: The statement body to execute when the function is called.
        """
        super().__init__(parser_node)
        self._kwargs: list[Assignment] = kwargs
        self._args: list[Variable_Expression] = args
        self._body: Statement = body
        self._func_name: str = func_name

    def __str__(self) -> str:
        """Return string representation of the function declaration.

        Returns:
            A string showing the function name, parameters, and body.
        """
        return f"{self._func_name}({self._args}, {self._kwargs}) -> {self._body}"

    def __repr__(self) -> str:
        """Return detailed string representation of the function declaration.

        Returns:
            Same as __str__ for this class.
        """
        return str(self)

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the function declaration by creating and storing the function.

        Creates a Function_Signature object with the specified parameters and body,
        then adds it to the current variable scope.

        Args:
            context: The current execution context of the knit script interpreter.
        """
        params = []
        defaults = {}
        for arg in self._args:
            params.append(arg.variable_name)
            if arg.variable_name in context.variable_scope:
                warnings.warn(Shadow_Variable_Warning(arg.variable_name))
        for kwarg in self._kwargs:
            params.append(kwarg.variable_name)
            if kwarg.variable_name in context.variable_scope:
                warnings.warn(Shadow_Variable_Warning(kwarg.variable_name))
            defaults[kwarg.variable_name] = kwarg.value(context)

        function = Function_Signature(self._func_name, params, self._body, defaults, context.variable_scope)
        context.variable_scope[self._func_name] = function  # assign to current scope
