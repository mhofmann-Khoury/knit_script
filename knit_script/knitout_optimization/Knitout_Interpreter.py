from typing import Tuple, List, Dict, Optional

from knit_script.knitout_optimization.knitout_parser import Knitout_Parser
from knit_script.knitout_optimization.knitout_structures.Knitout_Line import Version_Line, Knitout_Line
from knit_script.knitout_optimization.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitout_optimization.knitout_structures.knitout_instructions.instruction import Instruction
from knit_script.knitting_machine.Machine_State import Machine_State


class Knitout_Interpreter:
    """
        Interpreter for processing in writing knitout
    """

    def __init__(self, debug_grammar: bool = False, debug_parser: bool = False, debug_parser_layout: bool = False):
        self._parser = Knitout_Parser(debug_grammar, debug_parser, debug_parser_layout)
        self._machine_state: Optional[Machine_State] = None

    def parse_knitout(self, pattern: str, pattern_is_file: bool = True) -> Tuple[Version_Line, List[Header_Declaration], List[Instruction], List[Knitout_Line], Dict[int, str]]:
        """
        :param pattern: knitout pattern
        :param pattern_is_file: true if the pattern is in a file
        :return: the parsing results of the knitout pattern
        """
        return self._parser.parse(pattern, pattern_is_file=pattern_is_file)

    def write_trimmed_knitout(self, pattern: str, out_file: str, pattern_is_file: bool = True):
        """
        Outputs knitout trimmed of whitespace and comments.
        :param pattern: Knitout pattern
        :param out_file: file to output to
        :param pattern_is_file: true if the pattern is a filename
        """
        v, header, instructions, codes_by_line, comments = self.parse_knitout(pattern, pattern_is_file)
        lines = []
        for line, instruction in codes_by_line:
            if not isinstance(instruction, int):
                line = str(instruction)
            index_last_semi = line.rfind(";")
            if index_last_semi >= 1:
                line = line[:index_last_semi]
            lines.append(line.strip()+"\n")

        with open(out_file, "w") as out:
            out.writelines(lines)
