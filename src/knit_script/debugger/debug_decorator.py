"""Module containing decorator functions for Knit Script Debugger"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar, cast

from knit_script.debugger.debug_protocol import Debuggable_Element, Knit_Script_Debuggable_Protocol

# Type variables for the decorator
_P = ParamSpec("_P")  # Captures all parameters for methods that start with the instruction
_R = TypeVar("_R")  # Captures return type for methods that start with the instruction


def debug_knitscript_statement(execution_method: Callable[_P, _R]) -> Callable[_P, _R]:
    """
    Decorates execution methods of knit script statements so that the knit script debugger can act using the standard Python Debugger.

    Args:
        execution_method (Callable[[Statement, Knit_Script_Context], Any]):
            The statement's execution method to be debugged.

    Returns:
        Callable[[Statement, Knit_Script_Context], Any]:  The statement's execution method, wrapped with code to activate the Knit scrip debugger attached to the given context.
    """

    @wraps(execution_method)
    def wrap_with_knitscript_debug(*_args: _P.args, **_kwargs: _P.kwargs) -> _R:
        """
        Args:
            *_args:
                Positional arguments passed to the wrapped method. The positional argument expected are:
                - self (KS_Element): The statement being executed.
                - context (Knit_Script_Context): The context in which the statement is being executed and debugged.
            **_kwargs: Additional keyword arguments passed to the wrapped method.
        """
        statement: Debuggable_Element = cast(Debuggable_Element, _args[0] if len(_args) >= 1 else _kwargs["self"])
        context: Knit_Script_Debuggable_Protocol = cast(Knit_Script_Debuggable_Protocol, _args[1] if len(_args) >= 2 else _kwargs["context"])
        if context.debugger is None:
            return execution_method(*_args, **_kwargs)

        context.debugger.debug_statement(statement)  # Handles pausing logic for knitout debugger
        try:
            return execution_method(*_args, **_kwargs)
        except Exception as e:
            context.debugger.debug_error(statement, e)
            raise

    return wrap_with_knitscript_debug
