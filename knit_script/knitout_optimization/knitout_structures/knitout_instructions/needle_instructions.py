"""Needle operations"""
from typing import Optional

from knit_script.knitout_optimization.knitout_structures.knitout_instructions.instruction import Instruction, Instruction_Type
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.needles import Needle
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set


class Needle_Instruction(Instruction):

    def __init__(self, instruction_type: Instruction_Type, needle: Needle, direction: Optional[Pass_Direction] = None, needle_2: Optional[Needle] = None, carrier_set: Optional[Carrier_Set] = None,
                 comment: Optional[str] = None):
        super().__init__(instruction_type, comment)
        self.carrier_set = carrier_set
        self.needle_2 = needle_2
        self.direction = direction
        self.needle = needle

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


class Knit_Instruction(Needle_Instruction):

    def __init__(self, needle: Needle, direction: str, cs: Carrier_Set, comment: Optional[str]):
        super().__init__(Instruction_Type.Knit, needle, direction=Pass_Direction.get_direction(direction), carrier_set=cs, comment=comment)


class Tuck_Instruction(Needle_Instruction):

    def __init__(self, needle: Needle, direction: str, cs: Carrier_Set, comment: Optional[str]):
        super().__init__(Instruction_Type.Tuck, needle, direction=Pass_Direction.get_direction(direction), carrier_set=cs, comment=comment)


class Split_Instruction(Needle_Instruction):

    def __init__(self, needle: Needle, direction: str, n2: Needle, cs: Carrier_Set, comment: Optional[str]):
        super().__init__(Instruction_Type.Split, needle, direction=Pass_Direction.get_direction(direction), needle_2=n2, carrier_set=cs, comment=comment)


class Drop_Instruction(Needle_Instruction):

    def __init__(self, needle: Needle, comment: Optional[str]):
        super().__init__(Instruction_Type.Split, needle, comment=comment)


class Amiss_Instruction(Needle_Instruction):

    def __init__(self, needle: Needle, comment: Optional[str]):
        super().__init__(Instruction_Type.Amiss, needle, comment=comment)


class Xfer_Instruction(Needle_Instruction):

    def __init__(self, needle: Needle, n2: Needle, comment: Optional[str]):
        super().__init__(Instruction_Type.Xfer, needle, needle_2=n2, comment=comment)


class Miss_Instruction(Needle_Instruction):

    def __init__(self, needle: Needle, direction: str, cs: Carrier_Set, comment: Optional[str]):
        super().__init__(Instruction_Type.Miss, needle, direction=Pass_Direction.get_direction(direction), carrier_set=cs, comment=comment)
