from typing import Optional

from knit_script.knitout_optimization.knitout_structures.knitout_instructions.instruction import Instruction, Instruction_Type
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set


class Carrier_Instruction(Instruction):

    def __init__(self, instruction_type: Instruction_Type, cs: Carrier_Set, comment: Optional[str]):
        super().__init__(instruction_type, comment)
        self.cs = cs

    def __str__(self):
        return f"{self.instruction_type} {self.cs}{self.comment_str}"


class In_Instruction(Carrier_Instruction):

    def __init__(self, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.In, cs, comment)

    def execute(self, machine_state):
        machine_state.bring_in(self.cs)


class Inhook_Instruction(Carrier_Instruction):

    def __init__(self, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Inhook, cs, comment)

    def execute(self, machine_state):
        machine_state.in_hook(self.cs)


class Releasehook_Instruction(Carrier_Instruction):

    def __init__(self, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Releasehook, cs, comment)

    def execute(self, machine_state):
        hooked_carriers = machine_state.carrier_system.hooked_carriers
        assert hooked_carriers == self.cs, f"Cannot release hook {self.cs} because currently hooked carriers are {hooked_carriers}"
        machine_state.release_hook()


class Out_Instruction(Carrier_Instruction):

    def __init__(self, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Out, cs, comment)

    def execute(self, machine_state):
        machine_state.out(self.cs)


class Outhook_Instruction(Carrier_Instruction):

    def __init__(self, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Outhook, cs, comment)

    def execute(self, machine_state):
        machine_state.out_hook(self.cs)
