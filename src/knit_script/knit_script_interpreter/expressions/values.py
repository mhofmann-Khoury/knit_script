"""Expression values that don't need context to evaluate"""
from __future__ import annotations

from enum import Enum
from typing import Any

from knitout_interpreter.knitout_operations.Header_Line import Knitout_Header_Line_Type
from parglare.parser import LRStackNode
from virtual_knitting_machine.Knitting_Machine_Specification import Knitting_Machine_Type
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.Machine_Specification import Machine_Bed_Position


class _Context_Free_Value(Expression):
    """Base class used for context free evaluations that do not need information about the state of the program to be processed."""

    def __init__(self, parser_node: LRStackNode):
        super().__init__(parser_node)

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """Evaluate the expression.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter.

        Returns:
            Any: The value.
        """
        return self.context_free_evaluation()

    def context_free_evaluation(self) -> Any:
        """
        Returns:
            The evaluated value of this expression without requiring the current context.
        """
        pass

    def __str__(self) -> str:
        return str(self.context_free_evaluation())

    def __repr__(self) -> str:
        return str(self)


class None_Value(_Context_Free_Value):
    """Used to None values."""

    def __init__(self, parser_node: LRStackNode) -> None:
        super().__init__(parser_node)

    def context_free_evaluation(self) -> None:
        """Get None value.

        Returns:
            None: None value.
        """
        return None


class Float_Value(_Context_Free_Value):
    """Processes numerical string into floating point value."""

    def __init__(self, parser_node: LRStackNode, value: str) -> None:
        """Initialize the Float_Value.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            value (str): String with float value.
        """
        super().__init__(parser_node)
        self._value: str = value

    def context_free_evaluation(self) -> float:
        """Get floating point value.

        Returns:
            float: Floating point value.
        """
        digits = ""
        for c in self._value:
            if c.isdigit() or c == "." or c == "-":
                digits += c
        return float(digits)


class Int_Value(Float_Value):
    """Expression of a single integer (not numerical expression) that evaluates to integer value."""

    def __init__(self, parser_node: LRStackNode, value: str) -> None:
        super().__init__(parser_node, value)

    def context_free_evaluation(self) -> int:
        """Get integer value of expression.

        Returns:
            int: Integer value of expression.
        """
        return int(super().context_free_evaluation())


class Bed_Value(_Context_Free_Value):
    """Expression of Needle bed."""

    def __init__(self, parser_node: LRStackNode, bed_str: str) -> None:
        """Initialize the Bed_Value.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            bed_str (str): String representing the bed.
        """
        super().__init__(parser_node)
        self._bed_str: str = bed_str

    def context_free_evaluation(self) -> Machine_Bed_Position:
        """Get Machine Bed Position from string.

        Returns:
            Machine_Bed_Position: Machine Bed Position from string (must be (f)ront or (b)ack).
        """
        capitalize = self._bed_str.capitalize()
        capitalize = capitalize.replace('s', 'S')
        return Machine_Bed_Position[capitalize]


class Boolean_Value(_Context_Free_Value):
    """Expressions of boolean values."""

    def __init__(self, parser_node: LRStackNode, bool_str: str) -> None:
        """Initialize the Boolean_Value.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            bool_str (str): String representing the bool.
        """
        super().__init__(parser_node)
        self._bool_str: str = bool_str

    def context_free_evaluation(self) -> bool:
        """Get boolean value of expression.

        Returns:
            bool: Boolean value of expression.
        """
        if self._bool_str == "True":
            return True
        else:
            return False


class String_Value(_Context_Free_Value):
    """Follows Python String Conventions."""

    def __init__(self, parser_node: LRStackNode, string: str) -> None:
        """Initialize the String_Value.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            string (str): The string.
        """
        super().__init__(parser_node)
        self._string: str = string

    def context_free_evaluation(self) -> str:
        """Get the string.

        Returns:
            str: The string.
        """
        return self._string


class _Xfer_Direction(Enum):
    """Enumerator for needle positioning."""
    Left = "Left"
    Right = "Right"

    def carriage_pass_direction(self) -> Carriage_Pass_Direction:
        """
        Returns:
            The carriage pass direction that corresponds to this Xfer_Direction term.
        """
        if self is _Xfer_Direction.Left:
            return Carriage_Pass_Direction.Leftward
        else:
            return Carriage_Pass_Direction.Rightward

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(str(self))


class Machine_Position_Value(_Context_Free_Value):
    """Used for evaluating Machine Position identifiers in headers."""

    def __init__(self, parser_node: LRStackNode, position_str: str) -> None:
        super().__init__(parser_node)
        self._position_str = position_str

    def context_free_evaluation(self) -> Carriage_Pass_Direction:
        """
        Returns:
            The value to be evaluated without context.
        """
        return _Xfer_Direction[self._position_str].carriage_pass_direction()


class Machine_Type_Value(_Context_Free_Value):
    """Used for evaluating Machine Type identifiers in headers."""

    def __init__(self, parser_node: LRStackNode, type_str: str) -> None:
        super().__init__(parser_node)
        self._type_str = type_str

    def context_free_evaluation(self) -> Knitting_Machine_Type:
        """
        Returns:
            The value to be evaluated without context.
        """
        return Knitting_Machine_Type[self._type_str]


class Header_ID_Value(_Context_Free_Value):
    """Used for evaluating strings of header types."""

    def __init__(self, parser_node: LRStackNode, hid_str: str) -> None:
        super().__init__(parser_node)
        self.hid_str = hid_str

    def context_free_evaluation(self) -> Knitout_Header_Line_Type:
        """
        Returns:
            The value to be evaluated without context.
        """
        return Knitout_Header_Line_Type[self.hid_str]
