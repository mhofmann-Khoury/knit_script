"""
Methods and support for writing knitout commands and updating a machine state
"""

from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line, Knitout_Comment_Line
from knitout_interpreter.knitout_operations.Pause_Instruction import Pause_Instruction
from knitout_interpreter.knitout_operations.Rack_Instruction import Rack_Instruction
from knitout_interpreter.knitout_operations.carrier_instructions import In_Instruction, Inhook_Instruction, Releasehook_Instruction, Outhook_Instruction, Out_Instruction
from knitout_interpreter.knitout_operations.knitout_instruction import Knitout_Instruction_Type
from knitout_interpreter.knitout_operations.needle_instructions import Miss_Instruction, Knit_Instruction, Tuck_Instruction, Split_Instruction, Drop_Instruction, Xfer_Instruction
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Needle import Needle
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import Yarn_Carrier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import Yarn_Carrier_Set


def build_instruction(instruction_type: Knitout_Instruction_Type, first_needle: Needle | None = None, direction: None | Carriage_Pass_Direction = None,
                      carrier_set: Yarn_Carrier_Set | Yarn_Carrier | None = None, second_needle: Needle | None = None, racking: float | None = None,
                      comment: str | None = None) -> Knitout_Line:
    """
    Update machine state with knitout instruction with given parameters
    :param comment:
    :param racking:
    :param instruction_type:
    :param first_needle: The needle to operate on
    :param direction: the optional direction for current pass
    :param carrier_set: optional carrier for instruction
    :param second_needle: optional second needle for xfers and splits
    :return: Knitout instruction
    """
    if instruction_type is Knitout_Instruction_Type.Knit:
        return Knit_Instruction(first_needle, direction, carrier_set, comment=comment)
    elif instruction_type is Knitout_Instruction_Type.Tuck:
        return Tuck_Instruction(first_needle, direction, carrier_set, comment=comment)
    elif instruction_type is Knitout_Instruction_Type.Drop:
        return Drop_Instruction(first_needle, comment=comment)
    elif instruction_type is Knitout_Instruction_Type.Xfer:
        return Xfer_Instruction(first_needle, second_needle, comment=comment)
    elif instruction_type is Knitout_Instruction_Type.Miss:
        return Miss_Instruction(first_needle, direction, carrier_set, comment)
    elif instruction_type is Knitout_Instruction_Type.Split:
        return Split_Instruction(first_needle, direction, second_needle, carrier_set, comment)
    elif instruction_type is Knitout_Instruction_Type.Outhook:
        return Outhook_Instruction(carrier_set, comment)
    elif instruction_type is Knitout_Instruction_Type.Out:
        return Out_Instruction(carrier_set, comment)
    elif instruction_type is Knitout_Instruction_Type.In:
        return In_Instruction(carrier_set, comment)
    elif instruction_type is Knitout_Instruction_Type.Inhook:
        return Inhook_Instruction(carrier_set, comment)
    elif instruction_type is Knitout_Instruction_Type.Releasehook:
        return Releasehook_Instruction(carrier_set, comment)
    elif instruction_type is Knitout_Instruction_Type.Rack:
        return Rack_Instruction(racking, comment)
    elif instruction_type is Knitout_Instruction_Type.Pause:
        return Pause_Instruction(comment)
