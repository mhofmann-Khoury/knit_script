import os
from typing import Tuple

from parglare import Parser, Grammar

from knit_script.knit_script_interpreter.knit_script_actions import action



class Knit_Script_Parser:
    """
        Parser for reading knitscript using parglare librare
    """
    def __init__(self, debug_grammar: bool = False, debug_parser: bool = False, debug_parser_layout: bool = False):
        pg_loc = os.path.join(os.path.dirname(__file__), 'knit_script.pg')
        self._grammar:Grammar = Grammar.from_file(pg_loc, debug=debug_grammar, ignore_case=True)
        self._parser: Parser = Parser(self._grammar, debug=debug_parser, debug_layout=debug_parser_layout, actions=action.all)

    def parse(self, pattern: str, pattern_is_file: bool = False) -> Tuple[list, list]:
        """
        Executes the parsing code for the parglare parser
        :param pattern: either a file or the knitspeak string to be parsed
        :param pattern_is_file: if true, assumes that the pattern is parsed from a file
        :return:
        """
        if pattern_is_file:
            return self._parser.parse_file(pattern)
        else:
            return self._parser.parse(pattern)