"""
Methods and support for writing knitout commands and updating a machine state
"""
import os

from knitting_machine.machine_components.machine_pass_direction import Pass_Direction
from knitting_machine.machine_components.needles import Needle
from knitting_machine.machine_components.yarn_carrier import Yarn_Carrier


def rack(machine_state, racking: float, comment: str = "") -> str:
    """
    :param machine_state: the current machine model to update
    :param racking: the new racking to set the machine to
    :param comment: additional details to document in the knitout
    :return: the racking instruction
    """
    machine_state._racking = racking
    # if racking != .25 and racking != -.75:  # racking for all needle knitting
    #     racking = math.floor(racking)
    return f"rack {racking} ;{comment}\n"


def _make_carrier_set(carrier: Yarn_Carrier) -> str:
    """
    Returns the string of the carrier formatted for knitout
    :param carrier: the set of carriers to be converted to a carrier set command parameter
    :return: the spaced carrier set parameter to be used in instructions
    """
    # if needle is not None:
    #     carrier.move_to_position(needle.position)
    return str(carrier)


def miss(machine_state, direction: Pass_Direction, needle: Needle, carrier_set: Yarn_Carrier, comment: str = "") -> str:
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
    assert machine_state.yarn_manager.is_active(carrier_set), f"Yarn-Carrier {carrier_set} is not active"
    carriers = _make_carrier_set(carrier_set)
    return f"miss {direction} {needle} {carriers};{comment}\n"


def knit(machine_state, direction: Pass_Direction, needle: Needle, carrier_set: Yarn_Carrier, comment: str = "", record_needle=True):
    """
    Pull a loop formed in direction D by the yarns in carriers CS through the loops on needle N,
    dropping them in the process.
    Knitting with an empty carrier set will drop
    :param record_needle: If true, records locations of loops at this position. Used for resetting sheets
    :param machine_state: the current machine model to update
    :param direction: the direction to pull the yarn across the needle from
    :param needle: the needle to make the loop on
    :param carrier_set: the set of carriers being used
    :param comment: additional details to document in the knitout
    :return: the knit instruction
    """
    loops = machine_state.knit(needle, carrier_set, record_needle=record_needle)
    carriers = _make_carrier_set(carrier_set)
    return f"knit {direction} {needle}{carriers} ;knit loops: {loops}. {comment}\n"


def tuck(machine_state, direction: Pass_Direction, needle: Needle, carrier_set: Yarn_Carrier, comment: str = "", record_needle=True) -> str:
    """
    Add a loop formed in direction D by the yarns held by carriers in CS to those already on needle N.
    Tucking with an empty carrier set will pull on the stitches without doing anything else (an "a-miss").
    :param record_needle: If true, records locations of loops at this position. Used for resetting sheets
    :param machine_state: the current machine model to update
    :param direction: the direction to pull the yarn across the needle from
    :param needle: the needle to make the loop on
    :param carrier_set: the set of carriers being used
    :param comment: additional details to document in the knitout
    :return: the tuck instruction
    """
    loops = machine_state.tuck(needle, carrier_set,record_needle=record_needle)
    carriers = _make_carrier_set(carrier_set)
    return f"tuck {direction} {needle}{carriers} ; tuck loops: {loops}. {comment}\n"


def split(machine_state, direction: Pass_Direction, start: Needle, target,
          carrier_set: Yarn_Carrier, comment: str = "", record_needle=True) -> str:
    """
    Pull a loop formed in direction D by the yarns in carriers CS through the loops on needle N,
    transferring the old loops to opposite-bed needle N2 in the process.
    Splitting with an empty carrier set will transfer
    :param record_needle: If true, records locations of loops at this position. Used for resetting sheets
    :param machine_state: the current machine model to update
    :param direction: the direction to pull the yarn across the needle from
    :param start: the first needle to make the loop on and transfer from
    :param target: the second needle to transfer the original loops from
    :param carrier_set: the set of carriers being used
    :param comment: additional details to document in the knitout
    :return: the split instruction
    """
    loops = machine_state.split(start, target, carrier_set, record_needle=record_needle)
    carriers = _make_carrier_set(carrier_set)
    return f"split {direction} {start} {target}{carriers} ;Split loops: {loops}. {comment}\n"


def drop(machine_state, needle: Needle, comment: str = "", record_needle=True) -> str:
    """
    Synonym for "knit + N".
    Drops the loops on the needle
    :param record_needle: If true, records locations of loops at this position. Used for resetting sheets
    :param machine_state: the current machine model to update
    :param needle: the needle to drop loops from
    :param comment: additional details to document in the knitout
    :return: the drop instruction
    """
    loops = machine_state.drop(needle, record_needle)
    return f"drop {needle} ;Dropped loops: {loops}. {comment}\n"


def xfer(machine_state, start: Needle, target: Needle, comment: str = "", record_needle:bool = True) -> str:
    """
    Synonym for "split + N N2".
    Transfer loops from needle 1 to needle 2, leaving needle 1 empty
    :param record_needle: If true, records locations of loops at this position. Used for resetting sheets
    :param machine_state: the current machine model to update
    :param start: the first needle to xfer from
    :param target: the second needle to xfer to
    :param comment: additional details to document in the knitout
    :return: the xfer instruction
    """
    machine_state.xfer(start, target, record_needle= record_needle)
    return f"xfer {start} {target} ;{comment}\n"


def bring_in(machine_state, carrier_set: Yarn_Carrier, comment: str = "") -> str:
    """
    enter is used to avoid confusion with "in" keyword. Brings yarn carrier into action without yarn holding hook
    :param machine_state: the current machine model to update
    :param carrier_set: the set of carriers to bring in
    :param comment: additional details to document in the knitout
    :return: in instruction
    """
    machine_state.bring_in(carrier_set)
    return f"in {_make_carrier_set(carrier_set)} ;{comment}{os.linesep}"


def inhook(machine_state, carrier_set: Yarn_Carrier, comment: str = "") -> str:
    """
    Indicate that the given carrier set should be brought into action using the yarn inserting hook when next used.
    The inserting hook will be parked just before the first stitch made with the carriers
    :param machine_state: the current machine model to update
    :param carrier_set: the set of carriers to bring in
    :param comment: additional details to document in the knitout
    :return: the inhook instruction
    """
    machine_state.in_hook(carrier_set)
    return f"inhook {_make_carrier_set(carrier_set)} ;{comment}\n"


def releasehook(machine_state, comment: str = "") -> str:
    """
    Release the yarns currently held in the yarn inserting hook.
    Must be proceeded by a call to inhook with the same carrier set and at least one knitting operation.
    :param machine_state: the current machine model to update
    :param comment: additional details to document in the knitout
    :return: the releasehook instruction
    """
    released_carrier = machine_state.yarn_manager.hooked_carrier
    machine_state.release_hook()
    if released_carrier is None:
        return f"; no-op. Releasehook with no hooked carriers\n"
    else:
        return f"releasehook {_make_carrier_set(released_carrier)} ;{comment}\n"


def outhook(machine_state, carrier_set: Yarn_Carrier, comment: str = "") -> str:
    """
    Release the yarns currently held in the yarn inserting hook.
    Must be proceeded by a call to inhook with the same carrier set and at least one knitting operation.
    :param machine_state: the current machine model to update
    :param carrier_set: the set of carriers to bring out
    :param comment: additional details to document in the knitout
    :return: the outhook instruction
    """
    machine_state.out_hook(carrier_set)
    return f"outhook {_make_carrier_set(carrier_set)} ;{comment}\n"


def out(machine_state, carrier_set: Yarn_Carrier, comment: str = "") -> str:
    """
    Bring a set of carriers out of action by directly moving into the grippers
    :param machine_state: the current machine model to update
    :param carrier_set: the set of carriers to bring out
    :param comment: additional details to document in the knitout
    :return: the out instruction
    """
    machine_state.out(carrier_set)
    return f"out {_make_carrier_set(carrier_set)} ;{comment}\n"
