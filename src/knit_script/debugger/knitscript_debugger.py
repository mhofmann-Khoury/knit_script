"""Module containing the Knit_Script_Debugger class."""

from __future__ import annotations

import sys
import warnings
from collections.abc import Callable
from enum import Enum

from virtual_knitting_machine.Knitting_Machine_Snapshot import Knitting_Machine_Snapshot

from knit_script._warning_stack_level_helper import get_user_warning_stack_level_from_knitscript_package
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.ks_element import KS_Element
from knit_script.knit_script_interpreter.statements.Statement import Statement
from knit_script.knit_script_warnings.Knit_Script_Warning import Breakpoint_Condition_Error_Ignored_Warning


class KnitScript_Debug_Mode(Enum):
    """Enumeration of stepping modes for the debugger"""

    Continue = "continue"  # Sets the debugger to step until a breakpoint is reached.
    Step_Out = "step-out"  # Sets teh debugger to step out to the parent statement from the current step.
    Step_In = "step-in"  # Sets the debugger to step into any child statements of the current step or to the next step.
    Step_Over = "step-over"  # Sets the debugger to step to the next sibling statement of the current step or out to the next parent.


class Knit_Script_Debugger:
    """Attaches to knitscript interpreters to provide interactive debugging support through the python debugger.

    Attributes:
        machine_snapshots (dict[int, Knitting_Machine_Snapshot]): Dictionary mapping knitout line numbers that were paused on to the state of the knitting machine at that line.
    """

    def __init__(self) -> None:
        self._context: Knit_Script_Context | None = None
        self._debug_mode: KnitScript_Debug_Mode = KnitScript_Debug_Mode.Continue
        self._breakpoints: dict[int, Callable[[Knit_Script_Debugger], bool]] = {}
        self._disabled_breakpoints: set[int] = set()
        self._take_snapshots: bool = True
        self._condition_error: Exception | None = None
        self._stop_on_condition_error: bool = True
        self._raised_exceptions: set[BaseException] = set()
        self.machine_snapshots: dict[int, Knitting_Machine_Snapshot] = {}
        self._last_pause_element: KS_Element | None = None  # The element that the debugger last paused on.

    @property
    def take_step_in(self) -> bool:
        """
        Returns:
            bool: True if the debugger will stop at every execution and evaluation. False otherwise.
        """
        return self._debug_mode is KnitScript_Debug_Mode.Step_In

    @property
    def take_step_over(self) -> bool:
        """
        Returns:
            bool: True if the debugger will step to the next statement at the same level as the last pause. False otherwise.
        """
        return self._debug_mode is KnitScript_Debug_Mode.Step_Over

    @property
    def take_step_out(self) -> bool:
        """
        Returns:
            bool: True if the debugger will continue until it reaches the parent statement/expression of the last time it was paused (or the end of the program). False otherwise.
        """
        return self._debug_mode is KnitScript_Debug_Mode.Step_Out

    @property
    def continue_to_end(self) -> bool:
        """
        Returns:
            bool: True if the debugger will continue until the next breakpoint or end of the program. False otherwise.
        """
        return self._debug_mode is KnitScript_Debug_Mode.Continue

    @property
    def taking_snapshots(self) -> bool:
        """
        Returns:
            bool: True if the debugger is set to take snapshots of the knitting machine state when paused. False, otherwise.

        Notes:
            Snapshots are stored in the debugger's machine_snapshots dictionary.
        """
        return self._take_snapshots

    @property
    def stop_on_condition_errors(self) -> bool:
        """
        Returns:
            bool: True if the debugger will stop when conditions trigger an exception. False, otherwise.
        """
        return self._stop_on_condition_error

    def attach_interpreter(self, context: Knit_Script_Context) -> None:
        """
        Attaches the given interpreter to this debugger.

        Args:
            context (Knit_Script_Context): The context of the knitout interpreter to attach to this debugger.
        """
        self._context = context

    def detach_interpreter(self) -> None:
        """
        Detaches the current interpreter from this debugger.
        """
        self._context = None

    def set_breakpoint(self, line: int, condition: Callable[[Knit_Script_Debugger], bool] | None = None) -> None:
        """
        Sets a breakpoint with the optional condition for all statements/ expressions executed on the given knitscript line number.
        Args:
            line (int): The line number of the knitscript line to set the breakpoint for.
            condition (Callable[[KnitScript_Debugger], bool], optional): The optional condition used to determine if the breakpoint should be set. Defaults to no conditions on breaking.
        """
        if condition is None:
            condition = Knit_Script_Debugger._unconditioned_breakpoint
        self._breakpoints[line] = condition
        if line in self._disabled_breakpoints:
            self._disabled_breakpoints.remove(line)

    def clear_breakpoint(self, line: int) -> None:
        """
        Removes any breakpoint at the given knitscript line number.
        Args:
            line (int): The line number of the knitscript line to clear.
        """
        if line in self._disabled_breakpoints:
            self._disabled_breakpoints.remove(line)
        if line in self._breakpoints:
            del self._breakpoints[line]

    def enable_breakpoint(self, line: int) -> None:
        """
        Enables any disabled breakpoint at the given knitscript line number. If there is no breakpoint and unconditioned breakpoint is enabled.

        Args:
            line (int): The line number of the knitscript to enable the breakpoint for.
        """
        if line not in self._breakpoints:
            self.set_breakpoint(line)
        elif line in self._disabled_breakpoints:
            self._disabled_breakpoints.remove(line)

    def disable_breakpoint(self, line: int) -> None:
        """
        Disable any breakpoint at the given knitscript line number. If there is no breakpoint, nothing happens.
        Args:
            line (int): The line number of the knitscript to disable the breakpoint for.
        """
        if line in self._breakpoints:
            self._disabled_breakpoints.add(line)

    def step(self) -> None:
        """
        Sets the debugger to a step into every statement/ expression.
        """
        self._debug_mode = KnitScript_Debug_Mode.Step_In

    def step_over(self) -> None:
        """
        Sets the debugger to step at the same level as the last pause our out to a parent statement.
        """
        self._debug_mode = KnitScript_Debug_Mode.Step_Over

    def step_out(self) -> None:
        """
        Sets the debugger to a step out to the parent statement/ expression or to the end of the program.
        """
        self._debug_mode = KnitScript_Debug_Mode.Step_Out

    def continue_knitout(self) -> None:
        """
        Sets the debugger to continue to the next breakpoint or end of the knitout program.
        """
        self._debug_mode = KnitScript_Debug_Mode.Continue

    def enable_snapshots(self) -> None:
        """
        Sets the debugger to take snapshots of the knitting machine state whenever it pauses.
        """
        self._take_snapshots = True

    def disable_snapshots(self) -> None:
        """
        Sets the debugger to not take snapshots of the knitting machine state.
        """
        self._take_snapshots = False

    def ignore_condition_exceptions(self) -> None:
        """
        Sets the debugger to ignore condition exceptions and continue over these breakpoints.
        """
        self._stop_on_condition_error = False

    def pause_on_condition_exceptions(self) -> None:
        """
        Sets the debugger to stop when a breakpoint condition raises an exception.
        """
        self._stop_on_condition_error = True

    def _breakpoint_is_active(self, line: int) -> bool:
        """
        Args:
            line (int): The line number of the knitscript line to check the breakpoint for.

        Returns:
            bool: True if the debugger should pause on any enabled breakpoint at the given line and with its current state.

        Notes:
            If the debugger is set to pause on condition errors and the condition raises an exception, the breakpoint will be active.

        Warnings:
            Breakpoint_Condition_Error_Ignored_Warning: If the breakpoint condition triggers an error that is ignored and passed over.
        """
        try:
            return line not in self._disabled_breakpoints and line in self._breakpoints and self._breakpoints[line](self)
        except Exception as condition_error:
            if self.stop_on_condition_errors:
                self._condition_error = condition_error
                return True
            else:
                warnings.warn(Breakpoint_Condition_Error_Ignored_Warning(condition_error, line), stacklevel=get_user_warning_stack_level_from_knitscript_package())
                return False

    def _is_step_over(self, statement: Statement) -> bool:
        """
        Determine if the given statement is a step over from the last pause of the debugger.
        A step over will occur when an element is reached that is not a descendant of the last element paused on.

        Args:
            statement (Statement): The statement to plausible step over to.

        Returns:
            bool: True if the statement would constitute a step over from the last paused element. False otherwise.
        """
        return statement.is_known_descendant(self._last_pause_element)

    def pause_on_statement(self, statement: Statement) -> bool:
        """
        Determines if the given statement should trigger the next pause in the debugger.

        Args:
            statement (Statement): The next statement to consider pausing before.

        Returns:
            bool: True if the debugger should pause before the given statement. False, otherwise.
        """
        return (
            self.take_step_in
            or (self.take_step_over and self._is_step_over(statement))
            or (self.take_step_out and statement.is_parent(self._last_pause_element))
            or self._breakpoint_is_active(statement.line_number)
        )

    def debug_statement(self, statement: Statement) -> None:
        """
        Triggers a pause in the debugger based on the given statement and context
        Args:
            statement (Statement): The statement that triggered the pause and will be executed next.
        """
        if self._context is not None and self.pause_on_statement(statement):
            line_number: int = statement.line_number
            self._last_pause_element = statement
            if self.taking_snapshots:
                self.machine_snapshots[line_number] = Knitting_Machine_Snapshot(self._context.machine_state)
            if sys.gettrace() is not None and sys.stdin.isatty():  # Check if IDE debugger is attached
                print(f"\n{'=' * 70}")
                print("TODO: Evaluation of statement pause condition")  # TODO
                print(f"{'=' * 70}")
                self.print_user_guide()
                breakpoint()  # Break before statement
                self._condition_error = None  # reset any condition errors

    def debug_error(self, statement: Statement, exception: BaseException) -> None:
        """
        Pause the debugger because the given statement raised the given exception
        Args:
            statement (Statement): The statement that triggered the pause and will be executed next.
            exception (BaseException): The exception that triggered the pause and will be raised after this break.
        """
        if self._context is not None and exception not in self._raised_exceptions:
            self._raised_exceptions.add(exception)
            line_number: int = statement.line_number
            self._last_pause_element = statement
            if self.taking_snapshots:
                self.machine_snapshots[line_number] = Knitting_Machine_Snapshot(self._context.machine_state)
            if sys.gettrace() is not None and sys.stdin.isatty():  # Check if IDE debugger is attached
                print(f"\n{'=' * 70}")
                print(f"Knit Script paused by an {exception.__class__.__name__} raised on line {line_number}: {statement}")
                print(f"\t{exception}")
                print(f"{'=' * 70}")
                self.print_user_guide()
                breakpoint()  # Break exception is raised

    @staticmethod
    def print_user_guide() -> None:
        """
        Prints a guide of the knit script debuggers available commands and current state.

        TODO: Finish this method
        """
        print("TODO User GUIDE")

    @staticmethod
    def _unconditioned_breakpoint(_self: Knit_Script_Debugger) -> bool:
        """
        The default condition for breakpoints. It always returns True, applying no condition to the breakpoint.

        Args:
            _self (Knit_Script_Debugger): The unused knitscript debugger used to match the condition signature.

        Returns:
            bool: True; the breakpoint will always pass.
        """
        return True
