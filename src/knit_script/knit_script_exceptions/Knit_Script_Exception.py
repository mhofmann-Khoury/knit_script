"""Module contains knitscript exceptions that are raised when violating knitting specific logic in a knitscript program.
"""

from __future__ import annotations

from knitout_interpreter.knitout_operations.knitout_instruction import Knitout_Instruction_Type
from virtual_knitting_machine.machine_components.needles.Needle import Needle


class Knit_Script_Exception(Exception):
    """Superclass for all exceptions related to processing KnitScript programs.

    The Knit_Script_Exception class provides the foundation for all error handling in the KnitScript programming language.
    It extends Python's built-in Exception class with KnitScript-specific formatting and behavior,
    ensuring that all KnitScript errors have consistent message formatting and can be caught collectively when needed.
    """

    def __init__(self, message: str | BaseException) -> None:
        """Initialize the Knit_Script_Exception.

        Creates a new KnitScript exception with the provided error message.
        The message is automatically formatted with a KnitScript exception prefix and newline formatting for consistent error display.

        Args:
            message (str | BaseException): The error message to display. If this is a string, the message will be prefixed with the error class name.
        """
        super().__init__(str(message) if isinstance(message, BaseException) else f"\n{self.__class__.__name__}: {message}")


class Incompatible_In_Carriage_Pass_Exception(Knit_Script_Exception):
    """Exception raised when instructions are combined in a carriage pass that are incompatible.

    This exception occurs when two or more instruction types are used together in a single carriage pass but cannot be executed simultaneously due to machine limitations or logical conflicts.

    Attributes:
        first_instruction (Knitout_Instruction_Type): The first instruction in the incompatible combination.
        second_instruction (Knitout_Instruction_Type): The second instruction in the incompatible combination.
    """

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
    """Exception raised when attempting a carriage pass without specifying a direction for yarn-carrier operations.

    This exception occurs when operations that require yarn carriers are attempted without establishing a carriage direction, which is necessary for proper yarn handling and loop formation.

    Attributes:
        instruction_type (Knitout_Instruction_Type): The instruction type that requires a direction.
    """

    def __init__(self, instruction_type: Knitout_Instruction_Type):
        """Initialize the Required_Direction_Exception.

        Args:
            instruction_type (Knitout_Instruction_Type): The instruction type that requires a direction.
        """
        self.instruction_type = instruction_type
        super().__init__(f"Cannot {self.instruction_type} without declaring a direction")


class All_Needle_Operation_Exception(Knit_Script_Exception):
    """Exception raised when an all-needle operation occurs without an all-needle racking.

    This exception occurs when operations that require all needles to be properly aligned (such as certain transfer operations)
    are attempted when the machine racking is not set to an all-needle position.

    Attributes:
        first_needle (Needle): The first needle in the operation.
        second_needle (Needle): The second needle in the operation.
        instruction (Knitout_Instruction_Type): The instruction type being attempted.
        racking (int): The current racking value.
    """

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
    """Exception raised when no working carrier has been declared for operations that require one.

    This exception occurs when knitting or tucking operations are attempted without first declaring a working yarn carrier, which is necessary for these operations to form proper loops.
    """

    def __init__(self) -> None:
        """Initialize the No_Declared_Carrier_Exception."""
        super().__init__("No declared working carriers to knit or tuck with.")
