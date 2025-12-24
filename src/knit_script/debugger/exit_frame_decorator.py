"""
A module containing a decorator for tracking debuggable frames when entering a subscope in knitscript.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, cast

from knit_script.debugger.debug_protocol import Knit_Script_Debuggable_Protocol

# Type variables for the decorator
_P = ParamSpec("_P")  # Captures all parameters for methods that start with the instruction


def exits_scope(scope_exiting_method: Callable[_P, bool]) -> Callable[_P, bool]:
    """
    Decorates a method that exits the current scope

    Args:
        scope_exiting_method (Callable[[Knit_Script_Debuggable_Protocol, ], bool]): The scoping method to wrap.

    Returns:
        Callable[[Knit_Script_Debuggable_Protocol, ], bool]:  The wrapped scoping method.
    """

    @wraps(scope_exiting_method)
    def wrap_exit_current_scope(*_args: _P.args, **_kwargs: _P.kwargs) -> bool:
        """
        Args:
            *_args:
                Positional arguments passed to the wrapped method. Expects a positional argument:
                - self (Knit_Script_Debuggable_Protocol): The debuggable process exiting its current scope.
            **_kwargs: Additional keyword arguments passed to the wrapped method.

        Returns:
            bool: True if the scope exited into a parent scope. False, otherwise.
        """
        context: Knit_Script_Debuggable_Protocol = cast(Knit_Script_Debuggable_Protocol, _args[0] if len(_args) >= 1 else _kwargs["self"])
        if context.debugger is None:
            return scope_exiting_method(*_args, **_kwargs)

        exited_into_parent = scope_exiting_method(*_args, **_kwargs)
        if exited_into_parent:
            context.debugger.exit_to_parent_frame()
        else:
            context.debugger.restart_frame(context.variable_scope)
        return exited_into_parent

    return wrap_exit_current_scope
