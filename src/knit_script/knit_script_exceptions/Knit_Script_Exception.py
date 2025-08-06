"""Module containing the base class for KnitScript exceptions.

This module provides the base exception classes for all KnitScript-related errors.
The Knit_Script_Exception class serves as the root of the exception hierarchy for the KnitScript programming language,
providing consistent error message formatting and serving as a common base for all specific exception types that can occur during knit script parsing, compilation, and execution.

The module also includes Knit_Script_Located_Exception for exceptions that can provide detailed location information from the parse tree.
"""
from parglare.common import Location, position_context

from knit_script.knit_script_interpreter.ks_element import KS_Element


class Knit_Script_Exception(Exception):
    """Superclass for all exceptions related to processing KnitScript programs.

    The Knit_Script_Exception class provides the foundation for all error handling in the KnitScript programming language.
    It extends Python's built-in Exception class with KnitScript-specific formatting and behavior,
    ensuring that all KnitScript errors have consistent message formatting and can be caught collectively when needed.

    This base class automatically prefixes error messages with "Knit Script Exception:" to clearly identify KnitScript-related errors and distinguish them from other system exceptions.
    All specific KnitScript exception types inherit from this class, creating a hierarchical exception system that allows for both specific and general error handling patterns.

    Attributes:
        message (str): The formatted error message including the KnitScript exception prefix.
    """

    def __init__(self, message: str):
        """Initialize the Knit_Script_Exception.

        Creates a new KnitScript exception with the provided error message.
        The message is automatically formatted with a KnitScript exception prefix and newline formatting for consistent error display.

        Args:
            message (str): The error message to display. This will be prefixed with "Knit Script Exception:" in the final formatted message.
        """
        self.message = f"\n{self.__class__.__name__}: {message}"
        super().__init__(self.message)


class Knit_Script_Located_Exception(Knit_Script_Exception):
    """Superclass for Knit-Script exceptions that can be located in a file by a given KS-Element from the parse tree.

    This class extends the base Knit_Script_Exception with location information extracted from parser elements.
    It provides detailed context about where in the source code the exception occurred, including file name, line number, and surrounding code context.
    This enhanced error reporting helps developers quickly identify and fix issues in their knit script programs.

    The located exception automatically formats location information and provides visual context showing the position where the error occurred within the source code.

    Attributes:
        ks_element (KS_Element): The KS_Element from the parse tree that caused the exception.
        error_location (Location): The location information for where the exception occurred.
        _location_message (str): Formatted location information including file and line number.
        _location_example (str): Code context showing the position where the error occurred.
    """

    def __init__(self, message: str | Exception, ks_element: KS_Element):
        """Initialize the Knit_Script_Located_Exception.

        Creates a new located KnitScript exception with enhanced location information extracted from the parser element.
        The exception includes detailed context about where the error occurred in the source code.

        Args:
            message (str | Exception): The error message to display or an existing exception to wrap with location information.
            ks_element (KS_Element): The KS_Element from the parse tree that caused the exception, providing location context.
        """
        self.ks_element = ks_element
        self.error_location: Location = self.ks_element.location
        if self.error_location.file_name is not None:
            self._location_message: str = f"File {self.error_location.file_name} on line {self.error_location.line}"
        else:
            self._location_message: str = f"Line {self.error_location.line}"
        self._location_example: str = position_context(self.error_location.input_str, self.error_location.start_position)
        message = f"({self._location_message} <{self._location_example}>): {message}"
        super().__init__(message)
