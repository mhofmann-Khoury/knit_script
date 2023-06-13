class Knitout_Error(Exception):
    """
        Super class for all knit script specific errors
    """

    def __init__(self, message: str, can_ignore_operation=False):
        super().__init__(f"Knitout raised a {self.__class__.__name__}:\n\t{message}")
        self._can_ignore_operation = can_ignore_operation
        self._message: str = message

    @property
    def can_ignore_operation(self) -> bool:
        return self._can_ignore_operation

    @property
    def message(self) -> str:
        """
        :return: the message to report with the error
        """
        return self._message


class Ignorable_Knitout_Error(Knitout_Error):

    def __init__(self, message: str):
        super().__init__(message, True)
