"""The Loop data structure"""
from typing import List, Optional

from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction


class Loop:
    """
    A class to represent a single loop structure
    Loops can be twisted (but no possible on knitting machines, so defaults to false)
    loops must be assigned a yarn parent
    The layer of a loop defines its position relative to other loops, for instance in cables and gauged sheets. Defaults to 0
    ...

    Attributes
    ----------
    is_twisted: bool
        True if the loop is twisted
    parent_loops: List[Loop]
        The list of loops that this loop is pulled through.
        The order in the list implies the stacking order with the first loop at the bottom the stack
    yarn: Yarn
        The Yarn that the loop is made on
    layer: int
        The position of this loop relative to other layers
    """
    #Todo add needle stacking edges to knitgraph structure
    def __init__(self, loop_id: int, yarn, layer: int = 0, is_twisted: bool = False, holding_needle=None):
        """
        :param holding_needle: needle that currently holds the loop
        :param layer:
        :param loop_id: id of loop. IDs should represent the order that loops are created
            with the first loop being created with id 0
        :param is_twisted: True if the loop should be twisted
            (created by pulling a carrier backwards across the needle)
        """
        self._holding_needle = holding_needle
        self.instructions: List[Instruction] = []
        self.creating_instruction: Optional[Instruction] = None
        self.is_twisted: bool = is_twisted
        assert loop_id >= 0, f"{loop_id}: Loop_id must be non-negative"
        self._loop_id: int = loop_id
        self.yarn = yarn
        self.parent_loops: List[Loop] = []
        self.layer: int = layer

    def put_on_needle(self, needle):
        """
        :param needle: Needle that now holds the loop
        """
        self._holding_needle = needle

    def drop_from_needle(self):
        """
        Drop loop from holding needle
        """
        self._holding_needle = None

    @property
    def holding_needle(self):
        """
        :return: Needle that currently holds this loop
        """
        return self._holding_needle

    @property
    def on_needle(self) -> bool:
        """
        :return: True if loop is on a needle
        """
        return self.holding_needle is not None

    def apply_operation(self, instruction: Instruction):
        self.instructions.append(instruction)
        # todo update holding needle based on operation

    def add_parent_loop(self, parent, stack_position: Optional[int] = None):
        """
        Adds the parent Loop onto the stack of parent_loops
        :param parent: the Loop to be added onto the stack
        :param stack_position: The position to insert the parent into, by default add on top of the stack
        """
        if stack_position is not None:
            self.parent_loops.insert(stack_position, parent)
        else:
            self.parent_loops.append(parent)

    @property
    def loop_id(self) -> int:
        """
        :return: the id of the loop
        """
        return self._loop_id

    def prior_loop_id(self, knitGraph) -> Optional[int]:
        """
        :param knitGraph: the knitgraph to check for prior loops
        :return: the id of the loop that comes before this in the knitgraph
        """
        prior_id = self.loop_id - 1
        if knitGraph.graph.has_node(prior_id):
            return prior_id
        else:
            return None

    def next_loop_id(self, knitGraph) -> Optional[int]:
        """
        :param knitGraph: the knitgraph to check for next loops
        :return: the id of the loop that comes after this in the knitgraph
        """
        next_id = self.loop_id + 1
        if knitGraph.graph.has_node(next_id):
            return next_id
        else:
            return None

    @property
    def is_twisted(self) -> bool:
        """
        :return: True if the loop is twisted
        """
        return self._is_twisted

    @is_twisted.setter
    def is_twisted(self, is_twisted: bool):
        self._is_twisted = is_twisted

    def __hash__(self):
        return self.loop_id

    def __eq__(self, other):
        return isinstance(other, Loop) and self.loop_id == other.loop_id and self.yarn == other.yarn

    def __lt__(self, other):
        assert isinstance(other, Loop)
        return self.loop_id < other.loop_id

    def __gt__(self, other):
        assert isinstance(other, Loop)
        return self.loop_id > other.loop_id

    def __str__(self):
        if self.is_twisted:
            twisted = ", twisted"
        else:
            twisted = ""
        return f"{self.loop_id} on yarn {self.yarn}{twisted}"

    def __repr__(self):
        return str(self)
