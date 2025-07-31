"""Functions for managing yarn carriers in the virtual knitting machine."""
from knitout_interpreter.knitout_operations.carrier_instructions import Outhook_Instruction
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import Yarn_Carrier


def carrier(machine_state: Knitting_Machine, carrier_id: int) -> Yarn_Carrier:
    """Retrieves a yarn carrier from the virtual knitting machine by its ID.

    Args:
        machine_state: The virtual knitting machine containing the carrier system.
        carrier_id: The numeric identifier of the carrier to retrieve.

    Returns:
        The Yarn_Carrier object corresponding to the specified carrier ID.

    Raises:
        KeyError: If the carrier_id does not exist in the machine's carrier system.
        IndexError: If the carrier_id is outside the valid range of carrier indices.
    """
    return machine_state.carrier_system[carrier_id]


def cut_active_carriers(machine_state: Knitting_Machine) -> list[Outhook_Instruction]:
    """Creates and executes outhook instructions to cut all active carriers.

    This function generates outhook instructions for all currently active carriers in the machine state,
    executes them to update the machine state, and returns the list of instructions that were created.

    Args:
        machine_state: The virtual knitting machine whose active carriers should be cut.

    Returns:
        A list of Outhook_Instruction objects that were created and executed to cut all active carriers.
        The list will be empty if no carriers were active.
    """
    outhooks = [Outhook_Instruction(c, f"Outhooking all active carriers") for c in machine_state.carrier_system.active_carriers]
    for outhook in outhooks:
        outhook.execute(machine_state)
    return outhooks
