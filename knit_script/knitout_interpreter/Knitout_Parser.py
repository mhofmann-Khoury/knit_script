"""Parser code for accessing Parglare language support"""
import re

import importlib_resources
import parglare.exceptions
from parglare import Parser, Grammar

import knit_script
from knit_script.knitout_interpreter.knitout_actions import action
from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Knitout_Line, Version_Line
from knit_script.knitout_interpreter.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction


class Knitout_Parser:
    """
        Parser for reading knitout using the parglare library
    """

    def __init__(self, debug_grammar: bool = False, debug_parser: bool = False, debug_parser_layout: bool = False):
        pg_resource_stream = importlib_resources.files(knit_script.knitout_interpreter).joinpath('knitout.pg')
        self._grammar: Grammar = Grammar.from_file(pg_resource_stream, debug=debug_grammar, ignore_case=True)
        self._set_parser(debug_parser, debug_parser_layout)

    def _set_parser(self, debug_parser: bool, debug_parser_layout: bool):
        self._parser: Parser = Parser(self._grammar, debug=debug_parser, debug_layout=debug_parser_layout, actions=action.all)
        self._parser.knitout_parser = self  # make this structure available from actions

    def parse(self, pattern: str, pattern_is_file: bool = False, reset_parser: bool = True, debug_parser: bool = False, debug_parser_layout: bool = False) -> \
            tuple[Version_Line, list[Header_Declaration], list[Instruction], list[Knitout_Line], list[Knitout_Line]]:
        """
        Executes the parsing code for the parglare parser
        :param debug_parser_layout: prints comment debugging
        :param debug_parser: prints grammar debugging
        :param reset_parser: resets parser to have no prior input
        :param pattern: Either a file or the knitout string to be parsed
        :param pattern_is_file: if true, assumes that the pattern is parsed from a file
        :return: version, header, instructions
        """
        version = Version_Line(-1)
        head = []
        instructions = []
        comments = []
        codes = []
        if reset_parser:
            self._set_parser(debug_parser, debug_parser_layout)
        if pattern_is_file:
            with open(pattern, "r") as pattern_file:
                lines = pattern_file.readlines()
        else:
            lines = pattern.splitlines()
        for i, line in enumerate(lines):
            if not re.match(r'^\s*$', line):
                try:
                    code = self._parser.parse(line)
                except parglare.exceptions.ParseError as e:
                    print(f"Parser Error on {i}: {line}")
                    raise e
                if code is None:
                    continue
                else:
                    assert isinstance(code, Knitout_Line)
                    code.original_line_number = i
                    codes.append(code)
                if isinstance(code, Version_Line):
                    assert version == code.version or version.version < 0, f"Cannot have multiple versions of knitout {version} and {code}"
                    version = code
                elif isinstance(code, Header_Declaration):
                    head.append(code)
                elif isinstance(code, Instruction):
                    instructions.append(code)
                else:
                    comments.append(code)
        if version.version < 0:
            version = Version_Line(2, "Version defaulted to 2")
        return version, head, instructions, codes, comments
