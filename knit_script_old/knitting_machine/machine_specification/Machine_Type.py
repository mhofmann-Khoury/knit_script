from enum import Enum


class Machine_Type(Enum):
    """
        Accepted Machine specifications
    """
    SWG091N2 = 'SWG091N2'

    def __str__(self):
        return self.value

