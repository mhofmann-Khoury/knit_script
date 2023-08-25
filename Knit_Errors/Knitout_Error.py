import os


class Knitout_Error(Exception):
    """
        Super class for all knit script specific errors
    """

    def __init__(self, message: str, knitout_instruction=None, can_ignore_operation=False):
        from_str = ""
        if knitout_instruction is not None:
            from_str = f" from {knitout_instruction}"
        super().__init__(f"Knitout raised a {self.__class__.__name__}:{os.linesep}\t{message}{from_str}")
        self.knitout_instruction = knitout_instruction
        self._can_ignore_operation = can_ignore_operation
        self._message: str = message

    @property
    def can_ignore_operation(self) -> bool:
        """
        :return: True if the operation can be ignored to resolve the error.
        """
        return self._can_ignore_operation

    @property
    def message(self) -> str:
        """
        :return: the message to report with the error
        """
        return self._message


class Ignorable_Knitout_Error(Knitout_Error):

    def __init__(self, message: str, knitout_instruction=None):
        super().__init__(message, knitout_instruction, True)
