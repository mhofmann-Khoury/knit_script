"""Parser code for accessing Parglare language support"""
import importlib_resources
from parglare import Parser, Grammar

import knit_script
from knit_script.knit_script_interpreter.knit_script_actions import action


class Knit_Script_Parser:
    """
        Parser for reading knit script files using parglare library
    """

    def __init__(self, debug_grammar: bool = False, debug_parser: bool = False, debug_parser_layout: bool = False):

        pg_resource_stream = importlib_resources.files(knit_script.knit_script_interpreter).joinpath('knit_script.pg')
        self._grammar: Grammar = Grammar.from_file(pg_resource_stream, debug=debug_grammar, ignore_case=True)
        self._parser: Parser = Parser(self._grammar, debug=debug_parser, debug_layout=debug_parser_layout, actions=action.all)

    def parse(self, pattern: str, pattern_is_file: bool = False) -> list:
        """
        Executes the parsing code for the parglare parser
        :param pattern: either a file or the knit script string to be parsed
        :param pattern_is_file: if true, assumes that the pattern is parsed from a file
        :return: List of statements parsed from file
        """
        if pattern_is_file:
            return self._parser.parse_file(pattern)
        else:
            return self._parser.parse(pattern)
