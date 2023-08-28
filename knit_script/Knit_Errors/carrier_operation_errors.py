from knit_script.Knit_Errors.Knitout_Error import Ignorable_Knitout_Error, Knitout_Error


class In_Active_Carrier_Error(Ignorable_Knitout_Error):

    def __init__(self, carrier: int, knitout_instruction=None):
        self._carrier: int = carrier
        super().__init__(self._message(), knitout_instruction)

    def _message(self) -> str:
        return f"Cannot bring in {self._carrier} because it is already active"


class Inserting_Hook_In_Use_Error(Knitout_Error):

    def __init__(self, knitout_instruction=None):
        super().__init__(self._message(), knitout_instruction)

    @staticmethod
    def _message() -> str:
        return f"Cannot use yarn inserting hook because it is already in use."


class Releasehook_Unhooked_Carrier(Ignorable_Knitout_Error):

    def __init__(self, carrier: int, knitout_instruction=None):
        self._carrier: int = carrier
        super().__init__(self._message(), knitout_instruction)

    def _message(self) -> str:
        return f"Cannot releasehook {self._carrier} because it is not on the inserting hook"


class Out_Inactive_Carrier_Error(Ignorable_Knitout_Error):

    def __init__(self, carrier: int, knitout_instruction=None):
        self._carrier: int = carrier
        super().__init__(self._message(), knitout_instruction)

    def _message(self) -> str:
        return f"Cannot bring out {self._carrier} because it is not active"


class Out_Hooked_Carrier_Error(Knitout_Error):

    def __init__(self, carrier: int, knitout_instruction=None):
        self._carrier: int = carrier
        super().__init__(self._message(), knitout_instruction)

    def _message(self) -> str:
        return f"Cannot take {self._carrier} out because it is on the yarn inserting hook"


class Cut_Hooked_Carrier_Error(Knitout_Error):

    def __init__(self, carrier: int, knitout_instruction=None):
        self._carrier: int = carrier
        super().__init__(self._message(), knitout_instruction)

    def _message(self) -> str:
        return f"Cannot cut {self._carrier} out because it is on the yarn inserting hook"
