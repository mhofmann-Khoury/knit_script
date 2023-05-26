from knit_script.knitout_optimization.knitout_structures.header_operations.Header_Declaration import Header_Declaration, Header_Operation


class Header_Extension_Declaration(Header_Declaration):
    def __init__(self, code: str):
        super().__init__(Header_Operation.X)
        self.code = code

    def __str__(self):
        return f"{self.operation}{self.code};{self.comment_str}\n"
