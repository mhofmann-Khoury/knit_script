"""Module containing the base class for KnitScript exceptions."""
from knitout_interpreter.knitout_operations.knitout_instruction import Knitout_Instruction_Type
from virtual_knitting_machine.machine_components.needles.Needle import Needle


class Knit_Script_Exception(Exception):
    """
        Superclass for All exceptions related to processing KnitScript programs.
    """

    def __init__(self, message: str):
        self.message = f"Knit Script Exception: {message}"
        super().__init__(self.message)


class Needle_Instruction_Type_Exception(Knit_Script_Exception):
    """
    Raised when providing an invalid instruction type to a carriage pass of needle instructions.
    """

    def __init__(self, instruction_type: Knitout_Instruction_Type):
        super().__init__(f"Expected instruction such as (knit, tuck, miss, split, xfer, drop) but got {instruction_type}")


class Incompatible_In_Carriage_Pass_Exception(Knit_Script_Exception):
    """
    Raised when instructions are combined in a carriage pass that are incompatible.
    """

    def __init__(self, first_instruction: Knitout_Instruction_Type, second_instruction: Knitout_Instruction_Type):
        self.second_instruction = second_instruction
        self.first_instruction = first_instruction
        super().__init__(f"Cannot {self.first_instruction} and {self.second_instruction} in same carriage pass")


class Required_Direction_Exception(Knit_Script_Exception):
    """
    Raised when attempting a carriage pass without specifying a direction for yarn-carrier operations.
    """

    def __init__(self, instruction_type: Knitout_Instruction_Type):
        self.instruction_type = instruction_type
        super().__init__(f"Cannot {self.instruction_type} without declaring a direction")


class Repeated_Needle_Exception(Knit_Script_Exception):
    """
    Raised when a carriage pass would require passing over the same needle more than once.
    """

    def __init__(self, needle: Needle):
        self.needle = needle
        super().__init__(f"Cannot work on {self.needle} more than once in a carriage pass.")


class All_Needle_Operation_Exception(Knit_Script_Exception):
    """
    Raised when an all-needle operation occurs without an all-needle racking.
    """

    def __init__(self, first_needle: Needle, second_needle: Needle, instruction: Knitout_Instruction_Type):
        self.first_needle = first_needle
        self.second_needle = second_needle
        self.instruction = instruction
        super().__init__(f"Cannot {self.instruction} on {self.first_needle} and {self.second_needle} at All-Needle racking.")


class No_Declared_Carrier_Exception(Knit_Script_Exception):
    """
        Error for reporting that no working carrier has been declared
    """

    def __init__(self):
        super().__init__("No declared working carriers to knit or tuck with.")


class Gauge_Value_Exception(Knit_Script_Exception):
    """
        Raised when gauge is set beyond the machine's capabilities
    """

    def __init__(self, gauge: int):
        super().__init__(f"Gauge must be between 0 and and the MAX_GAUGE but got {gauge}")


class Sheet_Value_Exception(Knit_Script_Exception):
    """
        Raised when sheet is set to an unacceptable value
    """

    def __init__(self, sheet: int, current_gauge: int):
        super().__init__(f"Sheet must be between 0 and gauge {current_gauge} but got {sheet}")
