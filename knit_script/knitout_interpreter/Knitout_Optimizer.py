"""Knitout_Optimizer"""
from typing import Optional

import networkx as nx
from networkx import DiGraph

from knit_script.knitout_interpreter.Knitout_Context import Knitout_Context
from knit_script.knitout_interpreter.knitout_structures.Carraige_Pass_Collection import Carriage_Pass_Instruction_Collection
from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Knitout_Line
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.Rack_Instruction import Rack_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.carrier_instructions import Outhook_Instruction, Inhook_Instruction, In_Instruction, \
    Out_Instruction, Releasehook_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.needle_instructions import Knitout_Needle_Instruction, Loop_Making_Instruction, Xfer_Instruction


class Knitout_Optimizer:
    """
        Optimizes interpreted knitout using topological sorting
    """
    _is_cp_start = "is_cp_start"
    _carriage_pass = "carriage_pass"

    def __init__(self, context: Knitout_Context, min_loops_before_release_hook=10, hook_size=4):
        self._hook_size = hook_size
        self._min_loops_before_release_hook = min_loops_before_release_hook
        self.context = context
        self.needle_instruction_graph: DiGraph = DiGraph()
        self.carriage_pass_graph: DiGraph = DiGraph()
        self.yarn_instruction_graph: DiGraph = DiGraph()
        self._needle_instructions_to_carriage_passes: dict[Knitout_Needle_Instruction: Carriage_Pass_Instruction_Collection] = {}
        self._carriage_pass_to_prior_pass: dict[Carriage_Pass_Instruction_Collection, Optional[Carriage_Pass_Instruction_Collection]] = {}
        self._instruction_to_releasehook: dict[Knitout_Line, Optional[Releasehook_Instruction]] = {}
        self._add_carriage_pass_edges()
        self._add_yarn_edges()
        self._add_stitch_edges()
        self._add_carriage_pass_edges()

    def _add_yarn_edges(self):
        current_in = None
        last_instruction = None
        loops_to_release = 0
        release = None
        inhook_direction = None
        pass_before_release = None
        for carrier, instructions in self.context.carrier_instructions.items():
            for instruction in instructions:
                self._instruction_to_releasehook[instruction] = release
                if isinstance(instruction, Inhook_Instruction):
                    current_in = instruction
                    last_instruction = current_in
                    release = Releasehook_Instruction(current_in.carrier_set, "Injected Releasehook")
                    loops_to_release = self._min_loops_before_release_hook
                elif isinstance(instruction, In_Instruction):
                    current_in = instruction
                    last_instruction = current_in
                elif isinstance(instruction, Knitout_Needle_Instruction):
                    assert last_instruction is not None
                    self.yarn_instruction_graph.add_edge(last_instruction, instruction, yarn_edge=True, yarn=str(carrier))
                    if inhook_direction is None and isinstance(last_instruction, Inhook_Instruction):
                        inhook_direction = instruction.direction
                        release.comment += f" before {inhook_direction} pass"
                        self.yarn_instruction_graph.add_edge(current_in, release, inhook_release_edge=True)
                    if inhook_direction is not None:
                        if loops_to_release > 0:  # loops still required to hold yarn
                            pass_before_release = self._needle_instructions_to_carriage_passes[instruction]  # carriage pass that can have release before it
                            self.carriage_pass_graph.add_edge(pass_before_release[-1], release, release_after_pass=True, inhook=current_in, carriage_pass=pass_before_release)
                            loops_to_release -= 1
                        elif inhook_direction is not None:  # sufficient loops released, looking for pass in inhook direction
                            if instruction.direction == inhook_direction:
                                carriage_pass = self._needle_instructions_to_carriage_passes[instruction]  # carriage pass that can have release before it
                                if carriage_pass is not pass_before_release:
                                    self.carriage_pass_graph.add_edge(release, carriage_pass[0], release_before_pass=True, inhook=current_in, carriage_pass=carriage_pass)
                                    prior_pass = self._carriage_pass_to_prior_pass[carriage_pass]
                                    # if prior_pass is not None:
                                    #     self.carriage_pass_graph.add_edge(prior_pass[-1], release, release_after_pass=True, inhooh=current_in, carriage_pass=prior_pass)
                                    loops_to_release = 0
                                    inhook_direction = None
                                    pass_before_release = None
                    last_instruction = instruction
                elif isinstance(instruction, Outhook_Instruction):
                    self.yarn_instruction_graph.add_edge(last_instruction, instruction)
                    self.yarn_instruction_graph.add_edge(current_in, instruction)
                    if release is not None:
                        self.yarn_instruction_graph.add_edge(release, instruction)
                    last_instruction = None
                    current_in = None
                    inhook_direction = None
                    release = None
                    loops_to_release = 0
                elif isinstance(instruction, Out_Instruction):
                    self.yarn_instruction_graph.add_edge(last_instruction, instruction)
                    self.yarn_instruction_graph.add_edge(current_in, instruction)
                    last_instruction = None
                    current_in = None
                    inhook_direction = None
                    release = None
                    loops_to_release = 0

    def _add_stitch_edges(self):
        for loop in self.context.machine_state.knit_graph.loops.values():
            loop_instructions = loop.instructions
            assert len(loop_instructions) > 0
            assert isinstance(loop_instructions[0], Loop_Making_Instruction), f"Loop is {loop_instructions[0]} before it is made by knit, tuck, or split"
            for instruction_1, instruction_2 in zip(loop_instructions[:-1], loop_instructions[1:]):
                self.needle_instruction_graph.add_edge(instruction_1, instruction_2, is_stitch_edge=True, loop=loop)

    def _add_carriage_pass_edges(self):
        prior_instruction = None
        prior_pass = None
        for i, carriage_pass in enumerate(self.context.carriage_passes):
            self._carriage_pass_to_prior_pass[carriage_pass] = prior_pass
            prior_pass = carriage_pass
            rack_instruction = carriage_pass.rack_instruction()
            rack_instruction.comment = f"injected rack for cp {i}"
            self.carriage_pass_graph.add_edge(rack_instruction, carriage_pass[0], rack_before_cp=True, carriage_pass=carriage_pass, in_cp_edge=False, between_cp_edge=True)
            if prior_instruction is not None:
                self.carriage_pass_graph.add_edge(prior_instruction, rack_instruction, cp_before_rack=True, carriage_pass=self._needle_instructions_to_carriage_passes[prior_instruction],
                                                  in_cp_edge=False, between_cp_edge=True)
            prior_instruction = carriage_pass[0]
            self._needle_instructions_to_carriage_passes[prior_instruction] = carriage_pass
            for instruction in carriage_pass[1:]:
                self.carriage_pass_graph.add_edge(prior_instruction, instruction, in_cp_edge=True, between_cp_edge=False)
                prior_instruction = instruction
                self._needle_instructions_to_carriage_passes[instruction] = carriage_pass

    def _add_xfer_release_constraint(self):
        last_release = None
        for carriage_pass in self.context.carriage_passes:
            if carriage_pass[-1] in self._instruction_to_releasehook:
                last_release = self._instruction_to_releasehook[last_release]
            elif last_release is not None and isinstance(carriage_pass[0], Xfer_Instruction):
                self.carriage_pass_graph.add_edge(last_release, carriage_pass[0], release_for_xfer=True, between_cp_edge=True, in_cp_edge=False)
                last_release = None

    def merge_graphs(self) -> DiGraph:
        yarn_and_needle = nx.compose(self.yarn_instruction_graph, self.needle_instruction_graph)
        all_graph = nx.compose(yarn_and_needle, self.carriage_pass_graph)
        return all_graph

    def optimize(self) -> list[Knitout_Line]:
        sorted_instructions = [*nx.topological_sort(self.merge_graphs())]
        clean_instructions = [self.context.version_line]
        clean_instructions.extend(self.context.executed_header)
        current_rack = 0
        for instruction in sorted_instructions:
            if not isinstance(instruction, Rack_Instruction) or instruction.rack != current_rack:
                clean_instructions.append(instruction)
        return clean_instructions

    def visualize(self, output_name: str = "knitout_graph", needles=True, yarn=True, cp=True, merged_graphs=True):
        """
            Outputs a graphml file to visualize the needle graph
        """

        def _string_graph(graph: DiGraph):
            strings = DiGraph()
            for u, v in graph.edges:
                data = graph.get_edge_data(u, v)
                if data is None:
                    string_data = {}
                else:
                    string_data = {data_id: str(data_value) for data_id, data_value in data.items()}
                strings.add_edge(f"{u.original_line_number}:{u}", f"{v.original_line_number}:{v}", **string_data)
            return strings

        if needles:
            nx.write_graphml(_string_graph(self.needle_instruction_graph), f"needles_{output_name}.graphml")
        if yarn:
            nx.write_graphml(_string_graph(self.yarn_instruction_graph), f"yarn_{output_name}.graphml")
        if cp:
            nx.write_graphml(_string_graph(self.carriage_pass_graph), f"passes_{output_name}.graphml")
        if merged_graphs:
            nx.write_graphml(_string_graph(self.merge_graphs()), f"{output_name}.graphml")

    # def optimize_knitout(self) -> list[Knitout_Line]:
    #         sorted_instructions = [*nx.topological_sort(self.)]
    #         return sorted_instructions
