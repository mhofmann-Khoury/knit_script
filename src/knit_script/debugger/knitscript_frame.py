"""Frame tracking for KnitScript execution tracing.

This module provides frame-level execution tracking for KnitScript programs,
similar to how Python's sys.settrace() provides frame objects during debugging.
"""

from __future__ import annotations

from typing import Any

from knit_script.debugger.debug_protocol import Debuggable_Element
from knit_script.knit_script_interpreter.scope.local_scope import Knit_Script_Scope


class Knit_Script_Frame:
    """Execution frame for KnitScript programs.

    This class tracks the execution state of a KnitScript program at a specific
    point in time, analogous to Python's frame objects in sys.settrace().

    Attributes:
        frame_id (int): Unique identifier for this frame.
        parent_frame (Knit_Script_Frame | None): Reference to the calling frame.
        child_frames (list[Knit_Script_Frame]): List of frames called from this frame.
    """

    _FRAME_COUNT: int = 0

    def __init__(self, scope: Knit_Script_Scope, parent_frame: Knit_Script_Frame | None = None) -> None:
        """Initialize a KnitScript execution frame.

        Args:
            scope (Knit_Script_Scope): The scope that this frame is being executed in.
            parent_frame (Knit_Script_Frame, optional): Optional parent frame in call stack.
        """
        self.frame_id: int = self._FRAME_COUNT
        Knit_Script_Frame._FRAME_COUNT += 1
        self.parent_frame: Knit_Script_Frame | None = parent_frame
        self._depth: int = 0 if self.parent_frame is None else self.parent_frame.depth + 1

        self.statement_history: list[Debuggable_Element] = []
        self.ks_scope: Knit_Script_Scope = scope

        # Execution history
        self.child_frames: list[Knit_Script_Frame] = []

    @property
    def depth(self) -> int:
        """
        Returns:
            int: The depth of this frame in the call stack.

        Notes:
            The first frame created when running the file is 0 and the call stack depth increments for the depth of the tree.
        """
        return self._depth

    @property
    def first_statement(self) -> Debuggable_Element | None:
        """
        Returns:
            Statement | None: The first statement executed in this frame, or None if this frame is empty.
        """
        return self.statement_history[0] if len(self.statement_history) > 0 else None

    @property
    def last_statement(self) -> Debuggable_Element | None:
        """
        Returns:
            Statement | None: The last statement executed in this frame, or None if this frame is empty.
        """
        return self.statement_history[-1] if len(self.statement_history) > 0 else None

    @property
    def first_line_number(self) -> int:
        """
        Returns:
            int: Line number of the first statement executed in this frame. 0 if no statements have been executed.
        """
        return self.first_statement.line_number if self.first_statement is not None else 0

    @property
    def last_line_number(self) -> int:
        """
        Returns:
            int: Line number of the last statement executed in this frame. 0 if no statements have been executed.
        """
        return self.last_statement.line_number if self.last_statement is not None else 0

    @property
    def source_file(self) -> str | None:
        """
        Returns:
            str | None: The source file of the knitscript being executed or None if it is being executed from a python string.
        """
        return self.first_statement.file_name if self.first_statement is not None else None

    @property
    def is_function(self) -> bool:
        """
        Returns:
            bool: True if the current frame is execution of a named function. False otherwise.
        """
        return self.ks_scope.is_function

    @property
    def function_name(self) -> str | None:
        """
        Returns:
            str | None: The name of this frame's scope if it represents a function.
        """
        return self.ks_scope.function_name

    @property
    def module_name(self) -> str | None:
        """
        Returns:
            str | None: The name of this frame's scope if it represents a module.
        """
        return self.ks_scope.module_name

    @property
    def is_module(self) -> bool:
        """
        Returns:
            bool: True if the current frame is execution of a named module. False otherwise.
        """
        return self.ks_scope.is_module

    def get_call_stack(self) -> list[Knit_Script_Frame]:
        """Get the complete call stack from root to current frame.

        Returns:
            list[Knit_Script_Frame]: List of frames from root to current
        """
        stack: list[Knit_Script_Frame] = []
        current: Knit_Script_Frame | None = self
        while current is not None:
            stack.append(current)
            current = current.parent_frame
        return list(reversed(stack))

    def is_above(self, frame: Knit_Script_Frame) -> bool:
        """
        Args:
            frame (Knit_Script_Frame): The other frame to compare depth to.

        Returns:
            bool: True if this frame is above the other frame in the call stack.
        """
        return self.depth < frame.depth

    def is_below(self, frame: Knit_Script_Frame) -> bool:
        """
        Args:
            frame (Knit_Script_Frame): The other frame to compare depth to.

        Returns:
            bool: True if this frame is below the other frame in the call stack.
        """
        return self.depth > frame.depth

    def same_depth(self, frame: Knit_Script_Frame) -> bool:
        """
        Args:
            frame (Knit_Script_Frame): The other frame to compare depth to.

        Returns:
            bool: True if this frame is at the same level as the other frame in the call stack.
        """
        return self.depth == frame.depth

    def add_child_frame(self, child_frame: Knit_Script_Frame) -> None:
        """Register a child frame that was called from this frame.

        Args:
            child_frame: The child frame to register
        """
        self.child_frames.append(child_frame)

    def add_statement(self, statement: Debuggable_Element) -> None:
        """Add a statement to the execution history.

        Args:
            statement (Statement): The statement that was executed to add to the execution history.
        """
        self.statement_history.append(statement)

    def get_var(self, name: str) -> Any:
        """
        Args:
            name (str): Variable name to get from frame's scope.

        Returns:
            Any: Variable value

        Raises:
            KeyError: If variable not found in the frame's scope
        """
        return self.ks_scope[name]

    def has_var(self, name: str) -> bool:
        """
        Args:
            name (str): Variable name to search for in frame's scope.

        Returns:
            bool: True if variable exists in the frame's scope. False otherwise.
        """
        return name in self.ks_scope

    def __repr__(self) -> str:
        """String representation of the frame.

        Returns:
            str: Formatted string showing frame details
        """
        return str(self)

    def __str__(self) -> str:
        """String representation of the frame.

        Returns:
            str: Formatted string showing frame details
        """
        if len(self.statement_history) == 0:
            return f"Empty Frame_{self.frame_id} at depth {self.depth}"
        else:
            return f"Frame_{self.frame_id} at depth {self.depth} in file <{self.source_file}> lines {self.first_line_number}-{self.last_line_number}"

    def __int__(self) -> int:
        return self.frame_id

    def __eq__(self, other: object) -> bool:
        """
        Compares frames by order in which frames were created.

        Args:
            other (int | Frame): A frame or a frame id to compare to.

        Returns:
            bool: True if this frame matches the given frame or frame id. False, otherwise.
        """
        return int(self) == int(other) if isinstance(other, (int, Knit_Script_Frame)) else False

    def __hash__(self) -> int:
        return self.frame_id

    def __lt__(self, other: object) -> bool:
        """
        Compares frames by order in which frames were created.

        Args:
            other (int | Frame): A frame or a frame id to compare to.

        Returns:
            bool: If this frame comes before the other frame.

        Raises:
            TypeError: If the item to compare to is not a frame or an integer.
        """
        if not isinstance(other, (int, Knit_Script_Frame)):
            raise TypeError(f"Cannot compare frames to item <{other}> of type <{type(other)}>")
        return int(self) < int(other)
