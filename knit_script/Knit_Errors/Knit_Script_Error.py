import os

from knit_script.Knit_Errors.Knitout_Error import Knitout_Error


class Knit_Script_Error(Exception):
    """
        Super class for all knit script specific errors
    """

    def __init__(self, message: str):
        super().__init__(f"Knit Script raised a {self.__class__.__name__}:{os.linesep}\t{message}")
        self._message: str = message

    @property
    def message(self) -> str:
        """
        :return: the message to report with the error
        """
        return self._message


class KnitScript_Knitout_Error(Knit_Script_Error):

    def __init__(self, knitout_error: Knitout_Error):
        self.knitout_error = knitout_error
        super().__init__(self.knitout_error.message)
