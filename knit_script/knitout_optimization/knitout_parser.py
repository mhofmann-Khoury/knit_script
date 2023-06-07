"""Parser code for accessing Parglare language support"""
from typing import Tuple, Dict, List, Optional

from parglare import Parser, Grammar
from parglare.parser import LRStackNode
from pkg_resources import resource_stream

from knit_script.knitout_optimization.knitout_actions import action
from knit_script.knitout_optimization.knitout_comment_actions import comment_action
from knit_script.knitout_optimization.knitout_structures.Knitout_Line import Knitout_Line, Comment_Line, Version_Line
from knit_script.knitout_optimization.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitout_optimization.knitout_structures.knitout_instructions.instruction import Instruction


class Knitout_Parser:
    """
        Parser for reading knitout using the parglare library
    """

    def __init__(self, debug_grammar: bool = False, debug_parser: bool = False, debug_parser_layout: bool = False):
        self.in_line_comments_start_position = None
        self.lines_of_code: List[Knitout_Line] = []
        self.comments_by_line: Dict[int: str] = {}
        self.held_comments: List[Comment_Line] = []
        pg_resource_stream = resource_stream("knit_script", "knitout_optimization/knitout.pg")
        self._grammar: Grammar = Grammar.from_file(pg_resource_stream.name, debug=debug_grammar, ignore_case=True)
        self._set_parser(debug_parser, debug_parser_layout)

    def _set_parser(self, debug_parser: bool, debug_parser_layout: bool):
        self._parser: Parser = Parser(self._grammar, debug=debug_parser, debug_layout=debug_parser_layout, actions=action.all, layout_actions=comment_action.all)
        self._parser.knitout_parser = self  # make this structure available from actions
        self._parser.layout_parser.parent_parser = self._parser  # makes the main parser accessible from actions
        self._parser.layout_parser.knitout_parser = self  # make this structure accessible from actions
        self.lines_of_code: List[Knitout_Line] = []
        self.comments_by_line: Dict[int: str] = {}
        self.in_line_comments_start_position: Optional[Tuple[int, Comment_Line]] = None
        self.held_comments: List[Comment_Line] = []

    def add_code_line(self, line: Knitout_Line):
        """
        Adds the line of code and records the comment
        :param line: line of code to add to end
        """
        self.lines_of_code.append(line)
        if line.has_comment:
            last_line, _ = self.last_line_of_code
            self.comments_by_line[last_line] = line.comment

    def associate_with_comment(self, stack_node: LRStackNode) -> Optional[str]:
        """

        :param stack_node:
        :return:
        """
        if self.in_line_comments_start_position is None:
            return None
        start_pos = self.in_line_comments_start_position[0]
        comment = self.in_line_comments_start_position[1]
        assert stack_node.start_position == start_pos, f"Comment's parent line not found: {comment} at {start_pos}"
        self.in_line_comments_start_position = None
        return comment.comment

    @property
    def last_line_of_code(self) -> Tuple[int, Optional[Knitout_Line]]:
        """
        :return: line number and string of last line of code parsed
        """
        if len(self.lines_of_code) == 0:
            return 0, None
        return len(self.lines_of_code) - 1, self.lines_of_code[-1]

    def parse(self, pattern: str, pattern_is_file: bool = False, reset_parser: bool = True, debug_parser: bool = False, debug_parser_layout: bool = False) -> \
            Tuple[Version_Line, List[Header_Declaration], List[Instruction], List[Knitout_Line], Dict[int, str]]:
        """
        Executes the parsing code for the parglare parser
        :param debug_parser_layout: prints comment debugging
        :param debug_parser: prints grammar debugging
        :param reset_parser: resets parser to have no prior input
        :param pattern: Either a file or the knitout string to be parsed
        :param pattern_is_file: if true, assumes that the pattern is parsed from a file
        :return: version, header, instructions
        """
        if reset_parser:
            self._set_parser(debug_parser, debug_parser_layout)
        if pattern_is_file:
            version, head, instructions = self._parser.parse_file(pattern)
        else:
            version, head, instructions = self._parser.parse(pattern)

        return version, head, instructions, self.lines_of_code, self.comments_by_line
