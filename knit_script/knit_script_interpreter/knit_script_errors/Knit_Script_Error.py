
class Knit_Script_Error(Exception):
    """
        Super class for all knit script specific errors
    """
    def __init__(self, message: str):
        super().__init__(f"Knit Script raised a {self.__class__.__name__}:\n\t{message}")
        self._message:str = message

    @property
    def message(self) -> str:
        """
        :return: the message to report with the error
        """
        return self._message