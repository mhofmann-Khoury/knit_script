"""Module containing the Knit_Script_Debugger_Protocol"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.needles.Sheet_Identifier import Sheet_Identifier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import Yarn_Carrier_Set

if TYPE_CHECKING:
    from knit_script.knit_script_interpreter.scope.local_scope import Knit_Script_Scope


class Debuggable_Element(Protocol):
    """
    Protocol for debuggable elements in knitscript execution (i.e., statements).
    """

    @property
    def line_number(self) -> int:
        """
        Returns:
            int: The line number where this element appears in the source file.
        """
        ...

    @property
    def file_name(self) -> str | None:
        """
        Returns:
            str | None: The file name of the knitscript program this was parsed from or None if the program was passed as a string.
        """
        ...


class Knit_Script_Debuggable_Protocol(Protocol):
    """A protocol for any debuggable value"""

    debugger: Knit_Script_Debugger_Protocol | None  # The debuggable protocol attached to the debuggable value
    variable_scope: Knit_Script_Scope  # The scope of the debuggable process.

    def report_locals(self) -> tuple[Knitting_Machine, Yarn_Carrier_Set | None, Sheet_Identifier, int]:
        """
        Returns:
            tuple[Knitting_Machine, Yarn_Carrier_Set | None, Sheet_Identifier, int]:
                A tuple containing the following values from the state of the debugged protocol:
                * The current state of the knitting machine.
                * The active yarn-carrier set or None if no carrier set is active.
                * The current sheet that the machine is set to.
                * The gauge that the machine is set to.
        """
        ...


class Knit_Script_Debugger_Protocol(Protocol):
    """
    A protocol for a knitscript debugging process.
    """

    def attach_context(self, debuggable: Knit_Script_Debuggable_Protocol) -> None:
        """
        Attaches the given interpreter to this debugger.

        Args:
            debuggable (Knit_Script_Debuggable_Protocol): The debuggable process to attach to.
        """
        ...

    def detach_context(self) -> None:
        """
        Detaches the current interpreter from this debugger.
        """
        ...

    def debug_statement(self, statement: Debuggable_Element) -> None:
        """
        Triggers a pause in the debugger based on the given statement and context.

        Args:
            statement (KS_Element): The statement that triggered the pause and will be executed next.
        """
        ...

    def debug_error(self, statement: Debuggable_Element, exception: BaseException) -> None:
        """
        Pause the debugger because the given statement raised the given exception.

        Args:
            statement (KS_Element): The statement that triggered the pause and will be executed next.
            exception (BaseException): The exception that triggered the pause and will be raised after this break.
        """
        ...

    def enter_child_frame(self, scope: Knit_Script_Scope) -> None:
        """
        Enters a child frame with the given scope and makes it the main frame of the debugger.

        Args:
            scope (Knit_Script_Scope): The scope to enter the child frame.
        """
        ...

    def exit_to_parent_frame(self) -> None:
        """
        Sets the current frame to the parent of the current frame.
        If there is no current frame, this is a No-op.
        """
        ...

    def restart_frame(self, scope: Knit_Script_Scope) -> None:
        """
        Sets the frame to a new frame without external context initiated with the given scope.
        Args:
            scope (Knit_Script_Scope): The scope to restart the current frame.
        """
        ...

    def reset_debugger(self, reset_breaks: bool = False, clear_snapshots: bool = False) -> None:
        """
        Resets the debugger to a new starting state with no prior information about where it was debugging.
        Args:
            reset_breaks (bool, optional): If True, clears all prior information about breakpoints. Defaults to False.
            clear_snapshots (bool, optional): If True, clears all snapshots taken by the debugger. Defaults to False.
        """
        ...

    def print(self, message: str) -> None:
        """
        Prints the given message to the debug logger.
        Args:
            message (str): The message to print.
        """
        ...
