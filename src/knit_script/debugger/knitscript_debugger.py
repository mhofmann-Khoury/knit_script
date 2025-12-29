"""Module containing the Knit_Script_Debugger class."""

from __future__ import annotations

import os
import sys
import warnings
from collections.abc import Callable
from enum import Enum

from virtual_knitting_machine.Knitting_Machine_Snapshot import Knitting_Machine_Snapshot

from knit_script.debugger.debug_protocol import Debuggable_Element, Knit_Script_Debuggable_Protocol, Knit_Script_Debugger_Protocol
from knit_script.debugger.knitscript_frame import Knit_Script_Frame
from knit_script.knit_script_interpreter.knitscript_logging.knitscript_logger import KnitScript_Debug_Log
from knit_script.knit_script_interpreter.scope.local_scope import Knit_Script_Scope
from knit_script.knit_script_warnings.Knit_Script_Warning import Breakpoint_Condition_Error_Ignored_Warning


class KnitScript_Debug_Mode(Enum):
    """Enumeration of stepping modes for the debugger"""

    Continue = "continue"  # Sets the debugger to step until a breakpoint is reached.
    Step_Out = "step-out"  # Sets the debugger to step out to the parent statement from the current step.
    Step_In = "step-in"  # Sets the debugger to step into any child statements of the current step or to the next step.
    Step_Over = "step-over"  # Sets the debugger to step to the next sibling statement of the current step or out to the next parent.


class Knit_Script_Debugger(Knit_Script_Debugger_Protocol):
    """Attaches to knitscript interpreters to provide interactive debugging support through the python debugger.

    Attributes:
        machine_snapshots (dict[int, Knitting_Machine_Snapshot]): Dictionary mapping knitout line numbers that were paused on to the state of the knitting machine at that line.
    """

    def __init__(self, debug_logger: KnitScript_Debug_Log | None = None) -> None:
        self._logger: KnitScript_Debug_Log = KnitScript_Debug_Log() if debug_logger is None else debug_logger
        self._context: Knit_Script_Debuggable_Protocol | None = None
        self.frame: Knit_Script_Frame | None = None
        self._debug_mode: KnitScript_Debug_Mode = KnitScript_Debug_Mode.Continue
        self._breakpoints: dict[int, Callable[[Knit_Script_Debugger], bool]] = {}
        self._disabled_breakpoints: set[int] = set()
        self._take_snapshots: bool = True
        self._condition_error: Exception | None = None
        self._stop_on_condition_error: bool = True
        self._raised_exceptions: set[BaseException] = set()
        self.machine_snapshots: dict[int, Knitting_Machine_Snapshot] = {}
        self._exited_frame: Knit_Script_Frame | None = None
        self._checking_frame: Knit_Script_Frame | None = None

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

    def attach_context(self, context: Knit_Script_Debuggable_Protocol) -> None:
        """
        Attaches the given interpreter to this debugger.

        Args:
            context (Knit_Script_Debuggable_Protocol): The context of the knitout interpreter to attach to this debugger.
        """
        self._context = context
        self.frame = Knit_Script_Frame(context.variable_scope)
        self._checking_frame = self.frame

    def detach_context(self) -> None:
        """
        Detaches the current interpreter from this debugger.
        """
        self._context = None
        self.frame = None
        self._checking_frame = None

    def debug_statement(self, statement: Debuggable_Element) -> None:
        """
        Triggers a pause in the debugger based on the given statement and context.

        Args:
            statement (Statement): The statement that triggered the pause and will be executed next.
        """
        if self._context is not None and self.pause_on_statement(statement):
            was_step_out = self._is_step_out()
            self._checking_frame = self.frame
            line_number: int = statement.line_number
            machine_state, active_carrier, sheet, gauge = self._context.report_locals()
            if self.taking_snapshots:
                self.machine_snapshots[line_number] = Knitting_Machine_Snapshot(machine_state)
            if self._is_interactive_debugger_attached():
                self.print(f"\n{'=' * 70}")
                self.print(f"KnitScript Debugger Paused at <{repr(statement)}>")
                if self._breakpoint_is_active(line_number):
                    self.print("Paused at active breakpoint.")
                    if self._condition_error is not None:
                        self.print(f"Breakpoint Condition triggered an exception:\n\t{self._condition_error}")
                elif was_step_out and self._exited_frame is not None:
                    if self._exited_frame.is_function:
                        self.print(f"\t Exited function {self._exited_frame.function_name}")
                    elif self._exited_frame.is_module:
                        self.print(f"\t Exited module {self._exited_frame.module_name}")
                self.print(f"{'=' * 70}")
                self.print_user_guide()
                breakpoint()  # Break before statement
                self._condition_error = None  # reset any condition errors
        self.add_statement_to_frame(statement)
        self._exited_frame = None

    def debug_error(self, statement: Debuggable_Element, exception: BaseException) -> None:
        """
        Pause the debugger because the given statement raised the given exception.

        Args:
            statement (Statement): The statement that triggered the pause and will be executed next.
            exception (BaseException): The exception that triggered the pause and will be raised after this break.
        """
        if self._context is not None and exception not in self._raised_exceptions:
            self._raised_exceptions.add(exception)
            line_number: int = statement.line_number
            machine_state, active_carrier, sheet, gauge = self._context.report_locals()
            if self.taking_snapshots:
                self.machine_snapshots[line_number] = Knitting_Machine_Snapshot(machine_state)
            if self._is_interactive_debugger_attached():
                self.print(f"\n{'=' * 70}")
                self.print(f"Knit Script paused by an {exception.__class__.__name__}")
                self.print(f"\tPaused at <{repr(statement)}>")
                self.print(f"\t{exception}")
                self.print(f"{'=' * 70}")
                self.print_user_guide()
                breakpoint()  # Break exception is raised

    def enter_child_frame(self, scope: Knit_Script_Scope) -> None:
        """
        Enters a child frame with the given scope and makes it the main frame of the debugger.

        Args:
            scope (Knit_Script_Scope): The scope to enter the child frame.
        """
        child_frame = Knit_Script_Frame(scope, self.frame)
        if self.frame is not None:
            self.frame.add_child_frame(child_frame)
        self.frame = child_frame

    def exit_to_parent_frame(self) -> None:
        """
        Sets the current frame to the parent of the current frame.
        If there is no current frame, this is a No-op.
        """
        if self.frame is not None:
            self._exited_frame = self.frame
            self.frame = self.frame.parent_frame

    def restart_frame(self, scope: Knit_Script_Scope) -> None:
        """
        Sets the frame to a new frame without external context initiated with the given scope.

        Args:
            scope (Knit_Script_Scope): The scope to restart the current frame.
        """
        self._exited_frame = self.frame
        self.frame = Knit_Script_Frame(scope)

    def reset_debugger(self, reset_breaks: bool = False, clear_snapshots: bool = False) -> None:
        """
        Resets the debugger to a new starting state with no prior information about where it was debugging.
        Args:
            reset_breaks (bool, optional): If True, clears all prior information about breakpoints. Defaults to False.
            clear_snapshots (bool, optional): If True, clears all snapshots taken by the debugger. Defaults to False.
        """
        if reset_breaks:
            self._breakpoints = {}
            self._disabled_breakpoints = set()
        if clear_snapshots:
            self.machine_snapshots = {}
        self._condition_error = None
        self._raised_exceptions = set()

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

    def continue_knitscript(self) -> None:
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

    def _at_breakpoint(self, line: int) -> bool:
        """
        Args:
            line (int): The line number to pause at.

        Returns:
            bool: True if the debugger is at an active breakpoint, False otherwise.
        """
        return line not in self._disabled_breakpoints and line in self._breakpoints

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
            return self._at_breakpoint(line) and self._breakpoints[line](self)
        except Exception as condition_error:
            if self.stop_on_condition_errors:
                self._condition_error = condition_error
                return True
            else:
                warnings.warn(Breakpoint_Condition_Error_Ignored_Warning(condition_error, line), stacklevel=1)
                return False

    def pause_on_statement(self, statement: Debuggable_Element) -> bool:
        """
        Determines if the given statement should trigger the next pause in the debugger.

        Args:
            statement (KS_Element): The next statement to consider pausing before.

        Returns:
            bool: True if the debugger should pause before the given statement. False, otherwise.
        """
        return self.take_step_in or self._breakpoint_is_active(statement.line_number) or self._is_step_out() or self._is_step_over()

    def _is_step_out(self) -> bool:
        """
        Returns:
            bool: True if the debugger is set pause when stepping out of the last frame and the debugger just exited a frame.
        """
        return self.take_step_out and self._checking_frame is not None and self._exited_frame is not None and not self._exited_frame.is_below(self._checking_frame)

    def _is_step_over(self) -> bool:
        """
        Determine if the given statement is a step over from the last pause of the debugger.
        A step over will occur when the current frame is not a child of the last frame that was paused on.

        Returns:
            bool: True if the statement would constitute a step over from the last paused element. False otherwise.
        """
        return self.take_step_over and self._checking_frame is not None and self.frame is not None and not self.frame.is_below(self._checking_frame)

    def add_statement_to_frame(self, statement: Debuggable_Element) -> None:
        """
        Adds the given statement to those that have been executed in the current frame.
        Args:
            statement (KS_Element): The statement to add to the execution history.
        """
        if self.frame is not None:
            self.frame.add_statement(statement)

    def print(self, message: str) -> None:
        """
        Prints the given message to the debug logger.
        Args:
            message (str): The message to print.
        """
        self._logger.print(message)

    def print_user_guide(self) -> None:
        """Helper function that prints out the KnitScript Debugger Breakpoint command line interface and Usage Guide."""
        self.print(f"\n{'=' * 10}KnitScript Debugger Options{'=' * 20}")
        self.print("knitscript_debugger.step()                             # Sets the debugger to step through every statement")
        self.print("knitscript_debugger.step_over()                        # Sets the debugger to step over sub-statements")
        self.print("knitscript_debugger.step_out()                         # Sets the debugger to step out of the current scope")
        self.print("knitscript_debugger.continue_knitscript()              # Sets the debugger to continue to the next breakpoint")
        self.print("knitscript_debugger.set_breakpoint(N, condition)       # Sets a breakpoint at line N with an optional condition function.")
        self.print("knitscript_debugger.enable_breakpoint(N)               # Enables a breakpoint at line N. If no breakpoint is there, an unconditioned breakpoint is created.")
        self.print("knitscript_debugger.disable_breakpoint(N)              # Disables any breakpoint at line N. Any conditions are not removed.")
        self.print("knitscript_debugger.clear_breakpoint(N)                # Clears any breakpoint at line N. Any conditions are removed.")
        self.print("knitscript_debugger.enable_snapshots()                 # Enables the debugger to take snapshots of the machine state at any pause.")
        self.print("knitscript_debugger.disable_snapshots()                # Disables the debugger to take snapshots of the machine state at any pause.")
        self.print("knitscript_debugger.ignore_condition_exceptions()      # Stop the debugger from pausing when a breakpoint condition raises an exception.")
        self.print("knitscript_debugger.pause_on_condition_exceptions()    # Force teh debugger to pause when a breakpoint condition raises an exception.")

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

    @staticmethod
    def _is_interactive_debugger_attached() -> bool:
        """Check if an interactive debugger session is active.

        Uses multiple heuristics to detect interactive debugging across
        different IDEs and platforms (PyCharm, VSCode, etc.).

        Returns:
            bool: True if an interactive debugger session is active. False otherwise.
        """
        # No trace function = no debugger
        if sys.gettrace() is None:
            return False

        # Check: CI/automated environment detection (if these exist, this session is not interactive and shouldn't be debugged)
        ci_indicators = {
            "CI",
            "CONTINUOUS_INTEGRATION",  # Generic CI
            "GITHUB_ACTIONS",  # GitHub Actions
            "TRAVIS",
            "CIRCLECI",  # Other CI systems
            "JENKINS_HOME",
        }
        if any(var in os.environ for var in ci_indicators):
            return False

        # Check: Known debugger modules
        trace = sys.gettrace()
        if trace is not None:
            trace_module = getattr(trace, "__module__", "")
            interactive_debuggers = ["pydevd", "pdb", "bdb", "debugpy", "_pydevd_bundle"]
            if any(debugger in trace_module for debugger in interactive_debuggers):
                return True

        # Check: IDE environment variables
        ide_indicators = {
            "PYCHARM_HOSTED",  # PyCharm
            "PYDEVD_LOAD_VALUES_ASYNC",  # PyCharm debugger
            "VSCODE_PID",  # VSCode
        }
        if any(var in os.environ for var in ide_indicators):
            return True

        # Check: TTY as fallback. An interactive console found (only reliable on Unix)
        return sys.stdin.isatty()
