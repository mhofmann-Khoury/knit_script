from knit_script.Knit_Errors.Knit_Script_Error import Knit_Script_Error
from knit_script.Knit_Errors.Knitout_Error import Knitout_Error
from knit_script.knitting_machine.machine_components.needles import Needle
from knit_script.knitting_machine.machine_components.yarn_management.Carrier import Carrier


class Long_Float_Error(Knitout_Error):

    def __init__(self, start_position: int | Needle, end_position: int | Needle, carrier: Carrier, max_float: int, knitout_instruction=None):
        self.carrier = carrier
        self.max_float = max_float
        self.start_position = start_position
        self.end_position = end_position
        super().__init__(self._message(), knitout_instruction)

    def _message(self) -> str:
        float_length = abs(int(self.end_position) - int(self.start_position))
        return f"Long float  of carrier {self.carrier} (i.e., >{self.max_float}) of {float_length} between {self.start_position} and {self.end_position}"


class Slider_Use_Error(Knitout_Error):

    def __init__(self, needle: Needle, knitout_instruction=None):
        self.needle = needle
        super().__init__(self._message(), knitout_instruction)

    def _message(self) -> str:
        return f"Cannot make loops on slider needle {self.needle}"


class Slider_Clear_Error(Knitout_Error):
    def __init__(self, needle: Needle, knitout_instruction=None):
        self.needle = needle
        super().__init__(self._message(), knitout_instruction)

    def _message(self) -> str:
        return f"Cannot transfer to slider needle {self.needle} because it is not clear"


class Blocked_Sliders_Error(Knitout_Error):

    def __init__(self, knitout_instruction=None):
        super().__init__(self._message(), knitout_instruction)

    @staticmethod
    def _message() -> str:
        return f"Sliders are blocked"


class Same_Bed_Transfer_Error(Knitout_Error):
    def __init__(self, start: Needle, target: Needle, knitout_instruction=None):
        self.target = target
        self.start = start
        super().__init__(self._message(), knitout_instruction)

    def _message(self) -> str:
        return f"Cannot transfer from {self.start} to {self.target} because they are on the same bed"


class Valid_Rack_Error(Knitout_Error):
    def __init__(self, start: Needle, target: Needle, current_rack: float, knitout_instruction=None):
        self.current_rack = current_rack
        self.target = target
        self.start = start
        super().__init__(self._message(), knitout_instruction)

    def _message(self) -> str:
        return f"Cannot transfer from {self.start} to {self.target} at rack of {self.current_rack}"


class Incompatible_Carriage_Pass_Operations(Knit_Script_Error):

    def __init__(self, first_instruction, second_instruction):
        self.second_instruction = second_instruction
        self.first_instruction = first_instruction
        super().__init__(self._message())

    def _message(self) -> str:
        return f"Cannot {self.first_instruction} and {self.second_instruction} in same carriage pass"


class Instructions_Require_Direction(Knit_Script_Error):

    def __init__(self, instruction):
        self.instruction = instruction
        super().__init__(self._message())

    def _message(self) -> str:
        return f"Cannot {self.instruction} without declaring a direction"


class Repeated_Needle_In_Pass(Knit_Script_Error):

    def __init__(self, needle):
        self.needle = needle
        super().__init__(self._message())

    def _message(self) -> str:
        return f"Cannot work on {self.needle} more than once in a carriage pass."


class All_Needle_Operation_Error(Knitout_Error):

    def __init__(self, first_needle, second_needle, instruction):
        self.first_needle = first_needle
        self.second_needle = second_needle
        self.instruction = instruction
        super().__init__(self._message())

    def _message(self) -> str:
        return f"Cannot {self.instruction} on {self.first_needle} and {self.second_needle} at All-Needle racking."
