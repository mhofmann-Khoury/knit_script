"""A module containing the base class for Knitting Script warnings.

This module provides the base warning class and specific warning types for the KnitScript programming language.
These warnings alert developers to potentially problematic code patterns, configuration issues, and situations that may lead to unexpected behavior without causing program termination.
The warning system helps developers write more robust knit script programs by identifying common pitfalls and questionable practices during execution.
"""

from __future__ import annotations

from virtual_knitting_machine.machine_components.needles.Needle import Needle
from virtual_knitting_machine.machine_components.needles.Sheet_Identifier import Sheet_Identifier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import Yarn_Carrier_Set


class Knit_Script_Warning(RuntimeWarning):
    """Base class for warnings caused by error-prone code in Knit Script.

    The Knit_Script_Warning class serves as the foundation for all warning types in the KnitScript programming language.
    It extends Python's RuntimeWarning to provide KnitScript-specific warning behavior and consistent message formatting.
    All specific KnitScript warning types inherit from this class, creating a hierarchical warning system that allows for both specific and general warning handling patterns.

    This base class automatically prefixes warning messages with "KnitScript Warning:" to clearly identify KnitScript-related warnings and distinguish them from other system warnings.
    The warning system is designed to help developers identify potentially problematic code without stopping program execution.
    """

    def __init__(self, message: str):
        """Initialize the Knit_Script_Warning.

        Creates a new KnitScript warning with the provided message. The message is automatically formatted with a KnitScript warning prefix and newline formatting for consistent warning display.

        Args:
            message (str): The warning message to display. This will be prefixed with "KnitScript Warning:" in the final formatted message.
        """
        super().__init__(message)


class Shadow_Variable_Warning(Knit_Script_Warning):
    """Warning raised when a variable shadows another variable in an outer scope.

    This warning is issued when a variable is defined in a local scope that has the same name as a variable in an outer scope, potentially hiding the outer variable and causing confusion.
    Variable shadowing can lead to unexpected behavior when developers intend to access the outer variable but inadvertently access the inner one instead.

    Attributes:
        variable_name (str): The variable that shadows a higher scope.
    """

    def __init__(self, variable_name: str):
        """Initialize the Shadow_Variable_Warning.

        Args:
            variable_name (str): The name of the variable that is shadowing another variable in an outer scope.
        """
        self.variable_name: str = variable_name
        super().__init__(f"Variable <{variable_name}> shadows a variable in the outer scope.")


class Shadows_Global_Variable_Warning(Shadow_Variable_Warning):
    """Warning raised when a variable shadows a global variable.

    This specific type of shadow warning is issued when a local variable is defined with the same name as a global variable, potentially hiding the global variable.
    This is a more specific case of variable shadowing that focuses on global scope conflicts,
    which can be particularly problematic since global variables are often expected to be accessible throughout the program.
    """

    def __init__(self, variable_name: str):
        """Initialize the Shadows_Global_Variable_Warning.

        Args:
            variable_name (str): The name of the variable that is shadowing a global variable.
        """
        super().__init__(variable_name)
        self.message = f"Variable <{variable_name}> shadows a global variable."


class Sheet_Beyond_Gauge_Warning(Knit_Script_Warning):
    """Warning raised when the sheet setting exceeds the current gauge limits.

    This warning occurs when attempting to set a sheet number that is outside the valid range for the current gauge configuration.
    Since sheet numbers must be between 0 and gauge-1, this warning is issued when automatic correction is applied to bring the sheet value back within acceptable bounds.
    """

    def __init__(self, sheet: int | Sheet_Identifier, gauge: int):
        """Initialize the Sheet_Beyond_Gauge_Warning.

        Args:
            sheet (int | Sheet_Identifier): The sheet value that exceeds the gauge limits and triggered the warning.
            gauge (int): The current gauge setting that defines the valid range for sheet values.
        """
        super().__init__(f"Gauge of {gauge} is greater than current sheet {sheet} so sheet is set to {gauge - 1}")


class Negative_Sheet_Warning(Knit_Script_Warning):
    """Warning raised when the sheet value is negative and reset to 0.

    This warning occurs when attempting to set a sheet number that is outside the valid range for the current gauge configuration.
    Since sheet numbers must be between 0 and gauge-1, this warning is issued when automatic correction is applied to bring the sheet value back within acceptable bounds.
    """

    def __init__(self, sheet: int | Sheet_Identifier):
        """Initialize the Sheet_Beyond_Gauge_Warning.

        Args:
            sheet (int | Sheet_Identifier): The sheet value that exceeds the gauge limits and triggered the warning.
        """
        super().__init__(f"Sheets must be positive values but given {sheet} so sheet is set to 0")


class Gauge_Value_Warning(Knit_Script_Warning):
    """Warning raised when gauge is set to a non-positive value."""

    def __init__(self, gauge: int) -> None:
        """
        Args:
            gauge (int): The invalid gauge value that was provided and caused the warning.
        """
        super().__init__(f"Gauge must be 1 or greater but got {gauge}. Gauge set to to 1 (Full Gauge)")


class Cut_Unspecified_Carrier_Warning(Knit_Script_Warning):
    """Warning raised when no carrier is specified with a cut operation."""

    def __init__(self, cur_carrier_set: Yarn_Carrier_Set | None):
        """Initialize the Sheet_Beyond_Gauge_Warning.

        Args:
            cur_carrier_set (Yarn_Carrier_Set | None): The current carrier that will be cut because no carrier set was specified.
        """
        message = "No carrier specified and no carrier is active. Cut is a No-Op" if cur_carrier_set is None else f"No carrier specified to cut, so cutting active carrier set {cur_carrier_set}"
        super().__init__(message)


class Breakpoint_Condition_Error_Ignored_Warning(Knit_Script_Warning):
    """
    Warning raised when a breakpoint condition is ignored.
    """

    def __init__(self, condition_error: BaseException, line_number: int) -> None:
        self.error: BaseException = condition_error
        self.line: int = line_number
        super().__init__(f"Conditional Breakpoint at Line {line_number} triggered Error:\n{condition_error}")


class Repeated_Needle_Warning(Knit_Script_Warning):
    """Warning raised when a carriage pass would require passing over the same needle more than once.

    This exception prevents machine operations that would attempt to work on the same needle multiple times within a single carriage pass, which is not physically possible on most knitting machines.

    Attributes:
        needle (Needle): The needle that would be worked on multiple times.
    """

    def __init__(self, needle: Needle):
        """Initialize the Repeated_Needle_Exception.

        Args:
            needle (Needle): The needle that would be worked on multiple times.
        """
        self.needle = needle
        super().__init__(f"Cannot work on {self.needle} more than once in a carriage pass.\n\tThis needle was skipped after its first use.")


class Unspecified_Carrier_Warning(Knit_Script_Warning):
    """
    Warning raised when no carrier is specified for a directed carriage pass but a valid carrier could be inferred.
    """

    def __init__(self, carrier: Yarn_Carrier_Set):
        super().__init__(f"No Carrier is specified so working carrier is presumed to be active carrier {carrier} which most recently formed a loop")
