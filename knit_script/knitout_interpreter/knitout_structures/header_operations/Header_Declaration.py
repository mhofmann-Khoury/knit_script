from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Knitout_Line
from knit_script.knitting_machine.machine_specification.Header_ID import Header_ID


class Header_Declaration(Knitout_Line):
    """
        Superclass of all header operations in knitout
    """

    def __init__(self, op_name: Header_ID, comment: None | str):
        super().__init__(comment)
        self.operation = op_name

    def __str__(self):
        return f";;{self.operation}{self.comment_str}"

    def add_to_header(self, header) -> bool:
        """
        update the header or redundancy error
        :param header: header to check against
        :return: True if header is updated
        """
        return False
