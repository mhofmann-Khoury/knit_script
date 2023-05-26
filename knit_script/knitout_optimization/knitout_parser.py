"""Parser code for accessing Parglare language support"""
from typing import Tuple

from parglare import Parser, Grammar
from pkg_resources import resource_stream

from knit_script.knitout_optimization.knitout_actions import action


class Knitout_Parser:
    """
        Parser for reading knitout using the parglare library
    """

    def __init__(self, debug_grammar: bool = False, debug_parser: bool = False, debug_parser_layout: bool = False):
        pg_resource_stream = resource_stream("knit_script", "knitout_optimization/knitout.pg")
        self._grammar: Grammar = Grammar.from_file(pg_resource_stream.name, debug=debug_grammar, ignore_case=True)
        self._parser: Parser = Parser(self._grammar, debug=debug_parser, debug_layout=debug_parser_layout, actions=action.all)

    def parse(self, pattern: str, pattern_is_file: bool = False) -> Tuple[int, list, list]:
        """
        Executes the parsing code for the parglare parser
        :param pattern: either a file or the knitout string to be parsed
        :param pattern_is_file: if true, assumes that the pattern is parsed from a file
        :return: version, header, instructions
        """
        if pattern_is_file:
            return self._parser.parse_file(pattern)
        else:
            return self._parser.parse(pattern)
