from typing import Optional

from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction, Instruction_Type
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set


class Carrier_Instruction(Instruction):

    def __init__(self, instruction_type: Instruction_Type, cs: Carrier_Set, comment: Optional[str]):
        super().__init__(instruction_type, comment)
        self.carrier_set = cs

    def __str__(self):
        return f"{self.instruction_type} {self.carrier_set}{self.comment_str}"


class Hook_Instruction(Carrier_Instruction):

    def __init__(self, instruction_type: Instruction_Type, cs: Carrier_Set, comment: Optional[str]):
        super().__init__(instruction_type, cs, comment)


class In_Instruction(Carrier_Instruction):

    def __init__(self, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.In, cs, comment)

    def execute(self, machine_state):
        machine_state.bring_in(self.carrier_set)


class Inhook_Instruction(Hook_Instruction):

    def __init__(self, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Inhook, cs, comment)

    def execute(self, machine_state):
        machine_state.in_hook(self.carrier_set)


class Releasehook_Instruction(Hook_Instruction):

    def __init__(self, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Releasehook, cs, comment)

    def execute(self, machine_state):
        hooked_carriers = machine_state.carrier_system.hooked_carriers
        assert hooked_carriers == self.carrier_set, f"Cannot release hook {self.carrier_set} because currently hooked carriers are {hooked_carriers}"
        machine_state.release_hook()


class Out_Instruction(Carrier_Instruction):

    def __init__(self, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Out, cs, comment)

    def execute(self, machine_state):
        machine_state.out(self.carrier_set)


class Outhook_Instruction(Hook_Instruction):

    def __init__(self, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Outhook, cs, comment)

    def execute(self, machine_state):
        machine_state.out_hook(self.carrier_set)
