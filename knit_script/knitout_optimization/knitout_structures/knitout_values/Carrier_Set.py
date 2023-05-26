"""Carrier Set structure for Knitout Parsing"""
from typing import Union, List


class Carrier_Set:
    """
        Structure for a set of carriers
    """
    def __init__(self, carriers: List[Union[int, str]]):
        assert len(carriers) > 0
        self.carriers = carriers

    def __str__(self):
        s = str(self.carriers[0])
        for c in self.carriers[1:]:
            s += f" {c}"
        return s
