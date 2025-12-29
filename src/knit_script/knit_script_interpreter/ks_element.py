"""Module containing the KS_Element Super Class.

This module provides the KS_Element base class, which serves as the foundation for all parser elements in the KnitScript language.
It provides common functionality for accessing parser node information, location data, and line number information that is essential for error reporting and debugging.
"""

from __future__ import annotations

import os
import warnings
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar, cast

from parglare.common import Location
from parglare.parser import LRStackNode

from knit_script.debugger.debug_decorator import debug_knitscript_statement
from knit_script.debugger.debug_protocol import Debuggable_Element
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.knitscript_logging.knitscript_logger import KnitScript_Logging_Level


class KS_Element(Debuggable_Element):
    """Superclass of all parser elements in KS.

    The KS_Element class provides the base functionality for all elements created during knit script parsing as a part of the abstract syntax tree.
    It maintains a reference to the parser node that created the element and provides convenient access to location information for error reporting and debugging purposes.

    This base class ensures that all knit script language elements have consistent access to their source location information,
    which is essential for providing meaningful error messages and debugging information to users.

    Attributes:
        parser_node (LRStackNode): The parser node that created this element.
    """

    def __init__(self, parser_node: LRStackNode):
        """Initialize the KS element with parser node information.

        Args:
            parser_node (LRStackNode): The parser node that created this element, containing location and context information.
        """
        self.parser_node: LRStackNode = parser_node

    @property
    def location(self) -> Location:
        """Get the location of this symbol in KnitScript file.

        Returns:
            Location: The location of this symbol in the source file, including file name, line number, and position information.
        """
        return Location(self.parser_node, self.parser_node.file_name)

    @property
    def line_number(self) -> int:
        """Get the line number of the symbol that generated this statement.

        Returns:
            int: The line number where this element appears in the source file.
        """
        return int(self.location.line)

    @property
    def file_name(self) -> str | None:
        """
        Returns:
            str | None: The file name of the knitscript program this was parsed from or None if the program was passed as a string.
        """
        return str(self.location.file_name) if self.location.file_name is not None else None

    @property
    def local_path(self) -> str | None:
        """
        Returns:
            str | None: The path to the directory containing the file from which this element was parsed or None if the value was parsed from a python string.
        """
        return os.path.dirname(self.file_name) if self.file_name is not None else None

    @property
    def location_str(self) -> str:
        """
        Returns:
            str: The string referencing the line number and possible file name information about this element.
        """
        file_str = ""
        if self.file_name is not None:
            file_str = f"in {self.file_name}"
        return f"on line {self.line_number}{file_str}"

    @property
    def position_context(self) -> str:
        """
        The position context string is the string from the knitscript program from which this element was parsed.
        The context string will begin at the start of this element and continue to the end of the line of knitscript or a semicolon on new line are reached.

        Returns:
            str: The string used to contextualize this element in the knitscript program.
        """
        context_str = str(self.location.input_str)[self.location.start_position : self.location.start_position + self.location.column_end]
        context_str = context_str.strip()  # strip white space
        context_str = context_str.rstrip(";")
        return context_str

    def __hash__(self) -> int:
        return hash((self.location.start_position, self.location.end_position, self.file_name))

    def __str__(self) -> str:
        return self.position_context

    def __repr__(self) -> str:
        return f"<{self.position_context}> {self.location_str}"


# Type variables for the decorator
_P = ParamSpec("_P")  # Captures all parameters for methods that start with the instruction
_R = TypeVar("_R")  # Captures return type for methods that start with the instruction


def associate_error(execution_method: Callable[_P, _R]) -> Callable[_P, _R]:
    """

    Args:
        execution_method (Callable[[KS_Element,], Any]): The wrapped method of a knitscript element to annotate associated errors.

    Returns:
        Callable[[KS_Element,], Any]: The wrapped method.
    """
    ks_error_note: str = "Error Raised when Executing Knitscript Program"

    @wraps(execution_method)
    def annotate_errors(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        """
        Wrap the method associated with the knit script element and annotate any caught errors with their location in the knitscript file.
        Args:
            self [KS_Element]: The method should start with or have a keyword self that is a knitscript element to associate with this error.
        """
        self: KS_Element = cast(KS_Element, args[0] if len(args) >= 1 else kwargs["self"])
        context: Knit_Script_Context = cast(Knit_Script_Context, args[1] if len(args) > 1 else kwargs["context"])
        caught_warnings = []

        try:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                return_val = execution_method(*args, **kwargs)
            for warning in caught:
                if not isinstance(warning.source, KS_Element):
                    warning.source = self
                    context.print(warning.message, self, KnitScript_Logging_Level.warning)
                    caught_warnings.append(warning)
            for warning in caught_warnings:
                warnings.warn(warning.message, stacklevel=1)
            return return_val
        except Exception as e:
            if not hasattr(e, "__notes__") or ks_error_note not in e.__notes__:
                e.add_note(ks_error_note)
                e.add_note(f"\t{e.__class__.__name__} at <{self.position_context}> in {self.location_str}")
                context.print(e, self, KnitScript_Logging_Level.error)
            raise

    if execution_method.__name__ == "execute":  # Wrapping an execute method which must also be debuggable.
        return debug_knitscript_statement(annotate_errors)
    else:  # Evaluations of expressions are not marked as debuggable, but their errors are annotated.
        return annotate_errors
