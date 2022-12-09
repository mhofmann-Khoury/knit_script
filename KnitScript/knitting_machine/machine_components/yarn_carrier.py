"""
    Representation of a Yarn Carrier on the machine
"""
from typing import Union, List, Optional

from KnitScript.knit_graphs.Knit_Graph import Knit_Graph
from KnitScript.knit_graphs.Loop import Loop

from KnitScript.knit_graphs.Yarn import Yarn


class Yarn_Carrier:
    """
    A structure to represent the location of a Yarn_carrier
    ...

    Attributes
    ----------
    loops_since_release: int
        The number of loops that have been made with carrier since a release hook was called
        Stays 0 when not on the yarn inserting hook
    """

    def __init__(self, carrier_ids: Union[int, List[int]] = 3, carrier_name: Optional[str] = None):
        """
        Represents the state of the yarn_carriage
        :param carrier_name:
        :param carrier_ids: The carrier_id for this yarn
        """
        if carrier_name is None:
            carrier_name = f"C{carrier_ids}"
        self._carrier_ids: List[int] = carrier_ids
        if isinstance(self._carrier_ids, int):
            self._carrier_ids = [carrier_ids]
        if self._many_yarns:
            for carrier in self.carrier_ids:
                assert 1 <= carrier <= 10, f"Carriers must between 1 and 10, but got {carrier}"
        else:
            assert 1 <= carrier_ids <= 10, f"Carriers must between 1 and 10, but got {carrier_ids}"
        # self._position: int = position
        self._yarns: List[Yarn] = [Yarn(f"{carrier_name}.{cid}") for cid in self.carrier_ids]
        self.loops_since_release: int = 0

    def create_loops(self, knit_graph:Knit_Graph) -> List[Loop]:
        """
        Creates a list of loops from the yarns in the carrier set
        :param knit_graph: the KnitGraph to add the loops to
        :return: the loops
        """
        self.loops_since_release += 1
        return [y.add_loop_to_end(knit_graph=knit_graph)[1] for y in self._yarns]

    def release_carrier(self):
        """
            Sets the carrier as being released from yarn inserting hook
        """
        self.loops_since_release = 0

    # @property
    # def position(self):
    #     """
    #     :return: The current needle position the carrier is sitting at
    #     """
    #     return self._position

    @property
    def carrier_ids(self) -> List[int]:
        """
        :return: the id of this carrier
        """
        return self._carrier_ids

    # def move_to_position(self, new_position: int):
    #     """
    #     Updates the structure as though the yarn carrier took a pass at the needle location
    #     :param new_position: the needle to move to
    #     """
    #     self._position = new_position

    @property
    def _many_yarns(self) -> bool:
        """
        :return: True if this carrier involves multiple carriers
        """
        return type(self.carrier_ids) == list

    def __str__(self):
        if not self._many_yarns:
            return " " + str(self.carrier_ids)
        else:
            carriers = ""
            for carrier in self.carrier_ids:
                carriers += f" {carrier}"
            return carriers

    def __repr__(self):
        return str(self)

    def __hash__(self):
        if self._many_yarns:
            hash_val = 0
            for i, carrier in enumerate(self.carrier_ids):
                hash_val += (10 ** i) * carrier  # gives unique hash for list of different orders
            return hash_val
        else:
            return self.carrier_ids

    def __eq__(self, other):
        if isinstance(other, Yarn_Carrier):
            return hash(self) == hash(other)
        return False

    def __iter__(self):
        if self._many_yarns:
            return iter(self.carrier_ids)
        else:
            return iter([self.carrier_ids])
