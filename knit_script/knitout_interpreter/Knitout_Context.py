from typing import Optional, List, Dict, Tuple

from knit_script.knitout_interpreter.knitout_errors.Knitout_Error import Ignorable_Knitout_Error
from knit_script.knitout_interpreter.knitout_structures.Carraige_Pass_Collection import Carriage_Pass_Collection
from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Version_Line, Comment_Line
from knit_script.knitout_interpreter.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.Pause_Instruction import Pause_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.carrier_instructions import Carrier_Instruction, Releasehook_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.needle_instructions import Knitout_Needle_Instruction
from knit_script.knitting_machine.Machine_State import Machine_State
from knit_script.knitting_machine.machine_components.yarn_management.Carrier import Carrier
from knit_script.knitting_machine.machine_specification.Header import Header


class Knitout_Context:

    def __init__(self):
        self._header: Header = Header()
        self.machine_state: Optional[Machine_State] = None
        self._executed_knitout: List[str] = []
        self.version_line: Optional[Version_Line] = None
        self.executed_header: List[Header_Declaration] = []
        self.executed_instructions: List[Instruction] = []
        self.carriage_passes: List[Carriage_Pass_Collection] = []
        self.carrier_instructions: Dict[Carrier: List[Instruction]] = {}
        self.carrier_management_instructions: Dict[Carrier: List[Carrier_Instruction]] = {}
        self.ignored_instructions: List[Comment_Line] = []

    @property
    def last_carriage_pass(self) -> Optional[Carriage_Pass_Collection]:
        if len(self.carriage_passes) == 0:
            return None
        return self.carriage_passes[-1]

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

    def _add_carrier_instruction(self, instruction: Knitout_Needle_Instruction | Carrier_Instruction):
        for carrier in instruction.carrier_set.get_carriers(self.machine_state.carrier_system):
            self.carrier_instructions[carrier].append(instruction)

    def _add_carrier_management_instruction(self, instruction: Knitout_Needle_Instruction | Carrier_Instruction):
        for carrier in instruction.carrier_set.get_carriers(self.machine_state.carrier_system):
            self.carrier_management_instructions[carrier].append(instruction)

    def execute_instructions(self, instructions: List[Instruction]) -> List[Comment_Line]:
        self.machine_state = self._header.machine_state()
        self.carrier_instructions = {c: [] for c in self.machine_state.carrier_system.carriers.values()}
        self.carrier_management_instructions = {c: [] for c in self.machine_state.carrier_system.carriers.values()}
        prior_instruction = None
        first_lines_commented = []
        active_carriage_pass = None
        for instruction in instructions:
            try:
                instruction.execute(self.machine_state)
                self.executed_instructions.append(instruction)
                if isinstance(instruction, Carrier_Instruction):
                    if not isinstance(instruction, Releasehook_Instruction):  # release hook is free floating of other operations
                        self._add_carrier_instruction(instruction)
                    self._add_carrier_management_instruction(instruction)
                if isinstance(instruction, Knitout_Needle_Instruction):
                    if active_carriage_pass is None:  # first in carriage pass
                        active_carriage_pass = Carriage_Pass_Collection(instruction, self.machine_state.racking)
                    else:
                        if active_carriage_pass.can_add_to_pass(instruction):  # add to current pass
                            active_carriage_pass.add_to_pass(instruction)
                        else:  # break and make a new pass
                            self.carriage_passes.append(active_carriage_pass)
                            active_carriage_pass = Carriage_Pass_Collection(instruction, self.machine_state.racking)
                    if instruction.carrier_set is not None:
                        self._add_carrier_instruction(instruction)
                elif active_carriage_pass is not None and not isinstance(instruction, Pause_Instruction):  # another operation might stop carriage pass.  pauses don't effect carriage pass
                    self.carriage_passes.append(active_carriage_pass)
                    active_carriage_pass = None
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
