from typing import Optional

from knit_script.knit_script_interpreter.header_structure import Machine_Type, Header_ID, Header
from knit_script.knitout_optimization.knitout_structures.header_operations.Header_Declaration import Header_Declaration


class Machine_Declaration(Header_Declaration):
    def __init__(self, machine: str, comment: Optional[str] = None):
        super().__init__(Header_ID.Machine, comment)
        assert machine in Machine_Type, f"{machine} is not a supported machine type"
        self.machine = machine

    def __str__(self):
        return f";;{self.operation}: {self.machine}{self.comment_str}"

    def add_to_header(self, header: Header) -> bool:
        if header.overwriting_declaration(self):
            assert header.machine_type == self.machine, f"Cannot have two Machine Types: {self}"
            return False
        else:
            header.set_value(self.operation, self.machine)
            return True
