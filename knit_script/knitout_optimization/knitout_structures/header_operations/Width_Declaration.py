from knit_script.knitout_optimization.knitout_structures.header_operations.Header_Declaration import Header_Declaration, Header_Operation


class Width_Declaration(Header_Declaration):

    def __init__(self, w: int):
        super().__init__(Header_Operation.Width)
        self.w = w

    def __str__(self):
        return f";;{self.operation}: {self.w};{self.comment_str}\n"
