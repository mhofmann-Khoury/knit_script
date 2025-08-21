"""Module containing parsing exception class.

This module provides the Parsing_Exception class, which handles syntax and parsing errors that occur when processing KnitScript source code.
It wraps and enhances parglare ParseError objects with KnitScript-specific formatting and context information,
providing detailed location information, code context, and expected token information to help developers debug syntax errors in their knit script programs.
"""
from __future__ import annotations

from parglare import ParseError
from parglare.common import Location, position_context

from knit_script.knit_script_exceptions.Knit_Script_Exception import (
    Knit_Script_Exception,
)


class Parsing_Exception(Knit_Script_Exception):
    """Exception raised when there is an error parsing KnitScript code.

    The Parsing_Exception class provides enhanced error reporting for syntax errors in KnitScript source code.
    It wraps parglare ParseError objects and extracts detailed location information, code context, and expected token information
    to create comprehensive error messages that help developers identify and fix syntax issues.

    This exception provides formatted error messages that include the file name (if available), line number, a visual representation of the error location within the source code,
    and information about what tokens the parser was expecting at the point of failure.

    Attributes:
        parse_error (ParseError): The original ParseError from the parglare parser.
        error_location (Location): The location information for where the parsing error occurred.
        _location_message (str): Formatted location information including file and line number.
        _location_example (str): Code context showing the position where the error occurred.
        _expected (str): Formatted list of expected tokens at the error position.
    """

    def __init__(self, parglare_parse_error: ParseError) -> None:
        """Initialize the Parsing_Exception.

        Creates a new parsing exception from a parglare ParseError, extracting location information and formatting a comprehensive error message with context and expected token information.

        Args:
            parglare_parse_error (ParseError): The original ParseError from the parglare parser containing the raw parsing failure information.
        """
        self.parse_error: ParseError = parglare_parse_error
        self.error_location: Location = self.parse_error.location
        self._location_message: str = ""
        if self.error_location.file_name is not None:
            self._location_message += f" in File {self.error_location.file_name}"
        self._location_message += f" on line {self.error_location.line}"
        self._location_example: str = position_context(self.error_location.input_str, self.error_location.start_position)
        self._expected: str = f"Expected: {[t.name for t in self.parse_error.symbols_expected]}"
        super().__init__(f"Parsing Error{self._location_message}\n\t{self._location_example}\n\t{self._expected}")
