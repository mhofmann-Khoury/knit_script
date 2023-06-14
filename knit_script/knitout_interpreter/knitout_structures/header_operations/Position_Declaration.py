from typing import Optional

from knit_script.knitout_interpreter.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitting_machine.machine_components.machine_position import Machine_Position
from knit_script.knitting_machine.machine_specification.Header_ID import Header_ID


class Position_Declaration(Header_Declaration):
    def __init__(self, position: str, comment: Optional[str] = None):
        super().__init__(Header_ID.Position, comment)
        self.position: Machine_Position = Machine_Position[position]

    def __str__(self):
        return f";;{self.operation}: {self.position.value}{self.comment_str}"

    def add_to_header(self, header) -> bool:
        if header.overwriting_declaration(self):
            assert header.position == self.position, f"Cannot have two Positions: {self}"
            return False
        else:
            header.set_value(self.operation, self.position)
            return True
