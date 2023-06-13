from enum import Enum


class Header_ID(Enum):
    """
        Values that can be updated in header
    """
    Machine = "Machine"
    Width = "Width"
    Gauge = "Gauge"
    Carrier_Count = "Carriers"
    Position = "Position"
    Rack = "Rack"
    Hook = "Hook"
    Yarn = "Yarn"
    X = "X-"

    def __str__(self):
        return self.value
