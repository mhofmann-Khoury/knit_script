"""Needle operations"""
from typing import Optional

from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction, Instruction_Type
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.needles import Needle
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set


class Knitout_Needle_Instruction(Instruction):

    def __init__(self, instruction_type: Instruction_Type,
                 needle: Needle, direction: Optional[Pass_Direction] = None, needle_2: Optional[Needle] = None,
                 carrier_set: Optional[Carrier_Set] = None,
                 comment: Optional[str] = None):
        super().__init__(instruction_type, comment)
        self.carrier_set = carrier_set
        self.needle_2 = needle_2
        self.direction: Optional[Pass_Direction] = direction
        self.needle = needle
        self.carriage_pass = None

    @property
    def has_second_needle(self) -> bool:
        """
        :return: True if it has a second needle
        """
        return self.needle_2 is not None

    @property
    def has_direction(self) -> bool:
        """
        :return: True if it has a direction value
        """
        return self.direction is not None

    @property
    def has_carrier_set(self) -> bool:
        """
        :return: true if it has carrier set
        """
        return self.carrier_set is not None

    def _test_operation(self, machine_state):
        if self.has_carrier_set:
            assert machine_state.carrier_system.is_active(self.carrier_set), f"Cannot {self.instruction_type} with inactive carrier set {self.carrier_set}"
        if self.needle is not None:  # update needles to be in the machine state
            self.needle = machine_state[self.needle]
        if self.needle_2 is not None:
            self.needle_2 = machine_state[self.needle_2]

    def add_instruction_to_needle_1_loops(self):
        assert self.needle is not None
        for loop in self.needle.held_loops:
            loop.instructions.append(self)

    def add_instruction_to_needle_2_loops(self):
        assert self.needle_2 is not None
        for loop in self.needle_2.held_loops:
            loop.instructions.append(self)

    def __str__(self):
        if self.has_direction:
            dir_str = f" {self.direction}"
        else:
            dir_str = ""
        if self.has_second_needle:
            n2_str = f" {self.needle_2}"
        else:
            n2_str = ""
        if self.has_carrier_set:
            cs_str = f" {self.carrier_set}"
        else:
            cs_str = ""
        return f"{self.instruction_type}{dir_str} {self.needle}{n2_str}{cs_str}{self.comment_str}"


class Loop_Making_Instruction(Knitout_Needle_Instruction):

    def __init__(self, instruction_type: Instruction_Type, needle: Needle, direction: Optional[Pass_Direction] = None, needle_2: Optional[Needle] = None, carrier_set: Optional[Carrier_Set] = None,
                 comment: Optional[str] = None):
        super().__init__(instruction_type, needle, direction, needle_2, carrier_set, comment)


class Knit_Instruction(Loop_Making_Instruction):

    def __init__(self, needle: Needle, direction: str, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Knit, needle, direction=Pass_Direction.get_direction(direction), carrier_set=cs, comment=comment)

    def execute(self, machine_state):
        self._test_operation(machine_state)
        if len(self.needle.held_loops) == 0:
            print(f"Knitout Warning: Knitting on needle {self.needle} without prior loops.")
        self.add_instruction_to_needle_1_loops()
        loops = machine_state.knit(self.needle, self.carrier_set)
        for loop in loops:
            loop.instructions.append(self)
            loop.creating_instruction = self


class Tuck_Instruction(Loop_Making_Instruction):

    def __init__(self, needle: Needle, direction: str, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Tuck, needle, direction=Pass_Direction.get_direction(direction), carrier_set=cs, comment=comment)

    def execute(self, machine_state):
        self._test_operation(machine_state)
        loops = machine_state.tuck(self.needle, self.carrier_set)
        for loop in loops:
            loop.instructions.append(self)
            loop.creating_instruction = self


class Split_Instruction(Loop_Making_Instruction):

    def __init__(self, needle: Needle, direction: str, n2: Needle, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Split, needle, direction=Pass_Direction.get_direction(direction), needle_2=n2, carrier_set=cs, comment=comment)

    def execute(self, machine_state):
        self._test_operation(machine_state)
        self.add_instruction_to_needle_1_loops()  # loops that will be transferred
        loops = machine_state.split(self.needle, self.needle_2, self.carrier_set)
        for loop in loops:
            loop.instructions.append(self)
            loop.creating_instruction = self


class Drop_Instruction(Knitout_Needle_Instruction):

    def __init__(self, needle: Needle, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Split, needle, comment=comment)

    def execute(self, machine_state):
        self._test_operation(machine_state)
        self.add_instruction_to_needle_1_loops()  # add to loops before drop
        machine_state.drop(self.needle)


class Amiss_Instruction(Knitout_Needle_Instruction):

    def __init__(self, needle: Needle, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Amiss, needle, comment=comment)

    def execute(self, machine_state):
        self._test_operation(machine_state)


class Xfer_Instruction(Knitout_Needle_Instruction):

    def __init__(self, needle: Needle, n2: Needle, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Xfer, needle, needle_2=n2, comment=comment)

    def execute(self, machine_state):
        self._test_operation(machine_state)
        self.add_instruction_to_needle_1_loops()
        machine_state.xfer(self.needle, self.needle_2)
        # self.add_instruction_to_needle_2_loops()  # transferred loops


class Miss_Instruction(Knitout_Needle_Instruction):

    def __init__(self, needle: Needle, direction: str, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Miss, needle, direction=Pass_Direction.get_direction(direction), carrier_set=cs, comment=comment)

    def execute(self, machine_state):
        self._test_operation(machine_state)
