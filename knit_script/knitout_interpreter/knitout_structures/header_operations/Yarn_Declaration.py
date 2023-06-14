from typing import Optional

from knit_script.knit_graphs.Yarn import Yarn
from knit_script.knitout_interpreter.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitting_machine.machine_specification.Header_ID import Header_ID


class Yarn_Declaration(Header_Declaration):
    def __init__(self, carrier: int, size: int, plies: int, color: str, comment: Optional[str] = None):
        super().__init__(Header_ID.Yarn, comment)
        self.size = size
        self.plies = plies
        self.carrier = carrier
        self.color = color

    def __str__(self):
        return f";;{self.operation}-{self.carrier}: {self.size}-{self.plies} {self.color}{self.comment_str}"

    def add_to_header(self, header) -> bool:
        header.carriers_to_yarns[self.carrier] = self.yarn()
        return True

    def yarn(self) -> Yarn:
        """
        :return: Specified yarn for carrier
        """
        return Yarn.yarn_by_type(self.color, size=self.size, plies=self.plies)
