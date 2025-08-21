"""Structures for declaring functions.

This module provides classes for function declaration and execution in knit script programs.
It includes the Function_Signature class for managing function objects and the Function_Declaration statement for creating and registering user-defined functions.
"""
import warnings
from typing import Any

from parglare.parser import LRStackNode

from knit_script.knit_script_exceptions.python_style_exceptions import (
    Knit_Script_NameError,
    Knit_Script_TypeError,
)
from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.variables import (
    Variable_Expression,
)
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.ks_element import KS_Element
from knit_script.knit_script_interpreter.scope.local_scope import Knit_Script_Scope
from knit_script.knit_script_interpreter.statements.assignment import Assignment
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knit_script_warnings.Knit_Script_Warning import Shadow_Variable_Warning


class Function_Signature:
    """Function object which processes parameter values and executes function calls.

    Handles parameter binding, scope management, and execution of user-defined functions in the knit script language.
    The Function_Signature class manages the complete lifecycle of function calls including parameter validation, argument binding, scope creation, body execution, and return value handling.

    This class provides the runtime representation of user-defined functions, encapsulating their parameters, body, default values, and execution context.
    It ensures proper scope isolation while allowing access to the module scope where the function was defined.

    Attributes:
        _name (str): The name of the function.
        _parameter_names (list[str]): List of parameter names in declaration order.
        _body (Statement): The statement body to execute when the function is called.
        _defaults (dict[str, Any]): Dictionary mapping parameter names to their default values.
        _module_scope (Knit_Script_Scope): The scope in which the function was defined.
    """

    def __init__(self, name: str, parameter_names: list[str], body: Statement, defaults: dict[str, Any], module_scope: Knit_Script_Scope | None, source_statement: KS_Element):
        """Initialize a function signature.

        Args:
            source_statement(Function_Declaration): The statement that declared this function signature.
            name (str): The name of the function.
            parameter_names (list[str]): List of parameter names in declaration order.
            body (Statement): The statement body to execute when the function is called.
            defaults (dict[str, Any]): Dictionary mapping parameter names to their default values.
            module_scope (Knit_Script_Scope): The scope in which the function was defined, used for lexical scoping.
        """
        self._source_statement: KS_Element = source_statement
        self._name: str = name
        self._parameter_names: list[str] = parameter_names
        self._body: Statement = body
        self._defaults: dict[str, Any] = defaults
        self._module_scope: Knit_Script_Scope | None = module_scope

    def execute(self, context: Knit_Script_Context, args: list[Expression], kwargs: list[Assignment]) -> Any:
        """Execute the function with the given arguments.

        Creates a new function scope, binds parameters to arguments, executes the function body, and returns the result.
        Handles parameter validation, default value assignment, and proper scope management throughout the function call.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
            args (list[Expression]): Positional arguments passed to the function, evaluated in order.
            kwargs (list[Assignment]): Keyword arguments passed as assignment objects with parameter names and values.

        Returns:
            Any: The return value of the function, or None if no return statement was executed.

        Raises:
            NameError: If an unexpected keyword argument is provided that doesn't match any parameter name.
            TypeError: If required parameters are missing values after processing all arguments and defaults.
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
                if key not in self._parameter_names:
                    raise Knit_Script_NameError(f"Unexpected key {key} given to function {self._name}", self._source_statement)
                context.variable_scope[key] = arg
            else:
                arg = exp.evaluate(context)
                context.variable_scope[param] = arg
                filled_params.add(param)
        for assignment in kwargs:
            key = assignment.variable_name
            if key not in self._parameter_names:
                raise Knit_Script_NameError(f"Unexpected key {key} given to function {self._name}", self._source_statement)
            assignment.assign_value(context)
            filled_params.add(key)
        missing_parameters = [p for p in self._parameter_names if p not in filled_params]
        if len(missing_parameters) > 0:
            raise Knit_Script_TypeError(f"Knit Script function {self._name} expected a value(s) for parameters: {missing_parameters}", self._source_statement)

        self._body.execute(context)  # execute function body
        return_value = context.variable_scope.return_value  # store return value before exiting scope
        context.exit_current_scope()  # leave parameter scope
        return return_value


class Function_Declaration(Statement):
    """Statement structure for declaring functions.

    Creates a function signature and adds it to the current variable scope, making it available for later function calls.
    The Function_Declaration statement processes function definitions and creates executable Function_Signature objects that can be called from other parts of the knit script program.

    This statement handles parameter processing, default value evaluation, and function signature creation while providing proper warnings for variable shadowing situations.

    Attributes:
        _func_name (str): The name of the function being declared.
        _args (list[Variable_Expression]): List of variable expressions representing positional parameters.
        _kwargs (list[Assignment]): List of assignment objects representing keyword parameters with defaults.
        _body (Statement): The statement body to execute when the function is called.
    """

    def __init__(self, parser_node: LRStackNode, func_name: str, args: list[Variable_Expression], kwargs: list[Assignment], body: Statement) -> None:
        """Initialize a function declaration.

        Args:
            parser_node (LRStackNode): The parser node from the abstract syntax tree.
            func_name (str): The name of the function being declared.
            args (list[Variable_Expression]): List of variable expressions representing positional parameters.
            kwargs (list[Assignment]): List of assignment objects representing keyword parameters with default values.
            body (Statement): The statement body to execute when the function is called.
        """
        super().__init__(parser_node)
        self._kwargs: list[Assignment] = kwargs
        self._args: list[Variable_Expression] = args
        self._body: Statement = body
        self._func_name: str = func_name

    def __str__(self) -> str:
        """Return string representation of the function declaration.

        Returns:
            str: A string showing the function name, parameters, and body.
        """
        return f"{self._func_name}({self._args}, {self._kwargs}) -> {self._body}"

    def __repr__(self) -> str:
        """Return detailed string representation of the function declaration.

        Returns:
            str: Same as __str__ for this class.
        """
        return str(self)

    def execute(self, context: Knit_Script_Context) -> None:
        """Execute the function declaration by creating and storing the function.

        Creates a Function_Signature object with the specified parameters and body, evaluates default values, and adds the function to the current variable scope.
        Issues warnings for parameter names that shadow existing variables.

        Args:
            context (Knit_Script_Context): The current execution context of the knit script interpreter.
        """
        params = []
        defaults = {}
        for arg in self._args:
            params.append(arg.variable_name)
            if arg.variable_name in context.variable_scope:
                warnings.warn(Shadow_Variable_Warning(arg.variable_name), self)
        for kwarg in self._kwargs:
            params.append(kwarg.variable_name)
            if kwarg.variable_name in context.variable_scope:
                warnings.warn(Shadow_Variable_Warning(kwarg.variable_name), self)
            defaults[kwarg.variable_name] = kwarg.value(context)

        function = Function_Signature(self._func_name, params, self._body, defaults, context.variable_scope.module_scope, self)
        context.variable_scope[self._func_name] = function  # assign to current scope
