"""Parser code for accessing Parglare language support"""
from __future__ import annotations

import importlib_resources
from parglare import Parser, Grammar

import knit_script
from knit_script.knit_script_interpreter.knit_script_actions import action
from knit_script.knit_script_interpreter.parser_base import _Parser_Base


class Knit_Script_Parser(_Parser_Base):
    """Parser for reading knit script files using parglare library."""

    def __init__(self, debug_grammar: bool = False, debug_parser: bool = False, debug_parser_layout: bool = False):
        """Initializes the knit script parser.

        Args:
            debug_grammar: Will provide full parglare output for grammar states
            debug_parser: Will provide full parglare output for parsed file shift reduce status
            debug_parser_layout: Will provide layout information from parser
        """
        pg_resource_stream = importlib_resources.files(knit_script.knit_script_interpreter).joinpath('knit_script.pg')
        grammar = Grammar.from_file(pg_resource_stream, debug=debug_grammar, ignore_case=True)
        super().__init__(grammar=grammar,
                         parser=Parser(grammar, debug=debug_parser, debug_layout=debug_parser_layout, actions=action.all))
