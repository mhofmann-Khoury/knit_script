from typing import Any, cast

from parglare import Parser, Grammar, ParseError

from knit_script.knit_script_exceptions.parsing_exception import Parsing_Exception


class Parser_Base:
    """Abstract Base class for Knitscript Parser.

    Used to separate circular import of knitscript parsing action and use of the
    parser in the import expression.
    """

    def __init__(self, grammar: Grammar, parser: Parser):
        """Initializes the parser base.

        Args:
            grammar: The grammar for parsing
            parser: The parser instance
        """
        self._grammar = grammar
        self._parser = parser

    def parse(self, pattern: str, pattern_is_file: bool = False) -> list[Any]:
        """Executes the parsing code for the parglare parser.

        Args:
            pattern: Either a file or the knit script string to be parsed
            pattern_is_file: If true, assumes that the pattern is parsed from a file

        Returns:
            List of statements parsed from file

        Raises:
            Parsing_Exception: If parsing fails
        """
        try:
            if pattern_is_file:
                return cast(list[Any], self._parser.parse_file(pattern))
            else:
                return cast(list[Any], self._parser.parse(pattern))
        except ParseError as e:
            raise Parsing_Exception(e)
