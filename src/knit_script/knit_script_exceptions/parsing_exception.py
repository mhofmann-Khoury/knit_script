"""Module containing parsing exception class."""
from __future__ import annotations

from parglare import ParseError
from parglare.common import Location, position_context

from knit_script.knit_script_exceptions.Knit_Script_Exception import Knit_Script_Exception


class Parsing_Exception(Knit_Script_Exception):
    """Exception raised when there is an error parsing KnitScript code."""

    def __init__(self, parglare_parse_error: ParseError) -> None:
        """Initialize the Parsing_Exception.

        Args:
            parglare_parse_error (ParseError): The original ParseError from the parglare parser.
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
