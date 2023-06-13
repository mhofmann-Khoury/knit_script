from knit_script.knitout_optimization.knitout_errors.Knitout_Error import Ignorable_Knitout_Error


class In_Active_Carrier_Error(Ignorable_Knitout_Error):

    def __init__(self, carrier: int):
        self._carrier: int = carrier
        super().__init__(self._message())

    def _message(self) -> str:
        return f"Cannot bring in {self._carrier} because it is already active"


class Releasehook_Unhooked_Carrier(Ignorable_Knitout_Error):

    def __init__(self, carrier: int):
        self._carrier: int = carrier
        super().__init__(self._message())

    def _message(self) -> str:
        return f"Cannot releasehook {self._carrier} because it is not on the inserting hook"


class Out_Inactive_Carrier_Error(Ignorable_Knitout_Error):

    def __init__(self, carrier: int):
        self._carrier: int = carrier
        super().__init__(self._message())

    def _message(self) -> str:
        return f"Cannot bring out {self._carrier} because it is not active"
