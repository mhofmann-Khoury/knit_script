from typing import List, Dict, Optional

import networkx
from networkx import DiGraph

from knit_script.knitout_interpreter.Knitout_Context import Knitout_Context
from knit_script.knitout_interpreter.knitout_structures.Carraige_Pass_Collection import Carriage_Pass_Collection
from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Knitout_Line
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.carrier_instructions import Inhook_Instruction, Releasehook_Instruction, Carrier_Instruction, Hook_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.needle_instructions import Knitout_Needle_Instruction, Loop_Making_Instruction, Xfer_Instruction, Split_Instruction
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction


class Knitout_Topology_Graph:

    def __init__(self, context: Knitout_Context, min_loops_before_release_hook=10):
        self._min_loops_before_release_hook = min_loops_before_release_hook
        self.context = context
        self.instruction_graph: DiGraph = DiGraph()
        self.carriage_pass_graph: DiGraph = DiGraph()
        for cp1, cp2 in zip(self.context.carriage_passes[:-1], self.context.carriage_passes[1:]):
            self.carriage_pass_graph.add_edge(cp1, cp2)
        self._inhook_releasehook_pairs: Dict[Inhook_Instruction: Releasehook_Instruction] = {}
        self._inhook_directions: Dict[Inhook_Instruction: Pass_Direction] = {}
        self._inhook_next_pass: Dict[Inhook_Instruction: Carriage_Pass_Collection] = {}
        self.add_loop_connections()
        self.add_yarn_connections()
        self.add_between_pass_instructions()
        self.connect_releasehook_instructions()
        self.update_carriage_pass_directions()

    def add_between_pass_instructions(self):
        last_non_cp_instructions = []
        current_passes = {}  # used as a set
        started_pass = False
        last_hook_instruction = None
        last_releasehook = None
        for instruction in self.context.executed_instructions:
            if isinstance(instruction, Knitout_Needle_Instruction):  # in a carriage pass
                started_pass = True
                for prior in last_non_cp_instructions:
                    self.instruction_graph.add_edge(prior, instruction, is_carriage_pass_set_up=True)
                    current_passes[instruction] = instruction
                if last_releasehook is not None and (isinstance(instruction, Xfer_Instruction) or isinstance(instruction, Split_Instruction)):
                    self.instruction_graph.add_edge(last_releasehook, instruction, is_releasehook_edge=True, carrier_set=last_releasehook.carrier_set)
            elif isinstance(instruction, Hook_Instruction):
                if last_hook_instruction is not None:
                    self.instruction_graph.add_edge(last_hook_instruction, instruction, is_hook_edge=True)
                last_hook_instruction = instruction
                if isinstance(instruction, Releasehook_Instruction):
                    last_releasehook = instruction
            elif not isinstance(instruction, Carrier_Instruction):  # Don't place carrier operations
                if started_pass:  # reset instructions since last pass
                    last_non_cp_instructions = []
                started_pass = False
                last_non_cp_instructions.append(instruction)

    def get_next_carriage_pass(self, carriage_pass: Knitout_Needle_Instruction | Carriage_Pass_Collection) -> Optional[Carriage_Pass_Collection]:
        """
        :param carriage_pass: carriage pass or an instruction in a carriage passes
        :return: the following carriage pass or None if last pass
        """
        if isinstance(carriage_pass, Knitout_Needle_Instruction):
            carriage_pass = carriage_pass.carriage_pass
        for cp in self.carriage_pass_graph.successors(carriage_pass):
            return cp
        return None

    def get_prior_carriage_pass(self, carriage_pass: Knitout_Needle_Instruction | Carriage_Pass_Collection) -> Optional[Carriage_Pass_Collection]:
        """
        :param carriage_pass: carriage pass or an instruction in a carriage passes
        :return: the following carriage pass or None if last pass
        """
        if isinstance(carriage_pass, Knitout_Needle_Instruction):
            carriage_pass = carriage_pass.carriage_pass
        for cp in self.carriage_pass_graph.predecessors(carriage_pass):
            return cp
        return None

    def connect_releasehook_instructions(self):
        releasehook_directions = {}
        for inhook, releasehook in self._inhook_releasehook_pairs.items():
            releasehook_directions[releasehook] = self._inhook_directions[inhook]
            loops_since_inhook = 0
            next_instruction_with_yarn = self.next_needle_instruction_with_carrier(inhook)
            assert next_instruction_with_yarn is not None, f"{inhook.carrier_set} inhooked but never knit."
            while next_instruction_with_yarn is not None and loops_since_inhook < self._min_loops_before_release_hook:
                self.instruction_graph.add_edge(next_instruction_with_yarn, releasehook, is_releasehook_edge=True, carrier_set=releasehook.carrier_set)
                if isinstance(next_instruction_with_yarn, Loop_Making_Instruction):
                    loops_since_inhook += 1
                next_instruction_with_yarn = self.next_needle_instruction_with_carrier(next_instruction_with_yarn)

        for inhook, releasehook in self._inhook_releasehook_pairs.items():
            direction = self._inhook_directions[inhook]
            found_next_pass = False
            next_carriage_pass = self.get_next_carriage_pass(self.next_needle_instruction_with_carrier(inhook))
            while next_carriage_pass is not None:
                if next_carriage_pass.direction is None or next_carriage_pass.direction == direction:  # could be the next pass
                    first_in_pass = next_carriage_pass[0]
                    if not self.instruction_graph.has_edge(first_in_pass, releasehook):  # pass does not need hook in place
                        self.instruction_graph.add_edge(releasehook, first_in_pass, is_releasehook_edge=True)
                        prior_pass = self.get_prior_carriage_pass(next_carriage_pass)
                        assert prior_pass is not None, f"Knitout Error: Cannot releasehook before knitting"
                        last_in_pass = prior_pass[-1]
                        self.instruction_graph.add_edge(last_in_pass, releasehook, is_release_hook_edge=True)
                        found_next_pass = True
                        if next_carriage_pass.direction is None:
                            next_carriage_pass.direction = direction  # direction is implied by releasehook direction
                        break
                next_carriage_pass = self.get_next_carriage_pass(next_carriage_pass)
            if not found_next_pass:
                self.instruction_graph.add_edge(self.context.carriage_passes[-1][-1], releasehook, is_release_hook_edge=True)  # no carriage pass meets requirements

    def add_yarn_connections(self):
        for carrier, instructions in self.context.carrier_instructions.items():
            for instruction_1, instruction_2 in zip(instructions[:-1], instructions[1:]):
                self.instruction_graph.add_edge(instruction_1, instruction_2,
                                                is_carrier_edge=True, carrier=carrier)
        for carrier, instructions in self.context.carrier_management_instructions.items():
            for instruction_1, instruction_2 in zip(instructions[:-1], instructions[1:]):
                self.instruction_graph.add_edge(instruction_1, instruction_2,
                                                is_carrier_edge=True, carrier=carrier)
            inhook = None
            for instruction in self.context.carrier_management_instructions[carrier]:
                if isinstance(instruction, Inhook_Instruction):
                    assert inhook is None, f"New Inhook instruction {instruction} found before releasehook"
                    inhook = instruction
                    next_needle_instruction = self.next_needle_instruction_with_carrier(inhook)
                    assert isinstance(next_needle_instruction, Knitout_Needle_Instruction), \
                        f"Inhook followed by carrier instruction {next_needle_instruction} without knitting."
                    self._inhook_directions[inhook] = next_needle_instruction.direction
                    self._inhook_next_pass[inhook] = next_needle_instruction.carriage_pass
                elif isinstance(instruction, Releasehook_Instruction):
                    assert inhook is not None, f"Release hook instruction {instruction} found before inhook"
                    self._inhook_releasehook_pairs[inhook] = instruction
                    inhook = None

    def next_in_carriage_pass(self, instruction: Knitout_Needle_Instruction) -> Optional[Knitout_Needle_Instruction]:
        """
        :param instruction:
        :return: Next instruction in the same carriage-pass as this instruction
        """
        successors = self.instruction_graph.successors(instruction)
        for successor in successors:
            edge = self.instruction_graph.edges[instruction, successor]
            edge_is_cp = "is_carrier_edge" in edge and edge["is_carrier_edge"]
            if edge_is_cp:  # recurse to next node:
                return successor
        return None

    def prior_in_carriage_pass(self, instruction: Knitout_Needle_Instruction) -> Optional[Knitout_Needle_Instruction]:
        """
        :param instruction:
        :return: Next instruction in the same carriage-pass as this instruction
        """
        predecessors = self.instruction_graph.predecessors(instruction)
        for predecessor in predecessors:
            edge = self.instruction_graph.edges[instruction, predecessor]
            edge_is_cp = "is_carrier_edge" in edge and edge["is_carrier_edge"]
            if edge_is_cp:  # recurse to next node:
                return predecessor
        return None

    def jump_to_end_of_carriage_pass(self, instruction: Knitout_Needle_Instruction) -> Knitout_Needle_Instruction:
        """
        :param instruction: the instruction in a carriage pass.
        :return: The instruction at the end of the carriage passes this instruction is in.
        Returns this instruction if it is the end of the carriage pass
        """
        next_in_pass = self.next_in_carriage_pass(instruction)
        if next_in_pass is None:
            return instruction
        else:
            return self.jump_to_end_of_carriage_pass(next_in_pass)

    def jump_to_start_of_carriage_pass(self, instruction: Knitout_Needle_Instruction) -> Knitout_Needle_Instruction:
        """
        :param instruction: the instruction in a carriage pass.
        :return: The instruction at the end of the carriage passes this instruction is in.
        Returns this instruction if it is the end of the carriage pass
        """
        prior_in_pass = self.prior_in_carriage_pass(instruction)
        if prior_in_pass is None:
            return instruction
        else:
            return self.jump_to_start_of_carriage_pass(prior_in_pass)

    def next_needle_instruction_with_carrier(self, instruction: Carrier_Instruction | Knitout_Needle_Instruction) \
            -> Optional[Knitout_Needle_Instruction]:
        """
        :param instruction:
        :return: next instruction that uses the carrier of the given instruction or None if no more instructions are found
        """
        inhook_successors = self.instruction_graph.successors(instruction)
        for successor in inhook_successors:
            edge = self.instruction_graph.edges[instruction, successor]
            edge_is_carrier = "is_carrier_edge" in edge and edge["is_carrier_edge"]
            if edge_is_carrier and isinstance(successor, Knitout_Needle_Instruction):
                return successor
        return None

    def update_carriage_pass_directions(self):
        for i, carriage_pass in enumerate(self.context.carriage_passes):  # update xfer pass directions and operation order
            if carriage_pass.direction is None:  # transfer pass with no implied pass direction
                if i == 0:
                    carriage_pass.direction = Pass_Direction.Leftward
                else:
                    carriage_pass.direction = self.context.carriage_passes[i - 1].direction.opposite()
            if isinstance(carriage_pass[0], Xfer_Instruction):
                carriage_pass = carriage_pass.sort_instructions(carriage_pass.direction)
            for instruction_1, instruction_2 in zip(carriage_pass[:-1], carriage_pass[1:]):
                self.instruction_graph.add_edge(instruction_1, instruction_2,
                                                is_carriage_pass_edge=True, direction=carriage_pass.direction)

        for cp1, cp2 in self.carriage_pass_graph.edges:
            if cp1.direction == cp2.direction:
                has_no_op_pass = True
            else:
                has_no_op_pass = False
            if cp1.direction is Pass_Direction.Leftward:
                side = "left"
            else:
                side = "right"
            self.instruction_graph.add_edge(cp1[-1], cp2[0], is_between_carriage_pass_edge=True, side=side, has_no_op_pass=has_no_op_pass)

    def add_loop_connections(self):
        for loop in self.context.machine_state.knit_graph.loops.values():
            loop_instructions = loop.instructions
            assert len(loop_instructions) > 0
            assert isinstance(loop_instructions[0], Loop_Making_Instruction), f"Loop is {loop_instructions[0]} before it is made by knit, tuck, or split"
            for instruction_1, instruction_2 in zip(loop_instructions[:-1], loop_instructions[1:]):
                self.instruction_graph.add_edge(instruction_1, instruction_2, is_loop_edge=True, loop=loop)

    def string_graph(self) -> DiGraph:
        strings = DiGraph()
        for u, v in self.instruction_graph.edges:
            data = self.instruction_graph.get_edge_data(u, v)
            string_data = {data_id: str(data_value) for data_id, data_value in data.items()}
            strings.add_edge(f"{u.original_line_number}:{u}", f"{v.original_line_number}:{v}", **string_data)
        return strings

    def topo_sort(self) -> List[Knitout_Line]:
        sorted_instructions = [*networkx.topological_sort(self.instruction_graph)]
        return sorted_instructions

    def visualize(self):
        networkx.write_graphml(self.string_graph(), "knitout_instruction_graph.graphml")
