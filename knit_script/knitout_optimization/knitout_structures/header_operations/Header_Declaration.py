from enum import Enum
from typing import Optional


class Header_Operation(Enum):
    """
        Header operations
    """
    Machine = "Machine"
    Gauge = "Gauge"
    Yarn = "Yarn"
    Carriers = "Carriers"
    Position = "Position"
    Width = "Width"
    X = "X-"

    def __str__(self):
        return self.value


class Header_Declaration:
    """
        Super class of all header operations in knitout
    """

    def __init__(self, op_name: Header_Operation):
        self.comment = None
        self.operation = op_name

    @property
    def has_comment(self) -> bool:
        """
        :return: True if comment is present
        """
        return self.comment is not None

    @property
    def comment_str(self) -> str:
        """
        :return: comment as a string
        """
        if not self.has_comment:
            return ""
        else:
            return self.comment

    def __str__(self):
        return f";;{self.operation}{self.comment_str}"

    def __repr__(self):
        return str(self)
