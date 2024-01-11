from typing import List

from knit_script.Knit_Errors.Knit_Script_Error import Knit_Script_Error
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set


class Duplicate_Carrier_Error(Knit_Script_Error):
    """
        Error for reporting that a carrier is used twice in a carrier declaration
    """

    def __init__(self, carrier: int):
        self._carrier: int = carrier
        super().__init__(self._message())

    @property
    def carrier(self) -> int:
        """
        :return: The carrier that errored
        """
        return self._carrier

    def _message(self) -> str:
        return f"Duplicate carrier declared: {self._carrier} "  # todo: error management that tracks line numbers


class No_Declared_Carrier_Error(Knit_Script_Error):
    """
        Error for reporting that no working carrier has been declared
    """

    def __init__(self):
        super().__init__(self._message())

    @staticmethod
    def _message() -> str:
        return "No working carriers is declared"


class Non_Existent_Carrier_Error(Knit_Script_Error):
    """Raised when using a carrier that is not available on the machine"""

    def __init__(self, carrier: int):
        self._carrier: int = carrier
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



class Inactive_Carrier_Error(Knit_Script_Error):
    """Raised when attempting to use a carrier that is not active"""

    def __init__(self, carrier_set: Carrier_Set, missing_carriers: List[int], instruction=None):
        self.missing_carriers = missing_carriers
        self._carrier_set: Carrier_Set = carrier_set
        self._instruction = instruction
        super().__init__(self._message())

    @property
    def carrier_set(self) -> Carrier_Set:
        """
        :return: the inactive carrier set
        """
        return self._carrier_set

    @property
    def instruction(self):
        """
        :return: the instruction type that cannot be completed
        """
        return self._instruction

    def _message(self) -> str:
        if self._instruction is not None:
            return f"Cannot \'{self._instruction}\' with inactive carriers {self.missing_carriers}"
        else:
            return f"Carriers {self.missing_carriers} in carrier set {self._carrier_set} are not active and cannot be used"
