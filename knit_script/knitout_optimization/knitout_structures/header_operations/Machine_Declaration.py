from knit_script.knitout_optimization.knitout_structures.header_operations.Header_Declaration import Header_Declaration, Header_Operation


class Machine_Declaration(Header_Declaration):
    def __init__(self, machine: str):
        super().__init__(Header_Operation.Machine)
        self.machine = machine

    def __str__(self):
        return f";;{self.operation}: {self.machine};{self.comment_str}\n"
