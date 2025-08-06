"""Module containing the KS_Element Super Class.

This module provides the KS_Element base class, which serves as the foundation for all parser elements in the KnitScript language.
It provides common functionality for accessing parser node information, location data, and line number information that is essential for error reporting and debugging.
"""
from parglare.common import Location
from parglare.parser import LRStackNode


class KS_Element:
    """Superclass of all parser elements in KS.

    The KS_Element class provides the base functionality for all elements created during knit script parsing.
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
