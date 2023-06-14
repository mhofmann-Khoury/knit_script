from typing import Optional

from knit_script.knitout_interpreter.knitout_structures.header_operations.Header_Declaration import Header_Declaration
from knit_script.knitting_machine.machine_specification.Header_ID import Header_ID


class Header_Extension_Declaration(Header_Declaration):
    def __init__(self, code: str, comment: Optional[str] = None):
        super().__init__(Header_ID.X, comment)
        self.code = code

    def __str__(self):
        return f"{self.operation}{self.code}{self.comment_str}"

    def add_to_header(self, header) -> bool:
        """
        update the header or redundancy error
        :param header: header to check against
        :return: True if header is updated
        """
        header.extensions.append(self.code)
        return True
