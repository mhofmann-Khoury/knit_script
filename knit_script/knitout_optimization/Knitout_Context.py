from typing import Optional, List, Dict, Tuple

from knit_script.knitout_optimization.knitout_errors.Knitout_Error import Ignorable_Knitout_Error
from knit_script.knitout_optimization.knitout_structures.Knitout_Line import Version_Line, Comment_Line
from knit_script.knitout_optimization.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitout_optimization.knitout_structures.knitout_instructions.carrier_instructions import Carrier_Instruction
from knit_script.knitout_optimization.knitout_structures.knitout_instructions.instruction import Instruction
from knit_script.knitting_machine.Machine_State import Machine_State
from knit_script.knitting_machine.machine_components.yarn_management.Carrier import Carrier
from knit_script.knitting_machine.machine_specification.Header import Header


class Knitout_Context:

    def __init__(self):
        self._header: Header = Header()
        self._machine_state: Optional[Machine_State] = None
        self._executed_knitout: List[str] = []
        self.version_line: Optional[Version_Line] = None
        self.executed_header: List[Header_Declaration] = []
        self.executed_instructions: List[Instruction] = []
        self.carrier_instructions: Dict[Carrier: List[Instruction]] = {}
        self.ignored_instructions: List[Comment_Line] = []

    @property
    def version(self) -> int:
        if self.version_line is not None:
            return self.version_line.version
        else:
            return 2

    def add_version(self, version_line: Version_Line):
        self.version_line = version_line

    def execute_header(self, header_declarations: List[Header_Declaration]) -> List[Comment_Line]:
        last_executed = None
        first_lines_commented = []
        for hd in header_declarations:
            caused_update = self._header.update_by_declaration(hd)
            if caused_update:
                self.executed_header.append(hd)
                last_executed = hd
            else:
                commented_header = Comment_Line(f"\t Header Not updated, so line is commented\n\t{hd}")
                if last_executed is None:
                    first_lines_commented.append(commented_header)
                else:
                    last_executed.add_follow_comment(commented_header)
        return first_lines_commented

    def execute_instructions(self, instructions: List[Instruction]) -> List[Comment_Line]:
        self._machine_state = self._header.machine_state()
        prior_instruction = None
        first_lines_commented = []
        for instruction in instructions:
            try:
                instruction.execute(self._machine_state)
                self.executed_instructions.append(instruction)
                if isinstance(instruction, Carrier_Instruction):
                    for cid in instruction.cs:
                        self.carrier_instructions[self._machine_state.carrier_system[cid]] = instruction
            except Ignorable_Knitout_Error as e:
                print(fr"""Knitout Warning for Knitout Line {instruction.original_line_number}
                Instruction raised Knitout Error: {e.message}
                Instruction commented out to recover Knitout Program.""")
                commented_instruction = Comment_Line(f"\t{e.message}\n\t;{instruction}")
                commented_instruction.original_line_number = instruction.original_line_number
                self.ignored_instructions.append(commented_instruction)
                if prior_instruction is None:
                    first_lines_commented.append(commented_instruction)
                else:
                    prior_instruction.follow_comments.append(commented_instruction)
            prior_instruction = instruction
        return first_lines_commented

    def execute_knitout(self, version_line: Version_Line, header_declarations: List[Header_Declaration], instructions: List[Instruction]) -> Tuple[List[Comment_Line], List[Comment_Line]]:
        self.add_version(version_line)
        first_header_comments = self.execute_header(header_declarations)
        first_instruction_comments = self.execute_instructions(instructions)
        return first_header_comments, first_instruction_comments
