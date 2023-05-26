from typing import Optional

from knit_script.knitout_optimization.knitout_structures.header_operations.Header_Declaration import Header_Declaration, Header_Operation


class Gauge_Declaration(Header_Declaration):
    def __init__(self, gauge: int):
        super().__init__(Header_Operation.Gauge)
        self.gauge = gauge

    def __str__(self):
        return f";;{self.operation}: {self.gauge};{self.comment_str}\n"
