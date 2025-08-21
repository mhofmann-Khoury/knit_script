"""Functions for managing yarn carriers in the virtual knitting machine.

This module provides utility functions for working with yarn carriers in the virtual knitting machine environment.
It includes functions for retrieving specific carriers by ID and managing the lifecycle of active carriers through cutting operations.
These functions are commonly used in knit script standard library operations and provide essential carrier management capabilities for knitting machine control.
"""
from knitout_interpreter.knitout_operations.carrier_instructions import (
    Outhook_Instruction,
    Releasehook_Instruction,
)
from virtual_knitting_machine.Knitting_Machine import Knitting_Machine
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import (
    Yarn_Carrier,
)


def carrier(machine_state: Knitting_Machine, carrier_id: int) -> Yarn_Carrier:
    """Retrieve a yarn carrier from the virtual knitting machine by its ID.

    This function provides access to specific yarn carriers within the machine's carrier system.
     It serves as a convenient interface for accessing carriers by their numeric identifiers, which are commonly used throughout knit script programs for carrier operations.

    Args:
        machine_state (Knitting_Machine): The virtual knitting machine containing the carrier system to access.
        carrier_id (int): The numeric identifier of the carrier to retrieve. Must be within the valid range of available carriers.

    Returns:
        Yarn_Carrier: The Yarn_Carrier object corresponding to the specified carrier ID, containing all carrier state and configuration information.

    Raises:
        KeyError: If the carrier_id does not exist in the machine's carrier system.
        IndexError: If the carrier_id is outside the valid range of carrier indices for the current machine configuration.
    """
    return machine_state.carrier_system[carrier_id]


def cut_active_carriers(machine_state: Knitting_Machine) -> list[Outhook_Instruction]:
    """Create and execute outhook instructions to cut all active carriers.

    This function generates outhook instructions for all currently active carriers in the machine state,
     executes them to update the machine state, and returns the list of instructions that were created.
     This operation is commonly used at the end of knitting operations to properly terminate all yarn carriers and ensure clean completion of the knitting process.

    The function automatically identifies all active carriers, creates appropriate outhook instructions for each one,
     executes those instructions to update the machine state, and returns the instruction list for inclusion in knitout output.

    Args:
        machine_state (Knitting_Machine): The virtual knitting machine whose active carriers should be cut and terminated.

    Returns:
        list[Outhook_Instruction]: A list of Outhook_Instruction objects that were created and executed to cut all active carriers.
        The list will be empty if no carriers were active at the time of the call.

    Note:
        This function modifies the machine state by executing the outhook instructions. After execution, all previously active carriers will be inactive and properly terminated.
    """
    if machine_state.carrier_system.hooked_carrier is not None:
        ops = [Releasehook_Instruction(machine_state.carrier_system.hooked_carrier, f"Attempt hook release before cutting all yarns")]
    else:
        ops = []
    ops.extend([Outhook_Instruction(c, f"Outhooking all active carriers") for c in machine_state.carrier_system.active_carriers if c.yarn.has_loops])
    for outhook in ops:
        outhook.execute(machine_state)
    return ops
