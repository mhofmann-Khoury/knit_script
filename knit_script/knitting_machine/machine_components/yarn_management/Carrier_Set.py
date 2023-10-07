"""
    Representation of a Yarn Carrier on the machine
"""
from typing import Union, List, Optional

from knit_script.knit_graphs.Knit_Graph import Knit_Graph
from knit_script.knit_graphs.Loop import Loop
from knit_script.knitting_machine.machine_components.yarn_management.Carrier import Carrier


class Carrier_Set:
    """
    A structure to represent the location of a Yarn_carrier
    ...

    Attributes
    ----------
    """

    def __init__(self, carrier_ids: Union[int, list[Union[int]]] = 3):
        """
        Represents the state of the yarn_carriage
        :param carrier_ids: The carrier_id for this yarn
        """
        if isinstance(carrier_ids, int):
            self._carrier_ids = [carrier_ids]
        elif isinstance(carrier_ids, Carrier_Set):
            self._carrier_ids = [*carrier_ids._carrier_ids]
        else:  # list or carriers or integers
            duplicates = set()
            self._carrier_ids = []
            for c in carrier_ids:
                if isinstance(c, int):
                    if c in duplicates:
                        print(f"KnitScript Warning: Ignoring duplicate carrier in carrier set {c}")
                    else:
                        duplicates.add(c)
                        self._carrier_ids.append(c)
                else:
                    assert isinstance(c, Carrier_Set)
                    for c_id in c._carrier_ids:
                        if c_id in duplicates:
                            print(f"KnitScript Warning: Ignoring duplicate carrier in carrier set {c}")
                        else:
                            duplicates.add(c_id)
                            self._carrier_ids.append(c_id)
        # todo parameter carrier spacing by machine type

    def set_position(self, carrier_system, position: Optional[int]):
        """
        Sets the position of each carrier in the set
        :param carrier_system: the carrier system to get carriers from
        :param position: the position to set to
        """
        for carrier in self.get_carriers(carrier_system):
            carrier.position = position

    def get_carriers(self, carrier_system) -> List[Carrier]:
        """
        :param carrier_system: carrier system referenced by set
        :return: carriers that correspond to the ids in the carrier set
        """
        return [carrier_system[cid] for cid in self.carrier_ids]

    def create_loops(self, knit_graph: Knit_Graph, carrier_system) -> List[Loop]:
        """
        Creates a list of loops from the yarns in the carrier set
        :param carrier_system:
        :param knit_graph: The KnitGraph to add the loops to
        :return: the loops
        """
        carriers = self.get_carriers(carrier_system)
        loops = [carrier.yarn.add_loop_to_end(knit_graph=knit_graph)[1] for carrier in carriers]
        for carrier in carriers:
            carrier.count_loop()
        return loops

    def release_carriers(self, carrier_system):
        """
            Sets the carrier as being released from yarn inserting hook
            :param carrier_system:
        """
        for carrier in self.get_carriers(carrier_system):
            carrier.releasehook()

    @property
    def carrier_ids(self) -> List[int]:
        """
        :return: the id of this carrier
        """
        return self._carrier_ids

    @property
    def many_carriers(self) -> bool:
        """
        :return: True if this carrier involves multiple carriers
        """
        return len(self.carrier_ids) > 1

    def __str__(self):
        carriers = str(self.carrier_ids[0])
        for cid in self.carrier_ids[1:]:
            carriers += f" {cid}"
        return carriers

    def __repr__(self):
        return str(self)

    def __hash__(self):
        if self.many_carriers:
            hash_val = 0
            for i, carrier in enumerate(self.carrier_ids):
                hash_val += (10 ** i) * carrier  # gives unique hash for a list of different orders
            return hash_val
        else:
            return self.carrier_ids[0]

    def __eq__(self, other):
        if isinstance(other, Carrier_Set):
            return hash(self) == hash(other)
        return False

    def __iter__(self):
        return iter(self.carrier_ids)

    def __getitem__(self, item: int):
        return self.carrier_ids[item]

    def __len__(self):
        return len(self.carrier_ids)

    @property
    def carrier_count(self) -> int:
        """
        :return: number of carriers
        """
        return len(self)

    def carrier_DAT_ID(self) -> int:
        """
        :return: Number used in DAT files to represent the carrier set
        """
        carrier_id = 0
        for place, carrier in enumerate(reversed(self.carrier_ids)):
            multiplier = 10 ** place
            carrier_val = multiplier * carrier
            carrier_id += carrier_val
        return carrier_id

    @staticmethod
    def carrier_set_by_count(carrier_count: int = 10):
        """
        :param carrier_count: the number of carriers in the carrier set
        :return: a carrier set of that size
        """
        return Carrier_Set([i for i in range(1, carrier_count + 1)])
