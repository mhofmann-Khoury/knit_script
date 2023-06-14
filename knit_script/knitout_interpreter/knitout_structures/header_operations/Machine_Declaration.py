from typing import Optional

from knit_script.knitout_interpreter.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitting_machine.machine_specification.Header_ID import Header_ID
from knit_script.knitting_machine.machine_specification.Machine_Type import Machine_Type


class Machine_Declaration(Header_Declaration):
    def __init__(self, machine: str, comment: Optional[str] = None):
        super().__init__(Header_ID.Machine, comment)
        try:
            _ = Machine_Type[machine]
        except KeyError:
            assert False, f"{machine} is not a supported machine type"
        self.machine = machine

    def __str__(self):
        return f";;{self.operation}: {self.machine}{self.comment_str}"

    def add_to_header(self, header) -> bool:
        if header.overwriting_declaration(self):
            assert header.machine_type.value == self.machine, f"Cannot have two Machine Types: {self}"
            return False
        else:
            header.set_value(self.operation, self.machine)
            return True
