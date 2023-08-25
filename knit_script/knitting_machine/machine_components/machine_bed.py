"""Representation of a needle bed on a machine"""

from typing import Dict, List, Optional, Set

from knit_script.knit_graphs.Knit_Graph import Knit_Graph
from knit_script.knit_graphs.Loop import Loop

from knit_script.knitting_machine.machine_components.needles import Slider_Needle, Needle
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set


class Machine_Bed:
    """
    A structure to hold information about loops held on one bed of needles...
    increasing indices indicate needles moving from left to right
        i.e., LEFT -> 0 1 2....N <- RIGHT of Machine
    Attributes
    ----------
    loops_to_needle: Dict[int, Optional[int]]
        A dictionary keyed by loop ids to the needle location that this loop is currently held at.
         If it is not held this is None or non-existent
    needles: List[Needle]
        The needles on this bed ordered from 0 to max
    sliders: List[Slider_Needle]
        The slider needles on this bed ordered from 0 to max
    """

    def __init__(self, is_front: bool, needle_count: int = 250):
        """
        A representation of the state of a bed on the machine
        :param is_front: True if this is the front bed, false if it is the back bed
        :param needle_count: the number of needles that are on this bed
        """
        self._is_front: bool = is_front
        self._needle_count: int = needle_count
        self.needles: List[Needle] = [Needle(self._is_front, i) for i in range(0, self.needle_count)]
        self.sliders: List[Slider_Needle] = [Slider_Needle(self._is_front, i) for i in range(0, self.needle_count)]
        self.loops_to_needle: Dict[Loop, Optional[Needle]] = {}
        self._active_sliders: Set[Slider_Needle] = set()

    @property
    def needle_count(self) -> int:
        """
        :return: the number of needles on the bed
        """
        return self._needle_count

    def __len__(self):
        return self.needle_count

    @property
    def is_front(self) -> bool:
        """
        :return: true if this is the front bed
        """
        return self._is_front

    def add_loops(self, needle: Needle, loops: List[Loop], drop_prior_loops: bool = True) -> List[Loop]:
        """
        Puts the loop_id on given needle, overrides existing loops as if a knit operation took place
        :param loops: the loops to put on the needle if not creating with the yarn carrier
        :param needle: the needle to add the loops on
        :param drop_prior_loops: If true, any loops currently held on this needle are dropped
        :return Returns the list of loops made with the carrier on this needle
        """
        needle = self[needle]  # make sure needle instance is the one in the machine bed state
        assert 0 <= needle.position < self.needle_count, f"Cannot place a loop at position {needle.position}"
        assert not (drop_prior_loops and needle.is_slider), "Cannot knit on slider needle"
        if drop_prior_loops:
            assert needle.is_clear(self), "Cannot drop loops if needle is not clear"
            self.drop(needle)
        needle.add_loops(loops)
        if isinstance(needle, Slider_Needle):
            self._active_sliders.add(needle)
        for loop in loops:
            self.loops_to_needle[loop] = needle
        return loops

    def drop(self, needle: Needle) -> List[Loop]:
        """
        Clears the loops held at this position as though a drop operation has been done
        :param needle: The position to drop loops from main and slider needles
        :return list of loops that were dropped
        """
        needle = self[needle]  # make sure the correct needle instance in machine bed state is used
        loops = [l for l in needle.held_loops]
        for loop in needle.held_loops:
            self.loops_to_needle[loop] = None
        needle.drop()
        return loops

    def __getitem__(self, item: Needle) -> Needle:
        """
        Gets an indexed needle on the bed
        :param item: the needle position to get a loop from
        :return: the loop_id held at that position
        """
        if item.is_slider:
            return self.sliders[item.position]
        else:
            return self.needles[item.position]

    def get_needle_of_loop(self, loop: Loop) -> Optional[Needle]:
        """
        Gets the needle that currently holds the loop
        :param loop: the loop being searched for
        :return: None if the bed does not hold the loop, otherwise the needle position that holds it
        """
        if loop not in self.loops_to_needle:
            return None
        else:
            return self.loops_to_needle[loop]

    def sliders_are_clear(self):
        """
        :return: True if no loops are on a slider needle
        """
        return len(self._active_sliders) == 0
