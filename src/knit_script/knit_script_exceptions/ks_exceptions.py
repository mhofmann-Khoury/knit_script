"""Module of common Knit Script Exceptions.

This module contains the exception classes used throughout the KnitScript programming language.
These exceptions cover various failure modes including assertion failures, parsing errors, machine operation conflicts, configuration errors, and fabric state issues.
Each exception provides detailed context about the specific error condition and includes relevant information for debugging and error recovery.
"""
from __future__ import annotations

from typing import Any

from knitout_interpreter.knitout_operations.knitout_instruction import (
    Knitout_Instruction_Type,
)
from virtual_knitting_machine.machine_components.needles.Needle import Needle

from knit_script.knit_script_exceptions.Knit_Script_Exception import (
    Knit_Script_Located_Exception,
)
from knit_script.knit_script_interpreter.ks_element import KS_Element


class Knit_Script_Assertion_Exception(AssertionError, Knit_Script_Located_Exception):
    """Exception raised when a KnitScript assertion fails.

    This exception is thrown when an assertion statement in KnitScript code evaluates to a falsy value.
    It provides detailed information about the failed condition and its actual value, along with any additional assertion report information that was provided with the assertion.
    """

    def __init__(self, assertion_statement: KS_Element, condition: Any, condition_value: Any, assertion_report: str | None = None) -> None:
        """Initialize the Knit_Script_Assertion_Exception.

        Args:
            assertion_statement (Assertion_Statement): The assertion statement from the knitscript file used to locate this error.
            condition (Any): The assertion condition that failed, typically an expression or condition object.
            condition_value (Any): The actual value that caused the assertion to fail.
            assertion_report (str | None, optional): Optional additional report information about the assertion failure. Defaults to None.
        """
        message = f"{condition} <{condition_value}>"
        if assertion_report is not None:
            message += f":\t{assertion_report}"
        AssertionError.__init__(self, condition, condition_value, assertion_report)
        Knit_Script_Located_Exception.__init__(self, message, assertion_statement)


class Needle_Instruction_Type_Exception(Knit_Script_Located_Exception):
    """Exception raised when providing an invalid instruction type to a carriage pass of needle instructions.

    This exception occurs when an instruction type that is not valid for needle operations is used in a context that expects needle-specific instructions
     such as knit, tuck, miss, split, xfer, or drop operations.
    """

    def __init__(self, needle_expression: KS_Element, instruction_type: Knitout_Instruction_Type):
        """Initialize the Needle_Instruction_Type_Exception.

        Args:
            needle_expression (Needle_Instruction_Exp): The Needle Instruction Expression used to locate the source of this error.
            instruction_type (Knitout_Instruction_Type): The invalid instruction type that was provided.
        """
        super().__init__(f"Expected instruction such as (knit, tuck, miss, split, xfer, drop) but got {instruction_type}", needle_expression)


class Incompatible_In_Carriage_Pass_Exception(Knit_Script_Located_Exception):
    """Exception raised when instructions are combined in a carriage pass that are incompatible.

    This exception occurs when two or more instruction types are used together in a single carriage pass but cannot be executed simultaneously due to machine limitations or logical conflicts.

    Attributes:
        first_instruction (Knitout_Instruction_Type): The first instruction in the incompatible combination.
        second_instruction (Knitout_Instruction_Type): The second instruction in the incompatible combination.
    """

    def __init__(self, source_statement: KS_Element, first_instruction: Knitout_Instruction_Type, second_instruction: Knitout_Instruction_Type):
        """Initialize the Incompatible_In_Carriage_Pass_Exception.

        Args:
            source_statement (KS_Element): The source statement of the carriage pass.
            first_instruction (Knitout_Instruction_Type): The first instruction type in the incompatible combination.
            second_instruction (Knitout_Instruction_Type): The second instruction type in the incompatible combination.
        """
        self.second_instruction = second_instruction
        self.first_instruction = first_instruction
        super().__init__(f"Cannot {self.first_instruction} and {self.second_instruction} in same carriage pass", source_statement)


class Required_Direction_Exception(Knit_Script_Located_Exception):
    """Exception raised when attempting a carriage pass without specifying a direction for yarn-carrier operations.

    This exception occurs when operations that require yarn carriers are attempted without establishing a carriage direction, which is necessary for proper yarn handling and loop formation.

    Attributes:
        instruction_type (Knitout_Instruction_Type): The instruction type that requires a direction.
    """

    def __init__(self, source_statement: KS_Element, instruction_type: Knitout_Instruction_Type):
        """Initialize the Required_Direction_Exception.

        Args:
            source_statement (KS_Element): The source statement of the carriage pass.
            instruction_type (Knitout_Instruction_Type): The instruction type that requires a direction.
        """
        self.instruction_type = instruction_type
        super().__init__(f"Cannot {self.instruction_type} without declaring a direction", source_statement)


class Repeated_Needle_Exception(Knit_Script_Located_Exception):
    """Exception raised when a carriage pass would require passing over the same needle more than once.

    This exception prevents machine operations that would attempt to work on the same needle multiple times within a single carriage pass, which is not physically possible on most knitting machines.

    Attributes:
        needle (Needle): The needle that would be worked on multiple times.
    """

    def __init__(self, source_statement: KS_Element, needle: Needle):
        """Initialize the Repeated_Needle_Exception.

        Args:
            source_statement (KS_Element): The source statement of the carriage pass.
            needle (Needle): The needle that would be worked on multiple times.
        """
        self.needle = needle
        super().__init__(f"Cannot work on {self.needle} more than once in a carriage pass.", source_statement)


class All_Needle_Operation_Exception(Knit_Script_Located_Exception):
    """Exception raised when an all-needle operation occurs without an all-needle racking.

    This exception occurs when operations that require all needles to be properly aligned (such as certain transfer operations)
    are attempted when the machine racking is not set to an all-needle position.

    Attributes:
        first_needle (Needle): The first needle in the operation.
        second_needle (Needle): The second needle in the operation.
        instruction (Knitout_Instruction_Type): The instruction type being attempted.
        racking (int): The current racking value.
    """

    def __init__(self, source_statement: KS_Element, first_needle: Needle, second_needle: Needle, racking: int, instruction: Knitout_Instruction_Type) -> None:
        """Initialize the All_Needle_Operation_Exception.

        Args:
            source_statement (KS_Element): The source statement of the carriage pass.
            first_needle (Needle): The first needle in the operation.
            second_needle (Needle): The second needle in the operation.
            racking (int): The current racking value.
            instruction (Knitout_Instruction_Type): The instruction type being attempted.
        """
        self.first_needle: Needle = first_needle
        self.second_needle: Needle = second_needle
        self.instruction: Knitout_Instruction_Type = instruction
        self.racking: int = racking
        super().__init__(f"Cannot {self.instruction} on {self.first_needle} and {self.second_needle} at All-Needle racking of {self.racking}.", source_statement)


class No_Declared_Carrier_Exception(Knit_Script_Located_Exception):
    """Exception raised when no working carrier has been declared for operations that require one.

    This exception occurs when knitting or tucking operations are attempted without first declaring a working yarn carrier, which is necessary for these operations to form proper loops.
    """

    def __init__(self, in_direction_statement: KS_Element) -> None:
        """Initialize the No_Declared_Carrier_Exception.

        Args:
            in_direction_statement (In_Direction_Statement): The input direction statement used to locate the error in the knit-script file.
        """
        super().__init__("No declared working carriers to knit or tuck with.", in_direction_statement)
