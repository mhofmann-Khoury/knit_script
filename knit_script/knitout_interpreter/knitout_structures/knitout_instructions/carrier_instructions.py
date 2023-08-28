from typing import Optional

from knit_script.Knit_Errors.carrier_operation_errors import In_Active_Carrier_Error, Inserting_Hook_In_Use_Error, Out_Inactive_Carrier_Error, Out_Hooked_Carrier_Error, Cut_Hooked_Carrier_Error
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
        for carrier in self.carrier_set.get_carriers(machine_state.carrier_system):
            if carrier.is_active:
                raise In_Active_Carrier_Error(carrier.carrier_id, self)
        machine_state.bring_in(self.carrier_set)


class Inhook_Instruction(Hook_Instruction):

    def __init__(self, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Inhook, cs, comment)

    def execute(self, machine_state):
        if not machine_state.carrier_system.inserting_hook_available:
            raise Inserting_Hook_In_Use_Error(self)
        for carrier in self.carrier_set.get_carriers(machine_state.carrier_system):
            if carrier.is_active:
                raise In_Active_Carrier_Error(carrier.carrier_id, self)
        machine_state.in_hook(self.carrier_set)


class Releasehook_Instruction(Hook_Instruction):

    def __init__(self, cs: Optional[Carrier_Set], comment: Optional[str] = None):
        super().__init__(Instruction_Type.Releasehook, cs, comment)

    def execute(self, machine_state):
        if self.carrier_set is not None:
            mismatched_carriers = [c for c in self.carrier_set.get_carriers(machine_state.carrier_system) if not c.is_hooked]
            if len(mismatched_carriers) > 0:
                print(f"Knitout Warning: cannot release unhooked carriers {mismatched_carriers}. Releasehook done on matching carriers")
        else:
            self.carrier_set = machine_state.carrier_system.hooked_carriers
        machine_state.release_hook()


class Out_Instruction(Carrier_Instruction):

    def __init__(self, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Out, cs, comment)

    def execute(self, machine_state):
        for carrier in self.carrier_set.get_carriers(machine_state.carrier_system):
            if carrier.is_active:
                raise Out_Inactive_Carrier_Error(carrier.carrier_id, self)
            if carrier.is_hooked:
                raise Out_Hooked_Carrier_Error(carrier.carrier_id, self)
        machine_state.out(self.carrier_set)


class Outhook_Instruction(Hook_Instruction):

    def __init__(self, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Outhook, cs, comment)

    def execute(self, machine_state):
        if not machine_state.carrier_system.inserting_hook_available:
            raise Inserting_Hook_In_Use_Error(self)
        for carrier in self.carrier_set.get_carriers(machine_state.carrier_system):
            if not carrier.is_active:
                raise Out_Inactive_Carrier_Error(carrier.carrier_id, self)
            if carrier.is_hooked:
                raise Cut_Hooked_Carrier_Error(carrier.carrier_id, self)
        machine_state.out_hook(self.carrier_set)
