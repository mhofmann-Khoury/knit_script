"""Module containing the KS_Element Super Class"""
from parglare.common import Location
from parglare.parser import LRStackNode


class KS_Element:
    """Superclass of all parser elements in KS."""

    def __init__(self, parser_node: LRStackNode):
        """Initializes the KS element.

        Args:
            parser_node: The parser node that created this element
        """
        self.parser_node: LRStackNode = parser_node

    @property
    def location(self) -> Location:
        """Location of this symbol in KnitScript file.

        Returns:
            The location of this symbol in the file
        """
        return self.parser_node.symbol.location

    @property
    def line_number(self) -> int:
        """Line number of the symbol that generated this statement.

        Returns:
            The line number
        """
        return int(self.location.line)
