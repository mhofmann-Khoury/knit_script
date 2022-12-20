"""
    Representation of a Yarn Carrier on the machine
"""
from typing import Union, List, Optional

from knit_script.knit_graphs.Knit_Graph import Knit_Graph
from knit_script.knit_graphs.Loop import Loop

from knit_script.knit_graphs.Yarn import Yarn
from knit_script.knit_script_interpreter.knit_script_errors.yarn_management_errors import Duplicate_Carrier_Error, Non_Existent_Carrier_Error


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

    def __init__(self, carrier_ids: Union[int, List[Union[int]]] = 3, carrier_name: Optional[str] = None):
        """
        Represents the state of the yarn_carriage
        :param carrier_name:
        :param carrier_ids: The carrier_id for this yarn
        """
        if carrier_name is None:
            carrier_name = f"C{carrier_ids}"
        if isinstance(carrier_ids, int):
            self._carrier_ids = [carrier_ids]
        elif isinstance(carrier_ids, Yarn_Carrier):
            self._carrier_ids = [*carrier_ids._carrier_ids]
        else: # list or carriers or integers
            duplicates = set()
            self._carrier_ids = []
            for c in carrier_ids:
                if isinstance(c, int):
                    if c in duplicates:
                        raise Duplicate_Carrier_Error(c)
                    duplicates.add(c)
                    self._carrier_ids.append(c)
                else:
                    assert isinstance(c, Yarn_Carrier)
                    for c_id in c._carrier_ids:
                        if c_id in duplicates:
                            raise Duplicate_Carrier_Error(c_id)
                        duplicates.add(c_id)
                        self._carrier_ids.append(c_id)
        for carrier in self.carrier_ids:
            if not (1 <= carrier <= 10):
                raise Non_Existent_Carrier_Error(carrier)
            assert 1 <= carrier <= 10, f"Carriers must between 1 and 10, but got {carrier}"
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

    @property
    def carrier_ids(self) -> List[int]:
        """
        :return: the id of this carrier
        """
        return self._carrier_ids

    @property
    def many_yarns(self) -> bool:
        """
        :return: True if this carrier involves multiple carriers
        """
        return len(self.carrier_ids) > 1

    def __str__(self):
        carriers = ""
        for carrier in self.carrier_ids:
            carriers += f" {carrier}"
        return carriers

    def __repr__(self):
        return str(self)

    def __hash__(self):
        if self.many_yarns:
            hash_val = 0
            for i, carrier in enumerate(self.carrier_ids):
                hash_val += (10 ** i) * carrier  # gives unique hash for list of different orders
            return hash_val
        else:
            return self.carrier_ids[0]

    def __eq__(self, other):
        if isinstance(other, Yarn_Carrier):
            return hash(self) == hash(other)
        return False

    def __iter__(self):
        return iter(self.carrier_ids)
