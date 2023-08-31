from typing import List

from knit_script.knitout_interpreter.Knitout_Context import Knitout_Context
from knit_script.knitout_interpreter.Knitout_Parser import Knitout_Parser
from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Version_Line, Knitout_Line, Comment_Line
from knit_script.knitout_interpreter.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction


class Knitout_Interpreter:
    """
        Interpreter for processing in writing knitout
    """

    def __init__(self, debug_grammar: bool = False, debug_parser: bool = False, debug_parser_layout: bool = False):
        self._parser = Knitout_Parser(debug_grammar, debug_parser, debug_parser_layout)
        self.context = Knitout_Context()

    def _reset_context(self):
        self.context = Knitout_Context()

    def parse_knitout(self, pattern: str, pattern_is_file: bool = True) -> tuple[Version_Line, list[Header_Declaration], list[Instruction], list[Knitout_Line], list[Knitout_Line]]:
        """
        :param pattern: knitout pattern
        :param pattern_is_file: true if the pattern is in a file
        :return: the parsing results of the knitout pattern
        """
        return self._parser.parse(pattern, pattern_is_file=pattern_is_file)

    def interpret_knitout(self, pattern: str, pattern_is_file: bool = True, reset_context: bool = True) -> List[Knitout_Line]:
        """
        :param pattern: A pattern as a string or the filename of the knitout file.
        :param pattern_is_file: If true, it looks for the knitout pattern in pattern's file location.
        :param reset_context: If true, reset the context for the file. Starts a new parse.
        :return: List of knitout lines that make up the program
        """
        if reset_context:
            self._reset_context()
        version_line, header_declarations, instructions, knitout_by_lines, comments = self.parse_knitout(pattern, pattern_is_file)
        top_comments = []
        last_non_comment = None
        for line in knitout_by_lines:
            if not isinstance(line, Comment_Line):
                last_non_comment = line
            elif last_non_comment is None:
                top_comments.append(line)
            else:
                last_non_comment.follow_comments.append(line)
        first_headers_commented, first_instructions_commented = self.context.execute_knitout(version_line, header_declarations, instructions)
        organized_knitout = []
        organized_knitout.extend(top_comments)
        organized_knitout.append(version_line)
        organized_knitout.extend(version_line.follow_comments)
        organized_knitout.extend(first_headers_commented)
        for header_line in self.context.executed_header:
            organized_knitout.append(header_line)
            organized_knitout.extend(header_line.follow_comments)
        organized_knitout.extend(first_instructions_commented)
        for instruction in self.context.executed_instructions:
            organized_knitout.append(instruction)
            organized_knitout.extend(instruction.follow_comments)
        return organized_knitout

    def organize_knitout(self, pattern: str, out_file: str, pattern_is_file: bool = True, reset_context: bool = True):
        """
        :param pattern: pattern to organize
        :param out_file: file to output organized knitout
        :param pattern_is_file: true if the pattern is a filename
        :param reset_context: True if interpreter should reset
        """
        organized_knitout = self.interpret_knitout(pattern, pattern_is_file, reset_context)
        knitout_lines = [str(kl) for kl in organized_knitout]
        with open(out_file, "w", encoding="utf-8") as out:
            out.writelines(knitout_lines)

    def write_trimmed_knitout(self, pattern: str, out_file: str, pattern_is_file: bool = True):
        """
        Outputs knitout trimmed of whitespace and comments.
        :param pattern: Knitout pattern
        :param out_file: file to output to
        :param pattern_is_file: true if the pattern is a filename
        """
        v, header, instructions, codes_by_line, comments = self.parse_knitout(pattern, pattern_is_file)
        lines = []
        for line, instruction in enumerate(codes_by_line):
            if not isinstance(instruction, Comment_Line):
                line = str(instruction)
                if instruction.has_comment:
                    index_last_semi = line.rfind(";")
                    line = line[:index_last_semi]
                lines.append(line.strip() + "\n")

        with open(out_file, "w", encoding="utf-8") as out:
            out.writelines(lines)
