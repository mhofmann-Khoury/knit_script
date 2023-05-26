from knit_script.knitout_optimization.knitout_structures.header_operations.Header_Declaration import Header_Declaration, Header_Operation
from knit_script.knitting_machine.machine_components.machine_position import Machine_Position


class Position_Declaration(Header_Declaration):
    def __init__(self, position: str):
        super().__init__(Header_Operation.Position)
        self.position: Machine_Position = Machine_Position[position]

    def __str__(self):
        return f";;{self.operation}: {self.position.value};{self.comment_str}\n"
