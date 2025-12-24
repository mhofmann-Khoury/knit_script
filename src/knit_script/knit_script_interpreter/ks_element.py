"""Module containing the KS_Element Super Class.

This module provides the KS_Element base class, which serves as the foundation for all parser elements in the KnitScript language.
It provides common functionality for accessing parser node information, location data, and line number information that is essential for error reporting and debugging.
"""

from __future__ import annotations

import os

from parglare.common import Location
from parglare.parser import LRStackNode


class KS_Element:
    """Superclass of all parser elements in KS.

    The KS_Element class provides the base functionality for all elements created during knit script parsing as a part of the abstract syntax tree.
    It maintains a reference to the parser node that created the element and provides convenient access to location information for error reporting and debugging purposes.

    This base class ensures that all knit script language elements have consistent access to their source location information,
    which is essential for providing meaningful error messages and debugging information to users.

    Attributes:
        parser_node (LRStackNode): The parser node that created this element.
    """

    _KNITSCRIPT_NOTE = "Raised in when Processing KnitScript"

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

    @staticmethod
    def has_ks_notes(error: BaseException) -> bool:
        """
        Args:
            error (BaseException): The error raised to determine if it has already been marked with knitscript context information.

        Returns:
            bool: True if the error has been annotated with knitscript context information.

        """
        return hasattr(error, "__notes__") and error.__notes__[0] == KS_Element._KNITSCRIPT_NOTE

    def add_ks_information_to_error(self, error: BaseException) -> BaseException:
        """
        Args:
            error (BaseException): The error raised to add contextual notes based on this knitscript element.

        Returns:
            BaseException: The same exception modified with notes that document the location in the knitscript file that triggered the error.
        """
        if self.has_ks_notes(error):
            return error  # Already annotated, return as is.
        error.add_note(self._KNITSCRIPT_NOTE)
        error.add_note(f"\t{error.__class__.__name__} {self.location_str}")
        error.add_note(f"\t{self.position_context}")
        return error
