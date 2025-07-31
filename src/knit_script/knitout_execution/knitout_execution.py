"""Factory function for building knitout instructions based on instruction type."""
from knitout_interpreter.knitout_operations.Knitout_Line import Knitout_Line
from knitout_interpreter.knitout_operations.Pause_Instruction import Pause_Instruction
from knitout_interpreter.knitout_operations.Rack_Instruction import Rack_Instruction
from knitout_interpreter.knitout_operations.carrier_instructions import In_Instruction, Inhook_Instruction, Releasehook_Instruction, Outhook_Instruction, Out_Instruction
from knitout_interpreter.knitout_operations.knitout_instruction import Knitout_Instruction_Type
from knitout_interpreter.knitout_operations.needle_instructions import Miss_Instruction, Knit_Instruction, Tuck_Instruction, Split_Instruction, Drop_Instruction, Xfer_Instruction
from virtual_knitting_machine.machine_components.carriage_system.Carriage_Pass_Direction import Carriage_Pass_Direction
from virtual_knitting_machine.machine_components.needles.Needle import Needle
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import Yarn_Carrier
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier_Set import Yarn_Carrier_Set


def build_instruction(instruction_type: Knitout_Instruction_Type,
                      first_needle: Needle | None = None,
                      direction: None | Carriage_Pass_Direction = None,
                      carrier_set: Yarn_Carrier_Set | Yarn_Carrier | None = None,
                      second_needle: Needle | None = None,
                      racking: float | None = None,
                      comment: str | None = None) -> Knitout_Line:
    """Builds a knitout instruction based on the specified instruction type and parameters.

    This factory function creates the appropriate knitout instruction object based on the instruction type and provided parameters.
    It handles all supported knitout instruction types including needle operations, carrier operations, and machine control operations.

    Args:
        instruction_type: The type of knitout instruction to create.
        first_needle: The primary needle for the operation. Required for needle-based instructions like knit, tuck, drop, etc.
        direction: The carriage pass direction for directional operations. Required for operations that involve yarn carrier movement.
        carrier_set: The yarn carrier or carrier set to use for the operation. Required for operations that manipulate yarn.
        second_needle: The secondary needle for operations requiring two needles, such as  transfers and splits.
        racking: The racking value for rack instructions. Specifies the relative position between needle beds.
        comment: Optional comment to include with the instruction for documentation or debugging purposes.

    Returns:
        The constructed knitout instruction object corresponding to the specified type.

    Raises:
        ValueError: If an unsupported instruction type is provided or
        if required parameters are missing for the specified instruction type.

    Todo: Remove this factory and use the equivalent from the updated knitout-interpreter package.
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
    else:
        raise ValueError(f"Unsupported instruction type: {instruction_type}")
