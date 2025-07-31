"""Module of common Knit Script Exceptions"""
from __future__ import annotations

from typing import Any

from knitout_interpreter.knitout_operations.knitout_instruction import Knitout_Instruction_Type
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_exceptions.Knit_Script_Exception import Knit_Script_Exception


class Knit_Script_Assertion_Exception(Knit_Script_Exception):
    """Exception raised when a KnitScript assertion fails."""

    def __init__(self, condition: Any, condition_value: Any, assertion_report: str | None = None) -> None:
        """Initialize the Knit_Script_Assertion_Exception.

        Args:
            condition (Expression): The assertion condition that failed.
            condition_value (Any): The actual value that caused the assertion to fail.
            assertion_report (str | None, optional): Optional additional report information about the assertion.
        """
        message = f"AssertionError:\n {condition} <{condition_value}>"
        if assertion_report is not None:
            message += f":{assertion_report}"
        super().__init__(message)


class Needle_Instruction_Type_Exception(Knit_Script_Exception):
    """Exception raised when providing an invalid instruction type to a carriage pass of needle instructions."""

    def __init__(self, instruction_type: Knitout_Instruction_Type):
        """Initialize the Needle_Instruction_Type_Exception.

        Args:
            instruction_type (Knitout_Instruction_Type): The invalid instruction type that was provided.
        """
        super().__init__(f"Expected instruction such as (knit, tuck, miss, split, xfer, drop) but got {instruction_type}")


class Incompatible_In_Carriage_Pass_Exception(Knit_Script_Exception):
    """Exception raised when instructions are combined in a carriage pass that are incompatible."""

    def __init__(self, first_instruction: Knitout_Instruction_Type, second_instruction: Knitout_Instruction_Type):
        """Initialize the Incompatible_In_Carriage_Pass_Exception.

        Args:
            first_instruction (Knitout_Instruction_Type): The first instruction type in the incompatible combination.
            second_instruction (Knitout_Instruction_Type): The second instruction type in the incompatible combination.
        """
        self.second_instruction = second_instruction
        self.first_instruction = first_instruction
        super().__init__(f"Cannot {self.first_instruction} and {self.second_instruction} in same carriage pass")


class Required_Direction_Exception(Knit_Script_Exception):
    """Exception raised when attempting a carriage pass without specifying a direction for yarn-carrier operations."""

    def __init__(self, instruction_type: Knitout_Instruction_Type):
        """Initialize the Required_Direction_Exception.

        Args:
            instruction_type (Knitout_Instruction_Type): The instruction type that requires a direction.
        """
        self.instruction_type = instruction_type
        super().__init__(f"Cannot {self.instruction_type} without declaring a direction")


class Repeated_Needle_Exception(Knit_Script_Exception):
    """Exception raised when a carriage pass would require passing over the same needle more than once."""

    def __init__(self, needle: Needle):
        """Initialize the Repeated_Needle_Exception.

        Args:
            needle (Needle): The needle that would be worked on multiple times.
        """
        self.needle = needle
        super().__init__(f"Cannot work on {self.needle} more than once in a carriage pass.")


class All_Needle_Operation_Exception(Knit_Script_Exception):
    """Exception raised when an all-needle operation occurs without an all-needle racking."""

    def __init__(self, first_needle: Needle, second_needle: Needle, racking: int, instruction: Knitout_Instruction_Type) -> None:
        """Initialize the All_Needle_Operation_Exception.

        Args:
            first_needle (Needle): The first needle in the operation.
            second_needle (Needle): The second needle in the operation.
            racking (int): The current racking value.
            instruction (Knitout_Instruction_Type): The instruction type being attempted.
        """
        self.first_needle: Needle = first_needle
        self.second_needle: Needle = second_needle
        self.instruction: Knitout_Instruction_Type = instruction
        self.racking: int = racking
        super().__init__(f"Cannot {self.instruction} on {self.first_needle} and {self.second_needle} at All-Needle racking of {self.racking}.")


class No_Declared_Carrier_Exception(Knit_Script_Exception):
    """Exception raised when no working carrier has been declared for operations that require one."""

    def __init__(self) -> None:
        """Initialize the No_Declared_Carrier_Exception."""
        super().__init__("No declared working carriers to knit or tuck with.")


class Gauge_Value_Exception(Knit_Script_Exception):
    """Exception raised when gauge is set beyond the machine's capabilities."""

    def __init__(self, gauge: int) -> None:
        """Initialize the Gauge_Value_Exception.

        Args:
            gauge (int): The invalid gauge value that was provided.
        """
        super().__init__(f"Gauge must be between 0 and and the MAX_GAUGE but got {gauge}")


class Sheet_Value_Exception(Knit_Script_Exception):
    """Exception raised when sheet is set to an unacceptable value."""

    def __init__(self, sheet: int, current_gauge: int) -> None:
        """Initialize the Sheet_Value_Exception.

        Args:
            sheet (int): The invalid sheet value that was provided.
            current_gauge (int): The current gauge setting.
        """
        super().__init__(f"Sheet must be between 0 and gauge {current_gauge} but got {sheet}")


class Sheet_Peeling_Stacked_Loops_Exception(Knit_Script_Exception):
    """Exception raised when trying to peel loops that cannot be returned to a separated state."""

    def __init__(self, front_needle: Needle, back_needle: Needle) -> None:
        """Initialize the Sheet_Peeling_Stacked_Loops_Exception.

        Args:
            front_needle (Needle): The front needle with recorded loops.
            back_needle (Needle): The back needle with recorded loops.
        """
        super().__init__(f"Loops recorded on {front_needle} and {back_needle}, but peeled loops cannot be returned to a seperated state")


class Sheet_Peeling_Blocked_Loops_Exception(Knit_Script_Exception):
    """Exception raised when loops cannot be returned due to blocking loops on the target needle."""

    def __init__(self, return_to_needle: Needle, return_from_needle: Needle) -> None:
        """Initialize the Sheet_Peeling_Blocked_Loops_Exception.

        Args:
            return_to_needle (Needle): The needle that has blocking loops.
            return_from_needle (Needle): The needle attempting to return loops.
        """
        super().__init__(f"Cannot return loops from {return_from_needle} because loops are held on {return_to_needle}")


class Lost_Sheet_Loops_Exception(Knit_Script_Exception):
    """Exception raised when loops are lost and the sheet cannot be reset."""

    def __init__(self, recorded_needle: Needle) -> None:
        """Initialize the Lost_Sheet_Loops_Exception.

        Args:
            recorded_needle (Needle): The needle where loops were recorded but are now lost.
        """
        super().__init__(f"Lost loops recorded on {recorded_needle}. Sheet cannot be reset.")
