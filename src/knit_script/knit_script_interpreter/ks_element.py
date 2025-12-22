"""Module containing the KS_Element Super Class.

This module provides the KS_Element base class, which serves as the foundation for all parser elements in the KnitScript language.
It provides common functionality for accessing parser node information, location data, and line number information that is essential for error reporting and debugging.
"""

from __future__ import annotations

from collections.abc import Iterable

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
        parent_element (KS_Element | None): The element that is a parent to this element in the abstract syntax tree. None if the element has no parent.
        child_elements (set[KS_Element]): The elements that are children of this element in the abstract syntax tree.
    """

    def __init__(self, parser_node: LRStackNode):
        """Initialize the KS element with parser node information.

        Args:
            parser_node (LRStackNode): The parser node that created this element, containing location and context information.
        """
        self.parser_node: LRStackNode = parser_node
        self.parent_element: KS_Element | None = None
        self.child_elements: set[KS_Element] = set()
        self._known_descendants: set[KS_Element] = set()

    def add_children(self, child_element: Iterable[KS_Element] | KS_Element | None) -> None:
        """
        Adds the child element(s) to the children of this KS_Element.
        Args:
            child_element (Iterable[KS_Element] | KS_Element): The child element(s) to add.
        """
        if child_element is None:
            return
        elif isinstance(child_element, KS_Element):
            self.child_elements.add(child_element)
            self._known_descendants.add(child_element)
            child_element.set_parent_element(self)
        else:
            self.child_elements.update(child_element)
            self._known_descendants.update(child_element)
            for child in child_element:
                child.set_parent_element(self)

    def _add_known_descendants(self, known_descendant: Iterable[KS_Element] | KS_Element) -> None:
        """
        Adds the given descendant(s) to the set of known descendants of this KS_Element.
        Args:
            known_descendant (Iterable[Ks_Element] | KS_Element): The descendants to add.
        """
        if isinstance(known_descendant, KS_Element):
            self._known_descendants.add(known_descendant)
        else:
            self._known_descendants.update(known_descendant)

    def set_parent_element(self, parent_element: KS_Element) -> None:
        """
        Sets the parent element of this KS_Element. Updates that parent's known descendants with this element's descendants.

        Args:
            parent_element (KS_Element): The parent element of this KS_Element.
        """
        self.parent_element = parent_element
        self.parent_element._add_known_descendants(self)
        self.parent_element._add_known_descendants(self._known_descendants)

    @property
    def siblings(self) -> set[KS_Element]:
        """
        Returns:
            set[KS_Element]: The set of knitscript elements that are siblings to this element (i.e., they share a parent element in the abstract syntax tree).
        """
        if self.parent_element is None:
            return set()
        else:
            return self.parent_element.child_elements.difference({self})

    def is_sibling(self, sibling: KS_Element) -> bool:
        """
        Args:
            sibling (KS_Element): The potential sibling of this knitscript element.

        Returns:
            bool: True if the element shares a parent with this knitscript element, False otherwise.

        Notes:
            This method does not check that sibling is not this element. The method will return True in this case (i.e., element.is_sibling(self) returns True).
        """
        return self.parent_element is not None and sibling in self.parent_element.child_elements

    def is_parent(self, parent: KS_Element | None) -> bool:
        """
        Args:
            parent (KS_Element): The possible parent element of this knitscript element.

        Returns:
            bool: True if the element is parent to this knitscript element. False otherwise.
        """
        return parent is self.parent_element

    def is_child(self, child: KS_Element) -> bool:
        """
        Args:
            child (KS_Element): The potential child element of this knitscript element.

        Returns:
            bool: True if given a child element is in this knitscript element, False otherwise.
        """
        return child in self.child_elements

    def is_known_descendant(self, descendant: KS_Element | None) -> bool:
        """
        Args:
            descendant (KS_Element):  The potential descendant of this element.

        Returns:
            bool: True if the given element is a known descendent of this element. False otherwise.
        """
        return descendant is not None and descendant in self._known_descendants

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

    def __hash__(self) -> int:
        return hash(str(self.parser_node))

    def __str__(self) -> str:
        return str(self.parser_node)

    def __repr__(self) -> str:
        return str(self.parser_node)
