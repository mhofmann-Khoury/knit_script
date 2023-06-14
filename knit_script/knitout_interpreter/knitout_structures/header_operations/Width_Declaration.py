from typing import Optional

from knit_script.knitout_interpreter.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitting_machine.machine_specification.Header_ID import Header_ID


class Width_Declaration(Header_Declaration):

    def __init__(self, width: int, comment: Optional[str] = None):
        super().__init__(Header_ID.Width, comment)
        self.width = width

    def __str__(self):
        return f";;{self.operation}: {self.width}{self.comment_str}"

    def add_to_header(self, header) -> bool:

        if header.overwriting_declaration(self):
            assert header.width == self.width, f"Cannot have two Widths: {self}"
            return False
        else:
            header.set_value(self.operation, self.width)
            return True
