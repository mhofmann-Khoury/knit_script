"""
A module containing a decorator for tracking debuggable frames when entering a subscope in knitscript.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, cast

from knit_script.debugger.debug_protocol import Knit_Script_Debuggable_Protocol
from knit_script.knit_script_interpreter.scope.local_scope import Knit_Script_Scope

# Type variables for the decorator
_P = ParamSpec("_P")  # Captures all parameters for methods that start with the instruction


def enters_new_scope(scope_entering_method: Callable[_P, Knit_Script_Scope]) -> Callable[_P, Knit_Script_Scope]:
    """
    Decorates a method that exits the current scope

    Args:
        scope_entering_method (Callable[[Knit_Script_Debuggable_Protocol, ], Knit_Script_Scope]): The scoping method to wrap.

    Returns:
        Callable[[Knit_Script_Debuggable_Protocol, ], Knit_Script_Scope]:  The wrapped scoping method.
    """

    @wraps(scope_entering_method)
    def wrap_enter_sub_scope(*_args: _P.args, **_kwargs: _P.kwargs) -> Knit_Script_Scope:
        """
        Args:
            *_args:
                Positional arguments passed to the wrapped method. Expects a positional argument:
                - self (Knit_Script_Debuggable_Protocol): The debuggable process handling scoping.
            **_kwargs: Additional keyword arguments passed to the wrapped method.

        Returns:
            Knit_Script_Scope: The child scope entered by the wrapped method.
        """
        context: Knit_Script_Debuggable_Protocol = cast(Knit_Script_Debuggable_Protocol, _args[0] if len(_args) >= 1 else _kwargs["self"])
        if context.debugger is None:
            return scope_entering_method(*_args, **_kwargs)

        returned_scope = scope_entering_method(*_args, **_kwargs)
        context.debugger.enter_child_frame(returned_scope)
        return returned_scope

    return wrap_enter_sub_scope
