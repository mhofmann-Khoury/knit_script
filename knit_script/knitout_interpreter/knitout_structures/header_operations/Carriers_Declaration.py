from typing import Optional

from knit_script.knitting_machine.machine_specification.Header_ID import Header_ID
from knit_script.knitout_interpreter.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set


class Carriers_Declaration(Header_Declaration):
    def __init__(self, carrier_set: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Header_ID.Carrier_Count, comment)
        assert carrier_set[0] == 1, f"Carriers must start from 1"
        for c1, c2 in zip(carrier_set[:-1], carrier_set[1:]):
            assert c1 + 1 == c2, f"Carriers must be in order"
        self.carrier_set = carrier_set

    @property
    def carrier_count(self) -> int:
        """
        :return: number of carriers declared
        """
        return len(self.carrier_set)

    def __str__(self):
        return f";;{self.operation}: {self.carrier_set}{self.comment_str}"

    def add_to_header(self, header) -> bool:
        if header.overwriting_declaration(self):
            assert header.carrier_count == self.carrier_count, f"Cannot have two carrier sets: {self}"
            return False
        else:
            header.set_value(self.operation, self.carrier_count)
            return True
