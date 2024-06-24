"""Base class for Knitout Lines of code"""
from typing import Optional


class Knitout_Line:
    """
        General class for lines of knitout
    """

    def __init__(self, comment: Optional[str]):
        self.comment = comment
        self.original_line_number: Optional[int] = None
        self.follow_comments: list[Comment_Line] = []

    def add_follow_comment(self, comment_line):
        """
        Adds comment line to comments that follow this line
        :param comment_line:
        """
        self.follow_comments.append(comment_line)

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
            return "\n"
        else:
            return f";{self.comment}\n"

    def execute(self, machine_state) -> bool:
        """
        Executes the instruction on the machine state.
        :param machine_state: The machine state to update.
        :return: True if the process completes an update.
        """
        return False

    def __str__(self):
        return self.comment_str

    def id_str(self) -> str:
        """
        :return: string with original line number added if present
        """
        if self.original_line_number is not None:
            return f"{self.original_line_number}:{self}"
        else:
            return str(self)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        if self.original_line_number is None:
            if other.original_line_number is None:
                return False
            else:
                return True
        else:
            return self.original_line_number < other.original_line_number

    def __hash__(self):
        if self.original_line_number is None:
            return hash(str(self))
        else:
            return self.original_line_number


class Version_Line(Knitout_Line):

    def __init__(self, version: int, comment: Optional[str] = None):
        super().__init__(comment)
        self.version = version

    def __str__(self):
        return f";!knitout-{self.version}{self.comment_str}"


class Comment_Line(Knitout_Line):
    def __init__(self, comment: Optional[str]):
        super().__init__(comment)
