"""Structure for Instructions"""
from enum import Enum
from typing import Optional

from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Knitout_Line


class Instruction_Type(Enum):
    """
        Knitout Instruction types
    """
    In = "in"
    Inhook = "inhook"
    Releasehook = "releasehook"
    Out = "out"
    Outhook = "outhook"
    Stitch = "stitch"
    Rack = "rack"
    Knit = "knit"
    Tuck = "tuck"
    Split = "split"
    Drop = "drop"
    Amiss = "amiss"
    Xfer = "xfer"
    Miss = "miss"
    Pause = "pause"
    X = "x-"

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)

    @staticmethod
    def get_instruction(inst_str: str):
        """
        Get the instruction from a string
        :param inst_str: instruction string to pull from
        :return: Instruction_Type Enum of that type
        """
        return Instruction_Type[inst_str.capitalize()]

    @property
    def is_carrier_instruction(self) -> bool:
        """
        :return: True if instruction operates on yarn carriers
        """
        return self in [Instruction_Type.In, Instruction_Type.Inhook, Instruction_Type.Releasehook, Instruction_Type.Out, Instruction_Type.Outhook]

    @property
    def is_needle_instruction(self) -> bool:
        """
        :return: True if operation operates on needles
        """
        return self in [Instruction_Type.Knit, Instruction_Type.Tuck, Instruction_Type.Split,
                        Instruction_Type.Miss, Instruction_Type.Amiss, Instruction_Type.Drop, Instruction_Type.Xfer]

    @property
    def in_knitting_pass(self) -> bool:
        """
        :return: True if instruction can be done in a knit pass
        """
        return self in [Instruction_Type.Knit, Instruction_Type.Tuck]  # Todo: test miss and drop operations

    @property
    def all_needle_instruction(self) -> bool:
        """
        :return: True if instruction is compatible with all-needle knitting
        """
        return self.in_knitting_pass

    @property
    def directed_pass(self) -> bool:
        """
        :return: True if instruction requires a direction
        """
        return self in [Instruction_Type.Knit, Instruction_Type.Tuck, Instruction_Type.Miss, Instruction_Type.Split]

    @property
    def requires_carrier(self) -> bool:
        """
        :return: True if instruction requires a direction
        """
        return self.directed_pass

    @property
    def requires_second_needle(self) -> bool:
        """
        :return: True if instruction requires second needle
        """
        return self in [Instruction_Type.Xfer, Instruction_Type.Split]

    @property
    def allow_sliders(self) -> bool:
        """
        :return: True if a xfer instruction that can operate on sliders
        """
        return self is Instruction_Type.Xfer

    def allowed_mid_pass(self) -> bool:
        """
        :return: true if pause instruction which can be done without interrupting a machine pass
        """
        return self is Instruction_Type.Pause

    def compatible_pass(self, other_instruction) -> bool:
        """
        Determine if instruction can share a machine pass
        :param other_instruction: Needle_Instruction to see if they match the pass type
        :return: True if both instructions could be executed in a pass
        """
        if not self.is_needle_instruction:
            return False
        elif self.in_knitting_pass and other_instruction.in_knitting_pass:
            return True
        else:
            return self is other_instruction


class Instruction(Knitout_Line):
    """
        Super class for knitout operations
    """

    def __init__(self, instruction_type: Instruction_Type, comment: Optional[str]):
        super().__init__(comment)
        self.instruction_type: Instruction_Type = instruction_type

    def __str__(self):
        return f"{self.instruction_type}{self.comment_str}"

    def execute(self, machine_state) -> bool:
        """
        Executes the instruction on the machine state.
        :param machine_state: The machine state to update.
        :return: True if the process completes an update.
        """
        return False
