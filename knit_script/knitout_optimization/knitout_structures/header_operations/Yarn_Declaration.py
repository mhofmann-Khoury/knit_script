from typing import Tuple

from knit_script.knitout_optimization.knitout_structures.header_operations.Header_Declaration import Header_Declaration, Header_Operation


class Yarn_Declaration(Header_Declaration):
    def __init__(self, carrier: int, yarn_type: Tuple[int, int], color: str):
        super().__init__(Header_Operation.Yarn)
        self.carrier = carrier
        self.color = color
        self.yarn_type = yarn_type

    def __str__(self):
        return f";;{self.operation}-{self.carrier}: {self.yarn_type[0]}-{self.yarn_type[1]} {self.color};{self.comment_str}\n"
