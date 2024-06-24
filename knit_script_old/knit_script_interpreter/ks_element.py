from parglare.common import Location
from parglare.parser import LRStackNode


class KS_Element:
    """Super class of all parser elements in KS"""
    def __init__(self, parser_node: LRStackNode):
        self.parser_node = parser_node

    @property
    def location(self) -> Location:
        """
        :return: location of this symbol in KnitScript file
        """
        return self.parser_node.symbol.location

    @property
    def line_number(self) -> int:
        """
        :return: Line number of the symbol that generated this statement
        """
        return self.location.line
