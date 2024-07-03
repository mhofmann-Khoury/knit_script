"""Structures for declaring functions"""
import warnings
from typing import Any

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.expressions.variables import Variable_Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.scope.local_scope import Knit_Script_Scope
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knit_script_interpreter.statements.assignment import Assignment
from knit_script.knit_script_warnings.Knit_Script_Warning import Shadow_Variable_Warning


class Function_Signature:
    """
        Function object which processes parameter values and executes function call
    """

    def __init__(self, name: str, parameter_names: list[str], body: Statement, defaults: dict[str, Any], module_scope: Knit_Script_Scope):
        """
        Instantiate
        :param name: name of function
        :param parameter_names: list of parameter names
        :param body: the body to execute on call
        :param defaults: key parameter names to default values
        """
        self._name: str = name
        self._parameter_names: list[str] = parameter_names
        self._body: Statement = body
        self._defaults: dict[str, Any] = defaults
        self._module_scope: Knit_Script_Scope = module_scope

    def execute(self, context: Knit_Script_Context, args: list[Expression], kwargs: list[Assignment]) -> Any:
        """
        Puts parameters from call into scope and executes function code
        :param context:  The current context of the knit_script_interpreter
        :param args: args passed in order
        :param kwargs: args passed with keywords
        """
        context.enter_sub_scope(function_name=self._name, module_scope=self._module_scope)  # enter function scope, set as function for return statements
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
            # assert key in self._parameter_names, f"Unexpected key {key} given to function {self._name}"
            assignment.assign_value(context)
            filled_params.add(key)
        missing_parameters = [p for p in self._parameter_names if p not in filled_params]
        if len(missing_parameters) > 0:
            raise TypeError(f"Knit Script function {self._name} expected a value(s) for parameters: {missing_parameters}")

        self._body.execute(context)  # execute function body
        return_value = context.variable_scope.return_value  # store return value before exiting scope and deleting it
        context.exit_current_scope()  # leave parameter scope
        return return_value


class Function_Declaration(Statement):
    """
        Statement structure for declaring functions
    """

    def __init__(self, parser_node, func_name: str, args: list[Variable_Expression], kwargs: list[Assignment], body: Statement):
        """
        Instantiate
        :param parser_node:
        :param func_name: Name of function.
        :param args: List of variables for arguments.
        :param kwargs: List of key word assignments.
        :param body: Body to execute.
        """
        super().__init__(parser_node)
        self._kwargs: list[Assignment] = kwargs
        self._args: list[Variable_Expression] = args
        self._body: Statement = body
        self._func_name: str = func_name

    def __str__(self):
        return f"{self._func_name}({self._args}, {self._kwargs}) -> {self._body}"

    def __repr__(self):
        return str(self)

    def execute(self, context: Knit_Script_Context):
        """
        Puts function object with variable signature into variable scope
        :param context: The current context of the knit_script_interpreter
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
