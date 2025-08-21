"""Expression values that don't need context to evaluate.

This module provides expression classes for literal values and context-free expressions in knit script programs.
These expressions represent constants and literal values that can be evaluated without requiring access to the current execution context,
including numbers, strings, booleans, and various enumerated types.
"""
from __future__ import annotations

from enum import Enum
from typing import Any

from knitout_interpreter.knitout_operations.Header_Line import Knitout_Header_Line_Type
from parglare.parser import LRStackNode
from virtual_knitting_machine.Knitting_Machine_Specification import (
    Knitting_Machine_Type,
)
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import (
    Carriage_Pass_Direction,
)

from knit_script.knit_script_interpreter.expressions.expressions import Expression
from knit_script.knit_script_interpreter.knit_script_context import Knit_Script_Context
from knit_script.knit_script_interpreter.Machine_Specification import (
    Machine_Bed_Position,
)


class _Context_Free_Value(Expression):
    """Base class used for context free evaluations that do not need information about the state of the program to be processed.

    The _Context_Free_Value class serves as the base for all expression types that represent literal values or constants that can be evaluated without access to the current execution context.
    These expressions have fixed values that don't depend on variable state, machine configuration, or other runtime information.

    This base class provides a common interface for context-free evaluation and standardizes the string representation behavior for all literal value expressions.
    """

    def __init__(self, parser_node: LRStackNode):
        """Initialize the context-free value expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
        """
        super().__init__(parser_node)

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """Evaluate the expression using context-free evaluation.

        Args:
            context (Knit_Script_Context): The current context of the knit_script_interpreter (unused for context-free values).

        Returns:
            Any: The constant value represented by this expression.
        """
        return self.context_free_evaluation()

    def context_free_evaluation(self) -> Any:
        """Get the evaluated value without requiring execution context.

        This method must be implemented by subclasses to return their constant value.

        Returns:
            Any: The evaluated value of this expression without requiring the current context.
        """
        pass

    def __str__(self) -> str:
        return str(self.context_free_evaluation())

    def __repr__(self) -> str:
        return str(self)


class None_Value(_Context_Free_Value):
    """Used to represent None values.

    The None_Value class represents Python's None literal in knit script expressions.
    It provides a constant None value that can be used in comparisons, assignments, and other operations where null values are needed.
    """

    def __init__(self, parser_node: LRStackNode) -> None:
        """Initialize the None_Value expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
        """
        super().__init__(parser_node)

    def context_free_evaluation(self) -> None:
        """Get the None value.

        Returns:
            None: Python's None value.
        """
        return None


class Float_Value(_Context_Free_Value):
    """Processes numerical string into floating point value.

    The Float_Value class handles floating-point literal expressions in knit script programs.
    It parses numeric string representations and converts them to Python float values, handling various numeric formats and extracting valid numeric characters.

    Attributes:
        _value (str): The original string representation of the floating-point number.
    """

    def __init__(self, parser_node: LRStackNode, value: str) -> None:
        """Initialize the Float_Value expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            value (str): String representation of the floating-point value.
        """
        super().__init__(parser_node)
        self._value: str = value

    def context_free_evaluation(self) -> float:
        """Get the floating point value from the string representation.

        Extracts valid numeric characters from the string and converts to a float value.

        Returns:
            float: The floating-point value represented by the string.
        """
        digits = ""
        for c in self._value:
            if c.isdigit() or c == "." or c == "-":
                digits += c
        return float(digits)


class Int_Value(Float_Value):
    """Expression of a single integer (not numerical expression) that evaluates to integer value.

    The Int_Value class extends Float_Value to handle integer literal expressions.
    It processes numeric strings and converts them to Python integer values, inheriting the numeric character extraction logic from Float_Value.
    """

    def __init__(self, parser_node: LRStackNode, value: str) -> None:
        """Initialize the Int_Value expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            value (str): String representation of the integer value.
        """
        super().__init__(parser_node, value)

    def context_free_evaluation(self) -> int:
        """Get the integer value from the string representation.

        Uses the parent class's float conversion and converts the result to an integer.

        Returns:
            int: The integer value represented by the string.
        """
        return int(super().context_free_evaluation())


class Bed_Value(_Context_Free_Value):
    """Expression of Needle bed positions.

    The Bed_Value class handles needle bed position literals in knit script programs.
    It converts string representations of bed positions into the corresponding Machine_Bed_Position enumeration values.

    Attributes:
        _bed_str (str): The string representation of the bed position.
    """

    def __init__(self, parser_node: LRStackNode, bed_str: str) -> None:
        """Initialize the Bed_Value expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            bed_str (str): String representing the bed position.
        """
        super().__init__(parser_node)
        self._bed_str: str = bed_str

    def context_free_evaluation(self) -> Machine_Bed_Position:
        """Get the Machine Bed Position from the string representation.

        Converts the bed string to the appropriate Machine_Bed_Position enumeration value, handling capitalization and slider designations.

        Returns:
            Machine_Bed_Position: The machine bed position corresponding to the string (front, back, front_slider, or back_slider).
        """
        capitalize = self._bed_str.capitalize()
        capitalize = capitalize.replace('s', 'S')
        return Machine_Bed_Position[capitalize]


class Boolean_Value(_Context_Free_Value):
    """Expressions of boolean values.

    The Boolean_Value class handles boolean literal expressions in knit script programs. It converts string representations of boolean values ("True"/"False") into Python boolean values.

    Attributes:
        _bool_str (str): The string representation of the boolean value.
    """

    def __init__(self, parser_node: LRStackNode, bool_str: str) -> None:
        """Initialize the Boolean_Value expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            bool_str (str): String representing the boolean value ("True" or "False").
        """
        super().__init__(parser_node)
        self._bool_str: str = bool_str

    def context_free_evaluation(self) -> bool:
        """Get the boolean value from the string representation.

        Converts the string representation to the corresponding Python boolean value.

        Returns:
            bool: True if the string is "True", False otherwise.
        """
        if self._bool_str == "True":
            return True
        else:
            return False


class String_Value(_Context_Free_Value):
    """Follows Python String Conventions.

    The String_Value class handles string literal expressions in knit script programs. It stores and provides access to string values following Python's string conventions and behavior.

    Attributes:
        _string (str): The string value content.
    """

    def __init__(self, parser_node: LRStackNode, string: str) -> None:
        """Initialize the String_Value expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            string (str): The string content.
        """
        super().__init__(parser_node)
        self._string: str = string

    def context_free_evaluation(self) -> str:
        """Get the string value.

        Returns:
            str: The string content.
        """
        return self._string


class _Xfer_Direction(Enum):
    """Enumerator for needle positioning during transfer operations.

    The _Xfer_Direction enumeration defines directional indicators used in transfer operations. It provides mapping between transfer direction keywords and the corresponding carriage pass directions.
    """
    Left = "Left"
    Right = "Right"

    def carriage_pass_direction(self) -> Carriage_Pass_Direction:
        """Get the carriage pass direction corresponding to this transfer direction.

        Returns:
            Carriage_Pass_Direction: The carriage pass direction that corresponds to this transfer direction.
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
    """Used for evaluating Machine Position identifiers in headers.

    The Machine_Position_Value class handles machine position literals used in knitout headers. It converts position string identifiers into the corresponding carriage pass direction values.

    Attributes:
        _position_str (str): The string representation of the machine position.
    """

    def __init__(self, parser_node: LRStackNode, position_str: str) -> None:
        """Initialize the Machine_Position_Value expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            position_str (str): String identifier for the machine position.
        """
        super().__init__(parser_node)
        self._position_str = position_str

    def context_free_evaluation(self) -> Carriage_Pass_Direction:
        """Get the carriage pass direction from the position string.

        Returns:
            Carriage_Pass_Direction: The carriage pass direction corresponding to the position identifier.
        """
        return _Xfer_Direction[self._position_str].carriage_pass_direction()


class Machine_Type_Value(_Context_Free_Value):
    """Used for evaluating Machine Type identifiers in headers.

    The Machine_Type_Value class handles machine type literals used in knitout headers. It converts type string identifiers into the corresponding Knitting_Machine_Type enumeration values.

    Attributes:
        _type_str (str): The string representation of the machine type.
    """

    def __init__(self, parser_node: LRStackNode, type_str: str) -> None:
        """Initialize the Machine_Type_Value expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            type_str (str): String identifier for the machine type.
        """
        super().__init__(parser_node)
        self._type_str = type_str

    def context_free_evaluation(self) -> Knitting_Machine_Type:
        """Get the knitting machine type from the type string.

        Returns:
            Knitting_Machine_Type: The machine type corresponding to the type identifier.
        """
        return Knitting_Machine_Type[self._type_str]


class Header_ID_Value(_Context_Free_Value):
    """Used for evaluating strings of header types.

    The Header_ID_Value class handles header type identifiers used in knitout header specifications. It converts header ID strings into the corresponding Knitout_Header_Line_Type enumeration values.

    Attributes:
        hid_str (str): The string representation of the header ID.
    """

    def __init__(self, parser_node: LRStackNode, hid_str: str) -> None:
        """Initialize the Header_ID_Value expression.

        Args:
            parser_node (LRStackNode): The parser node from the parse tree.
            hid_str (str): String identifier for the header type.
        """
        super().__init__(parser_node)
        self.hid_str = hid_str

    def context_free_evaluation(self) -> Knitout_Header_Line_Type:
        """Get the knitout header line type from the header ID string.

        Returns:
            Knitout_Header_Line_Type: The header line type corresponding to the header ID.
        """
        return Knitout_Header_Line_Type[self.hid_str]
