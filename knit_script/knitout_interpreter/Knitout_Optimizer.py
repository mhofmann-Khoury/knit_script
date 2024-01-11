import math
from enum import Enum
from typing import Any

import networkx as nx
from networkx import DiGraph, NetworkXUnfeasible

from knit_script.Knit_Errors.Knitout_Error import Knitout_Error
from knit_script.knitout_interpreter.Knitout_Context import Knitout_Context
from knit_script.knitout_interpreter.knitout_structures.Carriage_Pass_Instructions import Carriage_Pass_Instructions
from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Knitout_Line
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.Rack_Instruction import Rack_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.carrier_instructions import Inhook_Instruction, Releasehook_Instruction, In_Instruction, Outhook_Instruction, \
    Out_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.needle_instructions import Knitout_Needle_Instruction, Loop_Making_Instruction
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction


class CP_Prerequisite(Enum):
    """
    Enumeration of Prerequisite types before a carriage pass
    """
    rack_to = "rack_to"
    yarn_available = "yarn_available"
    matches_hook_direction = "matches_hook_direction"
    yarn_order = "yarn_order"
    stitch_order = "stitch_order"
    xfer_after_release = "xfer_after_release"

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class Instruction_Prerequisite(Enum):
    """
    Enumeration of Prerequisite types before an instruction
    """
    hook_available = "hook_available"
    stable_yarn = "stable_yarn"
    in_before_out = "in_before_out"
    yarn_used = "yarn_used"
    hook_direction = "hook_direction"
    rack_used = "rack_used"

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class Knitout_Optimizer:
    """
        Optimizes Knitout from given context by relationship between instructions and whole carriage passes
    """

    def __init__(self, context: Knitout_Context, min_loops_before_release_hook=10, hook_size=4):
        self._hook_size = hook_size
        self._min_loops_before_release_hook = min_loops_before_release_hook
        self.context = context
        self.carriage_passes: list[Carriage_Pass_Instructions] = [*self.context.carriage_passes]
        for i, cp in enumerate(self.carriage_passes):
            cp.index = i
        self.needle_instruction_graph: DiGraph = DiGraph()
        self.carriage_pass_prerequisites: DiGraph = DiGraph()
        self.yarn_instruction_graph: DiGraph = DiGraph()
        self.instructions_to_cp: dict[Knitout_Needle_Instruction, Carriage_Pass_Instructions] = {}
        self.instruction_to_next_xfer: dict[Knitout_Needle_Instruction, Carriage_Pass_Instructions | None] = {}
        self._organize_instructions_in_cp()
        self._add_carriage_pass_edges()
        self._add_stitch_edges()
        self._add_yarn_edges()

    @staticmethod
    def _add_edge(graph: DiGraph, u, v, list_attributes: dict[str, Any], update_attributes: dict[str, Any]):
        """
        Adds an edge to the graph or updates the attributes if already present.
        :param graph: Graph to update.
        :param u: Start of edge.
        :param v: End of edge.
        :param list_attributes: Attributes in lists to add to.
        :param update_attributes: Attributes to update (override or add)
        """
        if not graph.has_edge(u, v):
            graph.add_edge(u, v)
        for key, addition in list_attributes.items():
            if key not in graph[u][v]:
                if isinstance(addition, tuple):
                    cur_values = {}
                else:
                    cur_values = set()
            else:
                cur_values = graph[u][v][key]
            if isinstance(cur_values, set):
                cur_values.add(addition)
            elif isinstance(cur_values, list):
                cur_values.append(addition)
            elif isinstance(cur_values, dict):
                assert isinstance(addition, tuple)
                cur_values[addition[0]] = addition[1]
            update_attributes[key] = cur_values
        nx.set_edge_attributes(graph, {(u, v): update_attributes})

    def _organize_instructions_in_cp(self):
        """
            Organizes carriage passes based on their instructions for indexing
        """
        for carriage_pass in self.carriage_passes:
            self.instructions_to_cp.update({instruction: carriage_pass for instruction in carriage_pass})

    def _add_carriage_pass_edges(self):
        """
            Add edges by carriage pass prerequisites.
        """
        last_rack_instruction = Rack_Instruction(0, f"Initialize 0 Rack")
        prior_pass = None
        for carriage_pass in self.carriage_passes:
            rack_instruction = carriage_pass.rack_instruction()
            rack_instruction.comment = f"Racked for carriage pass {carriage_pass.index}"
            if rack_instruction.rack != last_rack_instruction.rack:
                if prior_pass is not None:
                    self._add_edge(self.carriage_pass_prerequisites, prior_pass, rack_instruction,
                                   list_attributes={"prereqs": Instruction_Prerequisite.rack_used}, update_attributes={str(Instruction_Prerequisite.rack_used): True})
                last_rack_instruction = rack_instruction
            self._add_edge(self.carriage_pass_prerequisites, last_rack_instruction, carriage_pass,
                           list_attributes={"prereqs": CP_Prerequisite.rack_to}, update_attributes={str(CP_Prerequisite.rack_to): True})
            # if prior_pass is not None:
            #     self._add_edge(self.carriage_pass_prerequisites, prior_pass)
            prior_pass = carriage_pass

    def _add_yarn_edges(self):
        """
            Add edges by yarn management and use constraints
        """
        inhook_to_release: dict[Inhook_Instruction, Releasehook_Instruction] = {}
        inhook_to_first_carriage_passes: dict[Inhook_Instruction, Carriage_Pass_Instructions] = {}
        carriage_pass_to_inhook: dict[Carriage_Pass_Instructions, Inhook_Instruction] = {}
        current_in = None
        yarn_knit = False
        loops_to_release = 0
        release = None
        release_satisfied = False
        inhook_direction_set_pass = None
        last_involved_pass = None

        def _reset_yarn():
            nonlocal current_in
            current_in = None
            nonlocal yarn_knit
            yarn_knit = False
            nonlocal loops_to_release
            loops_to_release = 0
            nonlocal release
            release = None
            nonlocal inhook_direction_set_pass
            inhook_direction_set_pass = None
            nonlocal last_involved_pass
            last_involved_pass = None

        for carrier, instructions in self.context.carrier_instructions.items():
            _reset_yarn()
            for instruction in instructions:
                if isinstance(instruction, Inhook_Instruction):
                    if isinstance(current_in, Inhook_Instruction):
                        self._add_edge(self.yarn_instruction_graph, release, instruction,
                                       list_attributes={"prereqs": Instruction_Prerequisite.hook_available}, update_attributes={str(Instruction_Prerequisite.hook_available): True, "yarn": carrier})
                    current_in = instruction
                    yarn_knit = False
                    release = Releasehook_Instruction(current_in.carrier_set)
                    release_satisfied = False
                    inhook_to_release[instruction] = release
                    loops_to_release = self._min_loops_before_release_hook
                elif isinstance(instruction, In_Instruction):
                    current_in = instruction
                    yarn_knit = False
                elif isinstance(instruction, Knitout_Needle_Instruction):
                    carriage_pass = self.instructions_to_cp[instruction]
                    if isinstance(current_in, Inhook_Instruction) and current_in not in inhook_to_first_carriage_passes:
                        inhook_to_first_carriage_passes[current_in] = carriage_pass
                        carriage_pass_to_inhook[carriage_pass] = current_in
                    if last_involved_pass is not None and last_involved_pass != carriage_pass:
                        self._add_edge(self.carriage_pass_prerequisites, last_involved_pass, carriage_pass,
                                       list_attributes={"prereqs": CP_Prerequisite.yarn_order}, update_attributes={str(CP_Prerequisite.yarn_order): True, "yarn": carrier})
                    last_involved_pass = carriage_pass
                    assert current_in is not None, f"No in operation for {carrier} before {instruction}"
                    if not yarn_knit:
                        self._add_edge(self.yarn_instruction_graph, current_in, carriage_pass,
                                       list_attributes={"prereqs": CP_Prerequisite.yarn_available}, update_attributes={str(CP_Prerequisite.yarn_available): True, "yarn": carrier})
                        yarn_knit = True
                    if not release_satisfied:  # releasehook prerequisites have not been satisfied
                        if inhook_direction_set_pass is None:  # first knitting pass found before after inhook
                            inhook_direction_set_pass = carriage_pass
                        if loops_to_release > 0:
                            loops_to_release -= 1
                            self._add_edge(self.yarn_instruction_graph, carriage_pass, release,
                                           list_attributes={"prereqs": Instruction_Prerequisite.stable_yarn},
                                           update_attributes={str(Instruction_Prerequisite.stable_yarn): True, "yarn": carrier, "remaining_loops": loops_to_release})

                        elif inhook_direction_set_pass == carriage_pass or inhook_direction_set_pass.direction == carriage_pass.direction.opposite():  # inhook direction does not match yet
                            self._add_edge(self.yarn_instruction_graph, carriage_pass, release,
                                           list_attributes={"prereqs": Instruction_Prerequisite.hook_direction},
                                           update_attributes={str(Instruction_Prerequisite.hook_direction): True, "yarn": carrier})
                        else:  # sufficient loops found, inhook direction matches
                            self._add_edge(self.yarn_instruction_graph, release, carriage_pass,
                                           list_attributes={"prereqs": CP_Prerequisite.matches_hook_direction}, update_attributes={str(CP_Prerequisite.matches_hook_direction): True, "yarn": carrier})
                            inhook_direction_set_pass = None  # inhook satisfied
                            release_satisfied = True  # yarn stable and inhook satisfied
                elif isinstance(instruction, Outhook_Instruction):
                    self._add_edge(self.yarn_instruction_graph, current_in, instruction,
                                   list_attributes={"prereqs": Instruction_Prerequisite.in_before_out}, update_attributes={str(Instruction_Prerequisite.in_before_out): True, "yarn": carrier})
                    self._add_edge(self.yarn_instruction_graph, release, instruction,
                                   list_attributes={"prereqs": Instruction_Prerequisite.hook_available}, update_attributes={str(Instruction_Prerequisite.hook_available): True, "yarn": carrier})
                    if last_involved_pass is not None:
                        self._add_edge(self.yarn_instruction_graph, last_involved_pass, instruction,
                                       list_attributes={"prereqs": Instruction_Prerequisite.yarn_used}, update_attributes={str(Instruction_Prerequisite.yarn_used): True, "yarn": carrier})
                    _reset_yarn()
                elif isinstance(instruction, Out_Instruction):
                    self._add_edge(self.yarn_instruction_graph, current_in, instruction,
                                   list_attributes={"prereqs": Instruction_Prerequisite.in_before_out}, update_attributes={str(Instruction_Prerequisite.in_before_out): True, "yarn": carrier})
                    if last_involved_pass is not None:
                        self._add_edge(self.yarn_instruction_graph, last_involved_pass, instruction,
                                       list_attributes={"prereqs": Instruction_Prerequisite.yarn_used}, update_attributes={str(Instruction_Prerequisite.yarn_used): True, "yarn": carrier})
                    _reset_yarn()

        for inhook, release in inhook_to_release.items():
            merged_graph = self._merge_graphs()
            next_xfer, distance = self._find_next_xfer_pass(inhook, merged_graph)
            if next_xfer is not None:
                self._add_edge(self.yarn_instruction_graph, release, next_xfer, list_attributes={"prereqs": CP_Prerequisite.xfer_after_release},
                               update_attributes={str(CP_Prerequisite.xfer_after_release): True, "yarn": release.carrier_set})

        for inhook, carriage_pass in inhook_to_first_carriage_passes.items():
            for predecessor in self.needle_instruction_graph.predecessors(carriage_pass):
                if isinstance(predecessor, Carriage_Pass_Instructions):
                    if predecessor in carriage_pass_to_inhook:
                        pred_inhook = carriage_pass_to_inhook[predecessor]
                        if pred_inhook != inhook:
                            # self._add_edge(self.yarn_instruction_graph, predecessor, inhook,
                            #                list_attributes={"prereqs": Instruction_Prerequisite.hook_available},
                            #                update_attributes={str(Instruction_Prerequisite.hook_available): True, "yarn": inhook.carrier_set})
                            self._add_edge(self.yarn_instruction_graph, inhook_to_release[pred_inhook], inhook,
                                           list_attributes={"prereqs": Instruction_Prerequisite.hook_available},
                                           update_attributes={str(Instruction_Prerequisite.hook_available): True, "yarn": inhook.carrier_set})

    def _add_stitch_edges(self):
        """
            Add edges by stitch constraints per loop
        """
        for loop in self.context.machine_state.knit_graph.loops.values():
            loop_instructions = loop.instructions
            assert len(loop_instructions) > 0
            first_instruction = loop_instructions[0]
            assert isinstance(first_instruction, Loop_Making_Instruction), f"Loop is {first_instruction} before it is made by knit, tuck, or split"
            self.needle_instruction_graph.add_node(self.instructions_to_cp[first_instruction])
            for instruction_1, instruction_2 in zip(loop_instructions[:-1], loop_instructions[1:]):
                if instruction_1 in self.instructions_to_cp and instruction_2 in self.instructions_to_cp:
                    cp_1 = self.instructions_to_cp[instruction_1]
                    cp_2 = self.instructions_to_cp[instruction_2]
                    self._add_edge(self.needle_instruction_graph, cp_1, cp_2,
                                   list_attributes={"loops": loop, "prereqs": CP_Prerequisite.stitch_order, "prior_instructions": instruction_1, "post_instructions": instruction_2},
                                   update_attributes={str(CP_Prerequisite.stitch_order): True})

    def _find_next_xfer_pass(self, start_node: Carriage_Pass_Instructions | Knitout_Line,
                             graph: DiGraph | None,
                             prior_results: dict[Knitout_Line | Carriage_Pass_Instructions, tuple[None | Carriage_Pass_Instructions, int]] = None) -> tuple[None | Carriage_Pass_Instructions, int]:
        """
        Recursive function from start_node
        :param start_node: the node to start searching from
        :return: None or the xfer pass found, the distance to the xfer pass
        """
        if prior_results is None:
            prior_results = {}
        elif start_node in prior_results:
            return prior_results[start_node]
        if isinstance(start_node, Carriage_Pass_Instructions) and start_node.is_xfer_pass:
            prior_results[start_node] = start_node, 0
            return start_node, 0
        assert start_node in graph, f"Start Node is not included in graph structure"
        selected_xfer = None
        min_distance = math.inf
        for successor in graph.successors(start_node):
            if isinstance(successor, Carriage_Pass_Instructions):
                next_xfer, distance = self._find_next_xfer_pass(successor, graph=graph, prior_results=prior_results)
                if next_xfer is not None and distance < min_distance:
                    min_distance = distance
                    selected_xfer = next_xfer
        if selected_xfer is None:
            prior_results[start_node] = None, 0
            return None, 0
        else:
            prior_results[start_node] = selected_xfer, min_distance + 1
            return selected_xfer, min_distance + 1

    def _merge_graphs(self) -> DiGraph:
        """
        :return: A graph that merges all the constraint graphs
        """
        yarn_and_needle = nx.compose(self.yarn_instruction_graph, self.needle_instruction_graph)
        all_graph = nx.compose(yarn_and_needle, self.carriage_pass_prerequisites)
        return all_graph

    @staticmethod
    def _visualize_graph(graph: DiGraph, output_name: str = "knitout_graph"):
        strings = DiGraph()
        for u, v in graph.edges:
            data = graph.get_edge_data(u, v)
            if data is None:
                string_data = {}
            else:
                string_data = {data_id: str(data_value) for data_id, data_value in data.items()}
            strings.add_edge(u.id_str(), v.id_str(), **string_data)
        nx.write_graphml(strings, f"{output_name}.graphml")

    def visualize(self, output_name: str = "knitout_graph", needles=True, yarn=True, cp=True, merged_graphs=True):
        """
        Outputs a graphml file to visualize the needle graph.
        :param output_name: Name to apply to visualizations.
        :param needles: If True, output needle graph visualization.
        :param yarn: If True, output yarn graph visualization.
        :param cp: If True, output carriage pass graph visualization.
        :param merged_graphs: If True, output merged graphs visualization.
        """

        if needles:
            self._visualize_graph(self.needle_instruction_graph, f"needles_{output_name}")
        if yarn:
            self._visualize_graph(self.yarn_instruction_graph, f"yarn_{output_name}")
        if cp:
            self._visualize_graph(self.carriage_pass_prerequisites, f"passes_{output_name}")
        if merged_graphs:
            self._visualize_graph(self._merge_graphs(), f"{output_name}_merged")

    @staticmethod
    def _reduce_release_direction_constraint(merged_graph: DiGraph) -> DiGraph:
        hook_direction_edges = []
        for u, v, is_hook_direction in merged_graph.edges(data=str(Instruction_Prerequisite.hook_direction), default=False):
            if is_hook_direction:
                prereqs = merged_graph[u][v]['prereqs']
                prereqs.remove(Instruction_Prerequisite.hook_direction)
                if len(prereqs) == 0:
                    hook_direction_edges.append((u, v))
        merged_graph.remove_edges_from(hook_direction_edges)
        return merged_graph

    @staticmethod
    def _reduce_stable_loop_constraint(merged_graph: DiGraph, reduction=1) -> DiGraph:
        stabilizing_edges = []
        for u, v, stable_yarn in merged_graph.edges(data=str(Instruction_Prerequisite.stable_yarn), default=False):
            if stable_yarn:
                remaining_loops = merged_graph[u][v]["remaining_loops"]
                if remaining_loops < reduction:
                    prereqs = merged_graph[u][v]['prereqs']
                    prereqs.remove(Instruction_Prerequisite.stable_yarn)
                    if len(prereqs) == 0:
                        stabilizing_edges.append((u, v))
        merged_graph.remove_edges_from(stabilizing_edges)
        return merged_graph

    def optimize(self, visualize: bool = False) -> list[Knitout_Line]:
        """
        :return: Knitout instructions optimized with topological sorted instruction constraints
        """
        sorted_instructions = None
        graphs = self._merge_graphs()
        try:
            sorted_instructions = [*nx.topological_sort(graphs)]
        except NetworkXUnfeasible as _e:
            print(f"Knitout Warning: Releasehook must happen before another operations. Reducing constraints on releasehook direction")
            graphs = self._reduce_release_direction_constraint(graphs)
            if visualize:
                self._visualize_graph(graphs, f"hook_direction_constraint_reduced")
            try:
                sorted_instructions = [*nx.topological_sort(graphs)]
            except NetworkXUnfeasible as _e:
                for i in range(1, self._min_loops_before_release_hook):
                    graphs = self._reduce_stable_loop_constraint(graphs, i)
                    if visualize:
                        self._visualize_graph(graphs, f"stable_constraint_reduced_by_{i}")
                    try:
                        sorted_instructions = [*nx.topological_sort(graphs)]
                        print(f"Knitout Warning: Releasehook must happen before last {i} stabilizing loops. Yarn may be unstable")
                        break
                    except NetworkXUnfeasible as _e:
                        continue
        if sorted_instructions is None:
            raise Knitout_Error("Cannot optimize releasehook and rack placement with reduced constraints")
        clean_instructions = [self.context.version_line]
        clean_instructions.extend(self.context.executed_header)
        current_rack = 0
        current_direction = Pass_Direction.Leftward
        for instruction in sorted_instructions:
            if isinstance(instruction, Knitout_Line):
                if not isinstance(instruction, Rack_Instruction) or instruction.rack != current_rack:
                    clean_instructions.append(instruction)
                    if isinstance(instruction, Rack_Instruction):
                        current_rack = instruction.rack
            elif isinstance(instruction, Carriage_Pass_Instructions):
                if len(instruction.instructions) > 0:
                    if instruction.is_xfer_pass:
                        current_direction = current_direction.opposite()
                        instruction = instruction.sort_instructions(current_direction)
                    clean_instructions.extend(instruction.instructions)
        return clean_instructions
