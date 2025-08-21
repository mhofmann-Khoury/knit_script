"""Parser code for accessing Parglare language support.

This module provides the Knit_Script_Parser class, which implements the concrete parser for knit script files using the parglare parsing library.
It handles grammar loading, parser configuration, and provides debugging capabilities for grammar and parsing operations.
"""
from __future__ import annotations

from typing import cast

import importlib_resources
from parglare import Grammar, ParseError, Parser

import knit_script
from knit_script.knit_script_exceptions.parsing_exception import Parsing_Exception
from knit_script.knit_script_interpreter.knit_script_actions import action
from knit_script.knit_script_interpreter.statements.Statement import Statement


class Knit_Script_Parser:
    """Parser for reading knit script files using parglare library.

    The Knit_Script_Parser class provides the concrete implementation of knit script parsing using the parglare parsing framework.
    It loads the knit script grammar from resources, configures the parser with appropriate actions, and provides debugging capabilities for grammar development and troubleshooting parsing issues.

    This parser supports comprehensive debugging options including grammar state visualization, shift-reduce operation tracking, and layout information display.
     The parser integrates with the knit script action system to convert parsed syntax trees into executable knit script elements.
    """

    def __init__(self, debug_grammar: bool = False, debug_parser: bool = False, debug_parser_layout: bool = False):
        """Initialize the knit script parser with debugging options.

        Loads the knit script grammar from package resources and creates a configured parglare parser instance with the specified debugging settings and action handlers.

        Args:
            debug_grammar (bool, optional): If True, provides full parglare output for grammar states during parsing. Useful for debugging grammar definitions and conflicts. Defaults to False.
            debug_parser (bool, optional): If True, provides full parglare output for parsed file shift-reduce status. Useful for debugging parsing operations and understanding parser behavior.
            Defaults to False.
            debug_parser_layout (bool, optional): If True, provides layout information from parser including whitespace and indentation handling. Useful for debugging layout-sensitive parsing issues.
            Defaults to False.
        """
        pg_resource_stream = importlib_resources.files(knit_script.knit_script_interpreter).joinpath('knit_script.pg')
        self._grammar = Grammar.from_file(pg_resource_stream, debug=debug_grammar, ignore_case=True)
        self._parser = Parser(self._grammar, debug=debug_parser, debug_layout=debug_parser_layout, actions=action.all)

    def parse(self, pattern: str, pattern_is_file: bool = False) -> list[Statement]:
        """Execute the parsing code for the parglare parser.

        Parses the provided knit script code or file and returns the resulting abstract syntax tree. Handles both string-based parsing and file-based parsing based on the pattern_is_file parameter.

        Args:
            pattern (str): Either a file path or the knit script string to be parsed, depending on the pattern_is_file parameter.
            pattern_is_file (bool, optional): If True, treats pattern as a file path and reads the content from that file.
            If False, treats pattern as the actual knit script code to parse. Defaults to False.

        Returns:
            list[Statement]: List of statements parsed from the input, representing the abstract syntax tree of the knit script program.

        Raises:
            Parsing_Exception: If parsing fails due to syntax errors or other parsing issues. This wraps the original parglare ParseError with additional KnitScript-specific context and formatting.
        """
        try:
            if pattern_is_file:
                return cast(list[Statement], self._parser.parse_file(pattern))
            else:
                parse_results = self._parser.parse(pattern)
                return cast(list[Statement], parse_results)
        except ParseError as e:
            raise Parsing_Exception(e)
