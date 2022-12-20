from knit_script.knit_script_interpreter.knit_script_errors.Knit_Script_Error import Knit_Script_Error


class Duplicate_Carrier_Error(Knit_Script_Error):
    """
        Error for reporting that a carrier is used twice in a carrier declaration
    """
    def __init__(self, carrier: int):
        self._carrier:int = carrier
        super().__init__(self._message())

    @property
    def carrier(self) -> int:
        """
        :return: The carrier that errored
        """
        return self._carrier
    def _message(self) -> str:
        return f"Duplicate carrier declared: {self._carrier} "# todo: error management that tracks line numbers


class Non_Existent_Carrier_Error(Knit_Script_Error):
    """Raised when using a carrier that is not available on the machine"""
    def __init__(self, carrier: int):
        self._carrier:int = carrier
        super().__init__(self._message())

    @property
    def carrier(self) -> int:
        """
        :return: THe carrier that errored
        """
        return self._carrier

    def _message(self) -> str:
        if self.carrier < 1:
            return f"Carriers must be 1 or greater, but got {self.carrier}"
        return f"Carrier {self.carrier} is not available on the declared machine. "