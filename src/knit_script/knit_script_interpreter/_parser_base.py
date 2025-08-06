"""Module containing the Parser_Base Class.

This module provides the _Parser_Base class, which serves as an abstract base class for KnitScript parsers.
It provides a common interface for parsing operations while abstracting the underlying parglare parser implementation details.
The class handles the conversion from parglare ParseError exceptions to KnitScript-specific Parsing_Exception instances for consistent error handling across the system.
"""
from typing import Any, cast

from parglare import Parser, Grammar, ParseError

from knit_script.knit_script_exceptions.parsing_exception import Parsing_Exception


class _Parser_Base:
    """Abstract Base class for Knitscript Parser.

    Used to separate circular import of knitscript parsing action and use of the parser in the import expression.
    This class provides a standardized interface for parsing knit script code while encapsulating the parglare parser implementation details.

    The _Parser_Base class manages the grammar and parser instances, provides parsing methods for both string and file inputs,
    and handles error conversion from parglare's internal exceptions to KnitScript-specific exceptions for consistent error handling throughout the system.

    Attributes:
        _grammar (Grammar): The parglare grammar used for parsing knit script syntax.
        _parser (Parser): The parglare parser instance configured with the grammar and actions.
    """

    def __init__(self, grammar: Grammar, parser: Parser):
        """Initialize the parser base with grammar and parser instances.

        Args:
            grammar (Grammar): The grammar for parsing knit script syntax, typically loaded from a grammar file.
            parser (Parser): The parser instance configured with the grammar, debug settings, and action handlers.
        """
        self._grammar = grammar
        self._parser = parser

    def parse(self, pattern: str, pattern_is_file: bool = False) -> list[Any]:
        """Execute the parsing code for the parglare parser.

        Parses the provided knit script code or file and returns the resulting abstract syntax tree. Handles both string-based parsing and file-based parsing based on the pattern_is_file parameter.

        Args:
            pattern (str): Either a file path or the knit script string to be parsed, depending on the pattern_is_file parameter.
            pattern_is_file (bool, optional): If True, treats pattern as a file path and reads the content from that file.
            If False, treats pattern as the actual knit script code to parse. Defaults to False.

        Returns:
            list[Any]: List of statements parsed from the input, representing the abstract syntax tree of the knit script program.

        Raises:
            Parsing_Exception: If parsing fails due to syntax errors or other parsing issues. This wraps the original parglare ParseError with additional KnitScript-specific context and formatting.
        """
        try:
            if pattern_is_file:
                return cast(list[Any], self._parser.parse_file(pattern))
            else:
                return cast(list[Any], self._parser.parse(pattern))
        except ParseError as e:
            raise Parsing_Exception(e)
