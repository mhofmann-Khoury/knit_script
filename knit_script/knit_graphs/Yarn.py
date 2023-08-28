"""
The Yarn Data Structure
"""
from typing import Optional, Tuple, List, Dict

import networkx as networkx

from knit_script.knit_graphs.Loop import Loop
from knit_script.knitting_machine.machine_components.needles import Needle


class Yarn:
    """
    A class to represent a yarn structure.
    Yarns are structured as a list of loops with a pointer to the last loop id
    ...

    Attributes
    ----------
    yarn_graph: networkx.DiGraph
        A directed graph structure (always a list) of loops on the yarn
    last_loop_id: Optional[int]
        The id of the last loop on the yarn, none if no loops on the yarn
    """

    def __init__(self, yarn_id: str, last_loop: Optional[Loop] = None,
                 size: int = 2, plies: int = 30, color: str | None = "green"):
        """
        A Graph structure to show the yarn-wise relationship between loops
        :param yarn_id: the identifier for this loop
        :param last_loop: the loop to add onto this yarn at the beginning. May be none if yarn is empty.
        """
        self.color = color
        self.plies = plies
        self.size = size
        self.yarn_graph: networkx.DiGraph = networkx.DiGraph()
        if last_loop is None:
            self.last_loop_id = None
        else:
            self.last_loop_id: int = last_loop.loop_id
        self._yarn_id: str = yarn_id

    @staticmethod
    def yarn_by_type(color: str, last_loop: Optional[Loop] = None,
                     size: int = 2, plies: int = 30):
        """
        :param color:
        :param last_loop:
        :param size:
        :param plies:
        :return: Yarn with default string for specified yarn
        """
        return Yarn(f"{size}-{plies} {color}", last_loop, size, plies, color)

    @property
    def yarn_id(self) -> str:
        """
        :return: the id of this yarn
        """
        return self._yarn_id

    def __str__(self):
        return str(self.yarn_id)

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.yarn_graph.nodes)

    def last_needle(self) -> Optional[Needle]:
        """
        :return: The needle that holds the loop closest to the end of the yarn or None if the yarn has been dropped entirely
        """
        for loop in reversed(self):
            if loop.on_needle:
                return loop.holding_needle
        return None

    def add_loop_to_end(self, loop_id: int = None, loop: Optional[Loop] = None, is_twisted: bool = False, knit_graph=None) -> Tuple[int, Loop]:
        """
        Adds the loop at the end of the yarn
        :param knit_graph: Optional Knit_Graph used to calculate last loop id in knitgraph
        :param is_twisted: The parameter used for twisting the loop if it is created in the method
        :param loop: The loop to be added at this id. If none, a non-twisted loop will be created
        :param loop_id: the id of the new loop, if the loopId is none, it defaults to 1 more than last loop in the graph
        :return: the loop_id added to the yarn, the loop added to the yarn
        """
        return self.insert_loop(self.last_loop_id, True, loop_id, loop, is_twisted=is_twisted, knit_graph=knit_graph)

    def insert_loop(self, neighbor_loop_id: int, insert_after: bool,
                    loop_id: int = None, loop: Optional[Loop] = None,
                    layer: int = 0, is_twisted: bool = False, knit_graph=None):
        """
            Adds the loop at the end of the yarn
            :param knit_graph: Optional Knit_Graph used to calculate last loop id
            :param layer: The layer (0 by default) this loop is compared to other loops at the same position
            :param insert_after: if true, will add the loop to the yarn after neighbor
            :param neighbor_loop_id: the neighbor loop id to add to
            :param is_twisted: The parameter used for twisting the loop if it is created in the method
            :param loop: The loop to be added at this id. If none, a non-twisted loop will be created
            :param loop_id: the id of the new loop, if the loopId is none, it defaults to 1 more than last loop in the graph
            :return: the loop_id added to the yarn, the loop added to the yarn
            """
        if loop_id is None:  # Create a new Loop ID
            if loop is not None:  # get the loop id from the provided loop
                assert self.last_loop_id > loop.loop_id, \
                    f"Cannot add loop {loop.loop_id} after loop {self.last_loop_id}."
                loop_id = loop.loop_id
            else:  # the next loop on this yarn
                assert knit_graph is not None, "Cannot determine last loop id without a Knit_Graph"
                loop_id = knit_graph.last_loop_id + 1

        if loop is None:  # create a loop from default information
            loop = Loop(loop_id, self, layer=layer, is_twisted=is_twisted)
        self.yarn_graph.add_node(loop_id, loop=loop)
        if knit_graph is not None:
            knit_graph.add_loop(loop)
        if neighbor_loop_id is not None:
            if insert_after:
                for next_neighbor_id in [*self.yarn_graph.successors(neighbor_loop_id)]:
                    self.yarn_graph.remove_edge(neighbor_loop_id, next_neighbor_id)
                    self.yarn_graph.add_edge(loop_id, next_neighbor_id)
                self.yarn_graph.add_edge(neighbor_loop_id, loop_id)
            else:
                for prior_neighbor_id in [*self.yarn_graph.predecessors(neighbor_loop_id)]:
                    self.yarn_graph.remove_edge(prior_neighbor_id, neighbor_loop_id)
                    self.yarn_graph.add_edge(prior_neighbor_id, loop_id)
                self.yarn_graph.add_edge(loop_id, neighbor_loop_id)
        if len([*self.yarn_graph.successors(loop_id)]) == 0:
            self.last_loop_id = loop_id
        return loop_id, loop

    def __contains__(self, item):
        """
        Return true if the loop is on the yarn
        :param item: the loop being checked for in the yarn
        :return: true if the loop_id of item or the loop is in the yarn
        """
        if type(item) is int:
            return self.yarn_graph.has_node(item)
        elif isinstance(item, Loop):
            return self.yarn_graph.has_node(item.loop_id)
        else:
            return False

    def __iter__(self):
        return iter(self.yarn_graph)

    def __getitem__(self, item: int) -> Loop:
        """
        Collect the loop of a given id
        :param item: the loop_id being checked for in the yarn
        :return: the Loop on the yarn with the matching id
        """
        if item not in self:
            raise AttributeError
        else:
            return self.yarn_graph.nodes[item].loop

    def cut_yarn(self):
        """
        :return: New Yarn of the same type after cut this yarn
        """
        return Yarn(self.yarn_id + "_cut", size=self.size, plies=self.plies, color=self.color)
