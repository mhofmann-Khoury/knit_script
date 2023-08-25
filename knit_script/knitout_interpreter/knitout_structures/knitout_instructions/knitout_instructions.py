"""
Methods and support for writing knitout commands and updating a machine state
"""
from typing import Optional

from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Comment_Line, Knitout_Line
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.Pause_Instruction import Pause_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.Rack_Instruction import Rack_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.carrier_instructions import In_Instruction, Inhook_Instruction, Releasehook_Instruction, Outhook_Instruction, \
    Out_Instruction
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.instruction import Instruction_Type
from knit_script.knitout_interpreter.knitout_structures.knitout_instructions.needle_instructions import Miss_Instruction, Knit_Instruction, Tuck_Instruction, Split_Instruction, Drop_Instruction, \
    Xfer_Instruction, Amiss_Instruction
from knit_script.knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knit_script.knitting_machine.machine_components.needles import Needle
from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set


def rack(machine_state, racking: float, comment: Optional[str] = None) -> Rack_Instruction:
    """
    :param machine_state: the current machine model to update
    :param racking: the new racking to set the machine to
    :param comment: additional details to document in the knitout
    :return: the racking instruction
    """
    instruction = Rack_Instruction(racking, comment)
    instruction.execute(machine_state)
    return instruction


def miss(machine_state, direction: Pass_Direction, needle: Needle, carrier_set: Carrier_Set, comment: Optional[str] = None) -> Miss_Instruction:
    """
    Move the specified carriers as if they had just formed a loop in direction D at location N.
    (Not generally needed, used when performing explicit kickbacks or purposeful yarn capture.)

    Parameters
    ----------
    comment
    carrier_set
    needle
    direction
    machine_state
    """
    # assert machine_state.carrier_system.is_active(carrier_set), f"Yarn-Carrier {carrier_set} is not active"
    # carriers = _make_carrier_set(carrier_set)
    instruction = Miss_Instruction(needle, direction, carrier_set, comment)
    instruction.execute(machine_state)
    return instruction
    # return f"miss {direction} {needle} {carriers};{comment}\n"


def knit(machine_state, direction: Pass_Direction, needle: Needle, carrier_set: Carrier_Set, comment: Optional[str] = None) -> Knit_Instruction:
    """
    Pull a loop formed in direction D by the yarns in carriers CS through the loops on needle N,
    dropping them in the process.
    Knitting with an empty carrier set will drop
    Used for resetting the sheets.
    :param machine_state: The current machine model to update
    :param direction: the direction to pull the yarn across the needle from
    :param needle: the needle to make the loop on
    :param carrier_set: the set of carriers being used
    :param comment: additional details to document in the knitout
    :return: the knit instruction
    """
    # loops = machine_state.knit(needle, carrier_set, record_needle=record_needle)
    # carriers = _make_carrier_set(carrier_set)
    instruction = Knit_Instruction(needle, direction, carrier_set, comment)
    instruction.execute(machine_state)
    return instruction
    # return f"knit {direction} {needle} {carriers} ;knit loops: {loops}. {comment}\n"


def tuck(machine_state, direction: Pass_Direction, needle: Needle, carrier_set: Carrier_Set, comment: Optional[str] = None) -> Tuck_Instruction:
    """
    Add a loop formed in direction D by the yarns held by carriers in CS to those already on needle N.
    Tucking with an empty carrier set will pull on the stitches without doing anything else (an "a-miss").
    Used for resetting sheets.
    :param machine_state: The current machine model to update
    :param direction: the direction to pull the yarn across the needle from
    :param needle: the needle to make the loop on
    :param carrier_set: the set of carriers being used
    :param comment: additional details to document in the knitout
    :return: the tuck instruction
    """
    # loops = machine_state.tuck(needle, carrier_set, record_needle=record_needle)
    # carriers = _make_carrier_set(carrier_set)
    instruction = Tuck_Instruction(needle, direction, carrier_set, comment)
    instruction.execute(machine_state)
    return instruction
    # return f"tuck {direction} {needle} {carriers} ; tuck loops: {loops}. {comment}\n"


def split(machine_state, direction: Pass_Direction, start: Needle, target,
          carrier_set: Carrier_Set, comment: Optional[str] = None) -> Split_Instruction:
    """
    Pull a loop formed in direction D by the yarns in carriers CS through the loops on needle N,
    transferring the old loops to opposite-bed needle N2 in the process.
    Splitting with an empty carrier set will transfer
    :param machine_state: The current machine model to update
    :param direction: the direction to pull the yarn across the needle from
    :param start: the first needle to make the loop on and transfer from
    :param target: the second needle to transfer the original loops from
    :param carrier_set: the set of carriers being used
    :param comment: additional details to document in the knitout
    :return: the split instruction
    """
    # loops = machine_state.split(start, target, carrier_set, record_needle=record_needle)
    # carriers = _make_carrier_set(carrier_set)
    instruction = Split_Instruction(start, direction, target, carrier_set, comment)
    instruction.execute(machine_state)
    return instruction
    # return f"split {direction} {start} {target} {carriers} ;Split loops: {loops}. {comment}\n"


def drop(machine_state, needle: Needle, comment: Optional[str] = None) -> Drop_Instruction:
    """
    Synonym for "knit + N"
    Drops the loops on the needle
    :param machine_state: the current machine model to update
    :param needle: the needle to drop loops from
    :param comment: additional details to document in the knitout
    :return: the drop instruction
    """
    # loops = machine_state.drop_from_needle(needle, record_needle)
    instruction = Drop_Instruction(needle, comment)
    instruction.execute(machine_state)
    return instruction
    # return f"drop {needle} ;Dropped loops: {loops}. {comment}\n"


def xfer(machine_state, start: Needle, target: Needle, comment: Optional[str] = None, record_needle=False) -> Xfer_Instruction:
    """
    Synonym for "split + N N2"
    Transfer loops from needle 1 to needle 2, leaving needle 1 empty
    :param machine_state: the current machine model to update
    :param start: the first needle to xfer from
    :param target: the second needle to xfer to
    :param comment: additional details to document in the knitout
    :return: the xfer instruction
    """
    # machine_state.xfer(start, target, record_needle=record_needle)
    instruction = Xfer_Instruction(start, target, comment, record_location=record_needle)
    instruction.execute(machine_state)
    return instruction
    # return f"xfer {start} {target} ;{comment}\n"


def bring_in(machine_state, carrier_set: Carrier_Set, comment: Optional[str] = None) -> In_Instruction:
    """
    Enter is used to avoid confusion with "in" keyword.
    Brings yarn carrier into action without yarn holding hook
    :param machine_state: the current machine model to update
    :param carrier_set: the set of carriers to bring in
    :param comment: additional details to document in the knitout
    :return: in instruction
    """
    # machine_state.bring_in(carrier_set)
    instruction = In_Instruction(carrier_set, comment)
    instruction.execute(machine_state)
    return instruction
    # return f"in {_make_carrier_set(carrier_set)} ;{comment}{os.linesep}"


def inhook(machine_state, carrier_set: Carrier_Set, comment: Optional[str] = None) -> Inhook_Instruction:
    """
    Indicate that the given carrier set should be brought into action using the yarn inserting hook when next used.
    The inserting hook will be parked just before the first stitch made with the carriers
    :param machine_state: the current machine model to update
    :param carrier_set: the set of carriers to bring in
    :param comment: additional details to document in the knitout
    :return: the inhook instruction
    """
    # machine_state.in_hook(carrier_set)
    instruction = Inhook_Instruction(carrier_set, comment)
    instruction.execute(machine_state)
    return instruction
    # return f"inhook {_make_carrier_set(carrier_set)} ;{comment}\n"


def releasehook(machine_state, comment: Optional[str] = None) -> Releasehook_Instruction | Comment_Line:
    """
    Release the yarns currently held in the yarn inserting hook.
    Must be proceeded by a call to inhook with the same carrier set and at least one knitting operation.
    :param machine_state: The current machine model to update
    :param comment: additional details to document in the knitout
    :return: the releasehook instruction
    """
    released_carrier = machine_state.carrier_system.hooked_carriers
    # machine_state.release_hook()
    if released_carrier is None:
        return Comment_Line("no-op. Releasehook with no hooked carriers")
        # return f"; no-op. Releasehook with no hooked carriers\n"
    else:
        instruction = Releasehook_Instruction(released_carrier, comment)
        instruction.execute(machine_state)
        return instruction
        # return f"releasehook {_make_carrier_set(released_carrier)} ;{comment}\n"


def outhook(machine_state, carrier_set: Carrier_Set, comment: Optional[str] = None) -> Outhook_Instruction:
    """
    Release the yarns currently held in the yarn inserting hook.
    Must be proceeded by a call to inhook with the same carrier set and at least one knitting operation.
    :param machine_state: The current machine model to update
    :param carrier_set: the set of carriers to bring out
    :param comment: additional details to document in the knitout
    :return: the outhook instruction
    """
    # machine_state.out_hook(carrier_set)
    instruction = Outhook_Instruction(carrier_set, comment)
    instruction.execute(machine_state)
    return instruction
    # return f"outhook {_make_carrier_set(carrier_set)} ;{comment}\n"


def out(machine_state, carrier_set: Carrier_Set, comment: Optional[str] = None) -> Out_Instruction:
    """
    Bring a set of carriers out of action by directly moving into the grippers
    :param machine_state: the current machine model to update
    :param carrier_set: the set of carriers to bring out
    :param comment: additional details to document in the knitout
    :return: the out instruction
    """
    instruction = Out_Instruction(carrier_set, comment)
    instruction.execute(machine_state)
    return instruction


def build_instruction(instruction_type: Instruction_Type, first_needle: Optional[Needle] = None, direction: Optional[Pass_Direction] = None,
                      carrier_set: Optional[Carrier_Set] = None, second_needle: Optional[Needle] = None, racking: Optional[float] = None,
                      comment: Optional[str] = None) -> Knitout_Line:
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
    if instruction_type is Instruction_Type.Knit:
        return Knit_Instruction(first_needle, direction, carrier_set, comment=comment)
    elif instruction_type is Instruction_Type.Tuck:
        return Tuck_Instruction(first_needle, direction, carrier_set, comment=comment)
    elif instruction_type is Instruction_Type.Drop:
        return Drop_Instruction(first_needle, comment=comment)
    elif instruction_type is Instruction_Type.Xfer:
        return Xfer_Instruction(first_needle, second_needle, comment=comment)
    elif instruction_type is Instruction_Type.Amiss:
        return Amiss_Instruction(first_needle, comment)
    elif instruction_type is Instruction_Type.Miss:
        return Miss_Instruction(first_needle, direction, carrier_set, comment)
    elif instruction_type is Instruction_Type.Split:
        return Split_Instruction(first_needle, direction, second_needle, carrier_set, comment)
    elif instruction_type is Instruction_Type.Outhook:
        return Outhook_Instruction(carrier_set, comment)
    elif instruction_type is Instruction_Type.Out:
        return Out_Instruction(carrier_set, comment)
    elif instruction_type is Instruction_Type.In:
        return In_Instruction(carrier_set, comment)
    elif instruction_type is Instruction_Type.Inhook:
        return Inhook_Instruction(carrier_set, comment)
    elif instruction_type is Instruction_Type.Releasehook:
        return Releasehook_Instruction(carrier_set, comment)
    elif instruction_type is Instruction_Type.Rack:
        return Rack_Instruction(racking, comment)
    elif instruction_type is Instruction_Type.Pause:
        return Pause_Instruction(comment)
