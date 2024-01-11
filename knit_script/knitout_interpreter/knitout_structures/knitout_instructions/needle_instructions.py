"""Needle operations"""
from typing import Optional

from knit_script.Knit_Errors.knitting_errors import Long_Float_Error, Slider_Use_Error, Blocked_Sliders_Error, Slider_Clear_Error, Valid_Rack_Error, \
    Same_Bed_Transfer_Error
from knit_script.Knit_Errors.yarn_management_errors import Inactive_Carrier_Error
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction, Instruction_Type
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.needles import Needle
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set


class Knitout_Needle_Instruction(Instruction):

    def __init__(self, instruction_type: Instruction_Type,
                 needle: Needle, direction: Optional[str | Pass_Direction] = None, needle_2: Optional[Needle] = None,
                 carrier_set: Optional[Carrier_Set] = None,
                 comment: Optional[str] = None):
        super().__init__(instruction_type, comment)
        self.carrier_set = carrier_set
        self.needle_2 = needle_2
        if direction is not None and isinstance(direction, str):
            direction = Pass_Direction.get_direction(direction)
        self.direction: Optional[Pass_Direction] = direction
        self.needle = needle
        self.carriage_pass = None
        self.made_loops = None
        self.moved_loops = None

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

    def _test_operation(self, machine_state, test_clear_sliders=False, test_no_slider=False):
        if self.instruction_type.directed_pass:
            assert self.has_direction, f"Cannot {self.instruction_type} without a direction"
        if self.instruction_type.requires_second_needle:
            assert self.has_second_needle, f"Cannot {self.instruction_type} without target needle"
        if self.has_carrier_set:
            if not machine_state.carrier_system.is_active(self.carrier_set):
                raise Inactive_Carrier_Error(self.carrier_set, machine_state.missing_carriers(self.carrier_set), self)
            for carrier in self.carrier_set.get_carriers(machine_state.carrier_system):
                old_position = carrier.position
                if old_position is not None:  # first time used since brought in
                    float_length = abs(old_position - int(self.needle))
                    if float_length > machine_state.max_float:
                        raise Long_Float_Error(old_position, self.needle, carrier, machine_state.max_float, self)
        if self.needle is not None:  # update needles to be in the machine state
            self.needle = machine_state[self.needle]
            if not self.needle.is_clear(machine_state):
                raise Slider_Clear_Error(self.needle, self)
        if self.needle_2 is not None:
            self.needle_2 = machine_state[self.needle_2]
            if not self.needle_2.is_clear(machine_state):
                raise Slider_Clear_Error(self.needle_2, self)
            if self.needle.is_front == self.needle_2.is_front:
                raise Same_Bed_Transfer_Error(self.needle, self.needle_2, self)
        if test_clear_sliders:
            if not machine_state.sliders_are_clear():
                raise Blocked_Sliders_Error(self)
        if test_no_slider:
            if self.needle.is_slider:
                raise Slider_Use_Error(self.needle, self)

    def add_instruction_to_needle_1_loops(self):
        """
            Records the instruction as effecting the loops held on needle 1
        """
        assert self.needle is not None
        for loop in self.needle.held_loops:
            loop.instructions.append(self)

    def add_instruction_to_needle_2_loops(self):
        """
            Records the instruction as effecting the loops held on needle 2
        """
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

    def __init__(self, instruction_type: Instruction_Type, needle: Needle, direction: Optional[str | Pass_Direction] = None, needle_2: Optional[Needle] = None,
                 carrier_set: Optional[Carrier_Set] = None,
                 comment: Optional[str] = None):
        super().__init__(instruction_type, needle, direction, needle_2, carrier_set, comment)


class Knit_Instruction(Loop_Making_Instruction):

    def __init__(self, needle: Needle, direction: str | Pass_Direction, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Knit, needle, direction=direction, carrier_set=cs, comment=comment)

    def execute(self, machine_state):
        self._test_operation(machine_state, test_clear_sliders=True, test_no_slider=True)
        if len(self.needle.held_loops) == 0:
            print(f"Knitout Warning: Knitting on needle {self.needle} without prior loops.")
        self.add_instruction_to_needle_1_loops()
        self.made_loops = machine_state.knit(self.needle, self.carrier_set)
        for loop in self.made_loops:
            loop.instructions.append(self)
            loop.creating_instruction = self
        return True


class Tuck_Instruction(Loop_Making_Instruction):

    def __init__(self, needle: Needle, direction: str | Pass_Direction, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Tuck, needle, direction=direction, carrier_set=cs, comment=comment)

    def execute(self, machine_state):
        self._test_operation(machine_state, test_clear_sliders=True, test_no_slider=True)
        self.made_loops = machine_state.tuck(self.needle, self.carrier_set)
        for loop in self.made_loops:
            loop.instructions.append(self)
            loop.creating_instruction = self
        return True


class Split_Instruction(Loop_Making_Instruction):

    def __init__(self, needle: Needle, direction: str | Pass_Direction, n2: Needle, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Split, needle, direction=direction, needle_2=n2, carrier_set=cs, comment=comment)

    def execute(self, machine_state):
        self._test_operation(machine_state, test_clear_sliders=True, test_no_slider=True)
        self.add_instruction_to_needle_1_loops()  # loops that will be transferred
        self.made_loops, self.moved_loops = machine_state.split(self.needle, self.needle_2, self.carrier_set)
        for loop in self.made_loops:
            loop.instructions.append(self)
            loop.creating_instruction = self


class Drop_Instruction(Knitout_Needle_Instruction):

    def __init__(self, needle: Needle, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Drop, needle, comment=comment)

    def execute(self, machine_state):
        self._test_operation(machine_state, test_no_slider=True, test_clear_sliders=True)
        self.add_instruction_to_needle_1_loops()  # add to loops before drop
        machine_state.drop(self.needle)


class Amiss_Instruction(Knitout_Needle_Instruction):

    def __init__(self, needle: Needle, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Amiss, needle, comment=comment)

    def execute(self, machine_state):
        self._test_operation(machine_state)


class Xfer_Instruction(Knitout_Needle_Instruction):

    def __init__(self, needle: Needle, n2: Needle, comment: Optional[str] = None, record_location=True):
        super().__init__(Instruction_Type.Xfer, needle, needle_2=n2, comment=comment)
        self.record_location = record_location

    def execute(self, machine_state):
        self._test_operation(machine_state)
        # self.add_instruction_to_needle_1_loops()
        if self.needle.is_front:
            if not machine_state.valid_rack(int(self.needle), int(self.needle_2)):
                raise Valid_Rack_Error(self.needle, self.needle_2, machine_state.racking, self)
        else:
            if not machine_state.valid_rack(int(self.needle_2), int(self.needle)):
                raise Valid_Rack_Error(self.needle, self.needle_2, machine_state.racking, self)
        self.moved_loops = machine_state.xfer(self.needle, self.needle_2, record_needle=self.record_location)
        self.add_instruction_to_needle_2_loops()  # transferred loops


class Miss_Instruction(Knitout_Needle_Instruction):

    def __init__(self, needle: Needle, direction: str | Pass_Direction, cs: Carrier_Set, comment: Optional[str] = None):
        super().__init__(Instruction_Type.Miss, needle, direction=direction, carrier_set=cs, comment=comment)

    def execute(self, machine_state):
        """
        Positions the carrier above the give needle.
        :param machine_state: The machine state to update.
        """
        try:
            self._test_operation(machine_state)
        except Long_Float_Error as e:
            print(f"Warning: Miss with {e.message}")
        for cid in self.carrier_set:
            machine_state.carrier_system.position_carrier(cid, self.needle)
