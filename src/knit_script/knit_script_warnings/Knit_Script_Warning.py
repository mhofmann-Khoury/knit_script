"""A module containing the base class for Knitting Script warnings.

This module provides the base warning class and specific warning types for the KnitScript programming language.
These warnings alert developers to potentially problematic code patterns, configuration issues, and situations that may lead to unexpected behavior without causing program termination.
The warning system helps developers write more robust knit script programs by identifying common pitfalls and questionable practices during execution.
"""
from parglare.common import Location
from virtual_knitting_machine.machine_components.needles.Sheet_Identifier import (
    Sheet_Identifier,
)

from knit_script.knit_script_interpreter.ks_element import KS_Element


class Knit_Script_Warning(RuntimeWarning):
    """Base class for warnings caused by error-prone code in Knit Script.

    The Knit_Script_Warning class serves as the foundation for all warning types in the KnitScript programming language.
    It extends Python's RuntimeWarning to provide KnitScript-specific warning behavior and consistent message formatting.
    All specific KnitScript warning types inherit from this class, creating a hierarchical warning system that allows for both specific and general warning handling patterns.

    This base class automatically prefixes warning messages with "KnitScript Warning:" to clearly identify KnitScript-related warnings and distinguish them from other system warnings.
    The warning system is designed to help developers identify potentially problematic code without stopping program execution.

    Attributes:
        message (str): The formatted warning message including the KnitScript warning prefix.
    """

    def __init__(self, message: str, ks_element: KS_Element | None):
        """Initialize the Knit_Script_Warning.

        Creates a new KnitScript warning with the provided message. The message is automatically formatted with a KnitScript warning prefix and newline formatting for consistent warning display.

        Args:
            ks_element (KS_Element | None): The KnitScript element that triggered the warning. Used to identify the location in the knitscript code.
            message (str): The warning message to display. This will be prefixed with "KnitScript Warning:" in the final formatted message.
        """
        self._ks_element: KS_Element | None = ks_element
        self.message = message
        super().__init__(self.full_message)

    @property
    def full_message(self) -> str:
        """
        Returns:
            str: The full warning including the prefix and message.
        """
        return f"{self.prefix}: {self.message}"

    @property
    def prefix(self) -> str:
        """
        Returns:
            str: The prefix of the warning message based on the name of the warning and if the ks_element that triggered it is known.
        """
        prefix = f"\n{self.__class__.__name__}"
        if self.ks_element is not None:
            error_location: Location = self.ks_element.location
            if error_location.file_name is not None:
                prefix += f" (File {error_location.file_name} on line {error_location.line})"
            else:
                prefix += f" (Line {error_location.line})"
        return prefix

    @property
    def ks_element(self) -> KS_Element | None:
        """
        Returns:
            None | KS_Element: The element that triggered this warning, or None if that was not known.
        """
        return self._ks_element

    @ks_element.setter
    def ks_element(self, element: KS_Element) -> None:
        self._ks_element = element


class Shadow_Variable_Warning(Knit_Script_Warning):
    """Warning raised when a variable shadows another variable in an outer scope.

    This warning is issued when a variable is defined in a local scope that has the same name as a variable in an outer scope, potentially hiding the outer variable and causing confusion.
    Variable shadowing can lead to unexpected behavior when developers intend to access the outer variable but inadvertently access the inner one instead.

    Attributes:
        variable_name (str): The variable that shadows a higher scope.
    """

    def __init__(self, variable_name: str, ks_element: KS_Element | None = None):
        """Initialize the Shadow_Variable_Warning.

        Args:
            ks_element (KS_Element | None): The KnitScript element that triggered the warning. Used to identify the location in the knitscript code.
            variable_name (str): The name of the variable that is shadowing another variable in an outer scope.
        """
        self.variable_name: str = variable_name
        super().__init__(f"Variable <{variable_name}> shadows a variable in the outer scope.", ks_element)


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
        super().__init__(f"Gauge of {gauge} is greater than current sheet {sheet} so sheet is set to {gauge - 1}", None)
