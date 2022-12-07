"""Expression values that don't need context to evaluate"""
from enum import Enum
from typing import Any

from interpreter.expressions.expressions import Expression
from interpreter.parser.knit_pass_context import Knit_Script_Context
from knitting_machine.machine_components.machine_position import Machine_Bed_Position

class _Context_Free_Value(Expression):

    def __init__(self):
        super().__init__()

    def evaluate(self, context: Knit_Script_Context) -> Any:
        """
        Evaluate the expression
        :param context: The current context of the interpreter
        :return: the value
        """
        return self._context_free_evaluation()

    def _context_free_evaluation(self) -> Any:
        pass

    def __str__(self):
        return self._context_free_evaluation()

    def __repr__(self):
        return str(self)
class None_Value(_Context_Free_Value):
    """
        Used to None values
    """
    def __init__(self):
        super().__init__()

    def _context_free_evaluation(self) -> None:
        """
        :return: None value
        """
        return None


class Float_Value(_Context_Free_Value):
    """
        Processes numerical string into floating point value
    """

    def __init__(self, value: str):
        """
        Instantiate
        :param value: string with float value
        """
        super().__init__()
        self._value: str = value

    def _context_free_evaluation(self) -> float:
        """
        :return: floating point value
        """
        digits = ""
        for c in self._value:
            if c.isdigit() or c == "." or c == "-":
                digits += c
        return float(digits)

class Int_Value(Float_Value):
    """
        Expression of a single integer (not numerical expression) that evaluates to integer value
    """

    def __init__(self, value: str):
        super().__init__(value)

    def _context_free_evaluation(self) -> int:
        """
        :return: integer value of expression
        """
        return int(super()._context_free_evaluation())

class Bed_Value(_Context_Free_Value):
    """
        Expression of Needle bed
    """

    def __init__(self, bed_str: str):
        """
        Instantiate
        :param bed_str: string representing the bed
        """
        super().__init__()
        self._bed_str: str = bed_str

    def _context_free_evaluation(self) -> Machine_Bed_Position:
        """
        :return: Machine Bed Position from string (must be (f)ront or (b)ack)
        """
        capitalize = self._bed_str.capitalize()
        return Machine_Bed_Position[capitalize]


class Bed_Side(Enum):
    """Representation of left or right side of bed"""
    Right = "Right"
    Left = "Left"


class Bed_Side_Value(_Context_Free_Value):
    """
        Tracks which side of the bed the machine is currently on
    """

    def __init__(self, side: str):
        """
        Instantiate
        :param side:string representing the bed side
        """
        super().__init__()
        self._side:str = side

    def _context_free_evaluation(self) -> Bed_Side:
        """
        :return: Bed side represented by term
        """
        return Bed_Side[self._side]


class Boolean_Value(_Context_Free_Value):
    """
        Expressions of boolean values
    """

    def __init__(self, bool_str: str):
        """
        Instantiate
        :param bool_str: string representing the bool
        """
        super().__init__()
        self._bool_str:str = bool_str

    def _context_free_evaluation(self) -> bool:
        """
        :return: boolean value of expression
        """
        if self._bool_str == "True":
            return True
        else:
            return False



class String_Value(_Context_Free_Value):
    """
        Follows Python String Conventions
    """

    def __init__(self, string: str):
        """
        Instantiate
        :param string: the string
        """
        super().__init__()
        self._string:str = string

    def _context_free_evaluation(self) -> str:
        """
        :return: the string
        """
        return self._string

