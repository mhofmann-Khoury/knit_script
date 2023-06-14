from typing import Optional

from knit_script.knitout_interpreter.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitting_machine.machine_specification.Header_ID import Header_ID


class Gauge_Declaration(Header_Declaration):
    def __init__(self, gauge: int, comment: Optional[str] = None):
        super().__init__(Header_ID.Gauge, comment)
        self.gauge = gauge

    def __str__(self):
        return f";;{self.operation}: {self.gauge}{self.comment_str}"

    def add_to_header(self, header) -> bool:
        if header.overwriting_declaration(self):
            assert header.gauge == self.gauge, f"Cannot have two Gauges: {self}"
            return False
        else:
            header.set_value(self.operation, self.gauge)
            return True
